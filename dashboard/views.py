import sqlite3
import requests
import pyotp
import json
import multiprocessing
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView
from rest_framework.authtoken.models import Token
from dashboard.models import Domain
from domain_expiration.settings import DATABASES
from .forms import LoginUserForm


def is_token_valid(totp, URL, API):
    code2fa = totp.now()
    today = datetime.today().strftime('%Y-%m-%d')
    days_ago = datetime.today() - timedelta(days=60)
    days_ago = days_ago.strftime('%Y-%m-%d')
    url = f"{URL}?page=Campaigns&status=all&date_e={today}&date_s={days_ago}&date=12&group=all&traffic_source=all&timezone=+2:00&api_key={API}&code={code2fa}"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def get_campaign_data(binom, domain):
    try:
        data = is_token_valid(pyotp.TOTP(binom[3]), binom[4], binom[5])
        result = []
        for row in data:
            if row != 'error':
                domain_name = row["domain_name"]
                if domain_name == domain:
                    id = str(row["id"])
                    name = row["name"]
                    clicks = row["clicks"]
                    group = row["group_name"]
                    result.append((id, name, binom[0], group, clicks))
        return result
    except Exception as e:
        return []

def save_changes(request):
    try:
        with sqlite3.connect(DATABASES['default']['NAME']) as db:
            cur = db.cursor()
            domains = cur.execute("SELECT * FROM DNS_Records").fetchall()
            for domain in domains:
                content_value = request.POST.get(f'content_{domain[0]}')
                if content_value != domain[3]:
                    email = domain[5]
                    token = cur.execute("SELECT key FROM cloudflares WHERE email=?", (email,)).fetchone()[0]
                    identifier = domain[6]
                    zone_identifier = domain[7]
                    headers = {
                        "Content-Type": "application/json",
                        "X-Auth-Email": email,
                        "X-Auth-Key": token,
                    }
                    if 'save_change' in request.POST:
                        url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{identifier}"
                        prox = domain[4]
                        payload = {
                            "name": domain[1],
                            "content": content_value,
                            "type": domain[2],
                            "proxied": prox,
                            "priority": 0
                        }
                        requests.put(url, json=payload, headers=headers)
                        cur.execute("UPDATE DNS_Records SET content = ? WHERE id = ?", (content_value, domain[0]))
                        db.commit()
        return True
    except Exception as e:
        return False

class DomainsView(ListView):
    def index(request):
        if request.method == 'POST':
            if 'archived' in request.POST:
                with sqlite3.connect(DATABASES['default']['NAME']) as db:
                    cur = db.cursor()
                    domain_name = request.POST.get("archived")
                    new_archived = cur.execute("SELECT archived FROM dashboard_domain WHERE domain_name=?", (domain_name,)).fetchone()[0]
                    new_archived = not new_archived
                    cur.execute("UPDATE dashboard_domain SET archived = ? WHERE domain_name=?", (new_archived, domain_name))
                    db.commit()

        search_query = request.GET.get('query', '')
        order = request.GET.get('order_by', 'id')
        filter_over = request.GET.getlist('filter_over', [])
        filter_over = [value.replace("'", "").replace('"', '') for value in filter_over]
        page_number = request.GET.get('page')
        domains = Domain.objects.filter(domain_name__contains=search_query)

        if "overdue" in filter_over:
            domains = domains.filter(days_left__lt=0)
        if "overdue_7" in filter_over:
            domains = domains.filter(days_left__lt=8, days_left__gt=0)
        if "not_None" in filter_over:
            domains = domains.exclude(days_left=None)
        if "not_overdue" in filter_over:
            domains = domains.filter(days_left__gte=0)
        if "Not_archived" in filter_over:
            domains = domains.filter(archived=False)
        if "archived" in filter_over:
            domains = domains.filter(archived=True)
        
        paginator = Paginator(domains.order_by(order), 100)
        domains = paginator.get_page(page_number)
        
        return render(request, 'dashboard/index.html', {'title': 'Dashboard', 'domains': domains, 'order_by': order, 'filter_over': filter_over})

    def about(request):
        username = request.user.username
        for user in User.objects.all():
            if user.username == username:
                token, create = Token.objects.get_or_create(user=user)
                api_key = create.key if token is not None else None
                return render(request, 'dashboard/about.html', {'token': api_key, 'Username': username})

    def campaigns(request):
        result = False
        domain = False
        if request.method == 'POST' and 'check' in request.POST:
            domain = request.POST.get("domain", None)

        return render(request, 'dashboard/campaigns.html', {'title': 'Campaigns', 'result': result, 'domain': domain})

    def dns(request):
        if request.method == 'POST' and ('save_change' in request.POST or 'add_dns' in request.POST):
            p = multiprocessing.Process(target=request.POST['save_change'], kwargs={"request": request})
            p.start()

        order_by = request.GET.get('order_by', 'id')
        search_query = request.GET.get('query', '')
        filters = tuple(request.GET.getlist('filters', ('A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT'))) + ("",)

        with sqlite3.connect(DATABASES['default']['NAME']) as db:
            cur = db.cursor()
            try:
                domains = cur.execute(f"SELECT * FROM DNS_Records WHERE content LIKE '%{search_query}%' AND type IN {filters} ORDER BY {order_by}")
            except:
                domains = cur.execute(f"SELECT * FROM DNS_Records WHERE content LIKE '%{search_query}%' AND type IN {(filters,)} ORDER BY {order_by}")

        return render(request, 'dashboard/dns_records.html', {
            'title': 'DNS_Records',
            'domains': domains,
            'query': search_query,
            'filters': filters,
            'record_types': ('A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT')
        })

    def services(request):
        if request.method == 'POST':
            with sqlite3.connect(DATABASES['default']['NAME']) as db:
                cur = db.cursor()
                if 'add_cf' in request.POST:
                    key = request.POST.get('key')
                    email = request.POST.get('email')
                    cur.execute("INSERT INTO cloudflares (key, email) VALUES (?, ?)", (key, email))
                elif 'delete_cf' in request.POST:
                    key = request.POST.get('key')
                    email = request.POST.get('email')
                    cur.execute("DELETE FROM cloudflares WHERE key = ? AND email = ?", (key, email))
                if 'add_ukraine' in request.POST:
                    api_key = request.POST.get('api_key')
                    owner = request.POST.get('owner')
                    cur.execute("INSERT INTO ukraines (api_key, owner) VALUES (?, ?)", (api_key, owner))
                elif 'delete_ukraine' in request.POST:
                    api_key = request.POST.get('api_key')
                    owner = request.POST.get('owner')
                    cur.execute("DELETE FROM ukraines WHERE api_key = ? AND owner = ?", (api_key, owner))
                if 'add_namecheap' in request.POST:
                    api_key = request.POST.get('api_key')
                    api_user = request.POST.get('api_user')
                    client_ip = request.POST.get('client_ip')
                    cur.execute("INSERT INTO namecheaps (api_key, api_user, client_ip) VALUES (?, ?, ?)", (api_key, api_user, client_ip))
                elif 'delete_namecheap' in request.POST:
                    api_key = request.POST.get('api_key')
                    api_user = request.POST.get('api_user')
                    client_ip = request.POST.get('client_ip')
                    cur.execute("DELETE FROM namecheaps WHERE api_key = ? AND api_user = ? AND client_ip = ?", (api_key, api_user, client_ip))
                if 'add_godaddy' in request.POST:
                    api_key = request.POST.get('api_key')
                    api_secret = request.POST.get('api_secret')
                    owner = request.POST.get('owner')
                    cur.execute("INSERT INTO godaddies (api_key, api_secret, owner) VALUES (?, ?, ?)", (api_key, api_secret, owner))
                elif 'delete_godaddy' in request.POST:
                    api_key = request.POST.get('api_key')
                    api_secret = request.POST.get('api_secret')
                    owner = request.POST.get('owner')
                    cur.execute("DELETE FROM godaddies WHERE api_key = ? AND api_secret = ? AND owner = ?", (api_key, api_secret, owner))
                if 'add_binom' in request.POST:
                    binom = request.POST.get('binom')
                    url_1 = request.POST.get('url_1')
                    url_2 = request.POST.get('url_2')
                    otp = request.POST.get('otp')
                    api = request.POST.get('api')
                    hash = request.POST.get('hash')
                    owner = request.POST.get('owner')
                    cur.execute("INSERT INTO binoms (binom, url_1, url_2, otp, api, hash, owner) VALUES (?, ?, ?, ?, ?, ?, ?)", (binom, url_1, url_2, otp, api, hash, owner))
                elif 'delete_binom' in request.POST:
                    binom = request.POST.get('binom')
                    url_1 = request.POST.get('url_1')
                    url_2 = request.POST.get('url_2')
                    otp = request.POST.get('otp')
                    api = request.POST.get('api')
                    hash = request.POST.get('hash')
                    owner = request.POST.get('owner')
                    cur.execute("DELETE FROM binoms WHERE binom = ? AND url_1 = ? AND url_2 = ? AND otp = ? AND api = ? AND hash = ? AND owner = ?", (binom, url_1, url_2, otp, api, hash, owner))
                db.commit()
        with sqlite3.connect(DATABASES['default']['NAME']) as db:
            cur = db.cursor()
            godaddies = cur.execute("SELECT * FROM godaddies").fetchall()
            namecheaps = cur.execute("SELECT * FROM namecheaps").fetchall()
            cloudflares = cur.execute("SELECT * FROM cloudflares").fetchall()
            ukraines = cur.execute("SELECT * FROM ukraines").fetchall()
            binoms = cur.execute("SELECT * FROM binoms").fetchall()
            cur.close()
        return render(request, 'dashboard/services.html', {
            'title': 'Services',
            'godaddies': godaddies,
            'namecheaps': namecheaps,
            'cloudflares': cloudflares,
            'ukraines': ukraines,
            'binoms': binoms
        })

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'dashboard/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, error=True))

    def get_success_url(self):
        return reverse_lazy('index')

def logout_user(request):
    logout(request)
    return redirect('login')
