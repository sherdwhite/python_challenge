from PythonChallengeApp.models import IPAddressInfo
from rest_framework import serializers


class IPInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IPAddressInfo
        fields = ['ip_address', 'geo_ip_city', 'geo_ip_country_code', 'geo_ip_country_name', 'geo_ip_latitude',
                  'geo_ip_longitude']
