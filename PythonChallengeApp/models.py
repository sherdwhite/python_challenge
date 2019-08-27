from django.db import models
import datetime


class InputFile(models.Model):
    names = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.names)