from django.db import models


class IPAddresses(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip_address)
