from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from django.db import models

class Device(Basic):
    title = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, default='admin')
    password = models.CharField(max_length=50, default='admin1234')
    location = models.CharField(max_length=100, blank=True, null=True)
    macaddress = models.CharField(max_length=50, blank=True, null=True)
    deviceip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)

    def __str__(self):
        return f'{self.code} - {self.title}'

class Devicegroup(Basic):
    title = models.CharField(max_length=50, unique=True)
    device = models.ManyToManyField(Device, blank=True)

    def __str__(self):
        return f'{self.title} - {[item.title for item in self.device.all()]}'