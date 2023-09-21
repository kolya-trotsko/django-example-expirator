import sqlite3
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from dashboard.models import Domain
from dashboard.serializer import DomainSerializer
from domain_expiration.settings import DATABASES

def token_invalid():
    return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class DomainViewApi(APIView):
    serializer_class = DomainSerializer

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        key = request.headers.get("token", '')

        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            return token_invalid()

        try:
            with sqlite3.connect(DATABASES['default']['NAME']) as db:
                cur = db.cursor()
                data = {field: [row[0] for row in cur.execute(f"SELECT DISTINCT {field} FROM dashboard_domain").fetchall()] for field in ["name_servers", "binom_exists", "binom_allowed", "registrar"]}

            return Response({"token": token.key, **data, "days_left": "int", "days_clicks_60": "int", "overdue": "bool", "sslerror": "bool", "search_query": 'text', "count": 20, "page": 1}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"error - {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

    def post(self, request):
        key = request.headers.get("token", '')

        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            return token_invalid()

        try:
            filter_params = {field: request.data.get(field, False) for field in ["binom_allowed", "binom_exists", "registrar", "name_servers", "sslerror", "days_left", "overdue", "days_clicks_60"]}
            count, page_number, search_query = request.data.get('count', 20), request.data.get('page', 1), request.data.get('search_query', '')
            domains = Domain.objects.filter(domain_name__contains=search_query, **filter_params)
            paginator = Paginator(domains, count)
            page_number = min(max(1, int(page_number)), paginator.num_pages)
            domains = paginator.get_page(page_number)
            serializer = DomainSerializer(domains, many=True)

            return Response({"page": page_number, "max_page": paginator.num_pages, "count": count, "data": serializer.data, **filter_params}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginApi(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def post(self, request):
        username, password = request.data.get("username", ''), request.data.get("password", '')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, create = Token.objects.get_or_create(user=user)
            api_key = create.key if create else token.key
            return Response({"token": api_key}, status=status.HTTP_200_OK)
        else:
            return token_invalid()
