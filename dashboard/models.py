from django.db import models


class Domain(models.Model):
    domain_name = models.TextField('domain_name', blank=False, null=True)
    last_expiration_date = models.DateTimeField('last_expiration_date', blank=True, null=True)
    days_left = models.IntegerField('days_left', blank=True, null=True)
    binom_allowed = models.TextField('binom_allowed', blank=True, null=True)
    binom_exists = models.TextField('binom_exists', blank=True, null=True)
    name_servers = models.TextField('name_servers', blank=True, null=True)
    registrar = models.TextField('registrar', blank=True, null=True)
    cloudflare_acc = models.TextField('cloudflare_acc', blank=True, null=True)
    ssl_days_left = models.IntegerField('ssl_days_left', blank=True, null=True)
    days_clicks_60 = models.IntegerField('days_clicks_60', blank=True, null=True)
    ssl_error = models.BooleanField('ssl_error', null=True, blank=True)
    archived = models.BooleanField('archived', null=True, blank=True)
    check_whois = models.IntegerField('check_whois', blank=True, null=True)
    binom_owner = models.BooleanField('binom_owner', blank=True, null=True)
    cf_ns = models.BooleanField('cf_ns', blank=True, null=True)
    registrar_acc = models.BooleanField('registrar_acc', blank=True, null=True)
    auto_renew = models.BooleanField('auto_renew', blank=True, null=True, default=None)

    def __str__(self):
        return self.domain_name
    

class DNS_Records(models.Model):
    domain = models.TextField('domain', blank=False, null=False)
    type = models.TextField('type', blank=True, null=True)
    content = models.TextField('content', blank=True, null=True)
    proxied = models.TextField('owner', blank=True, null=True)
    cf_email = models.TextField('cf_email', blank=True, null=True)
    record_id = models.TextField('record_id', blank=True, null=True)
    zone_id = models.TextField('zone_id', blank=True, null=True),
    
    def __str__(self):
        return self.domain
