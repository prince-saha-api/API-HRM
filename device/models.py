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

class Group(Basic):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.code} - {self.title}'

class Devicegroup(Basic):
    title = models.CharField(max_length=50, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['group', 'device'], name='group_device')]

    def __str__(self):
        return f'{self.title} - {self.group.title} - {self.device.title}'