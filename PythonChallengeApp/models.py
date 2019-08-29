from django.db import models


class IPAddresses(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    geo_ip_isp = models.CharField(max_length=100, null=True, blank=True)
    geo_ip_city = models.CharField(max_length=100, null=True, blank=True)
    geo_ip_country_code = models.CharField(max_length=100, null=True, blank=True)
    geo_ip_country_name = models.CharField(max_length=100, null=True, blank=True)
    geo_ip_latitude = models.FloatField(null=True, blank=True)
    geo_ip_longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.ip_address)
