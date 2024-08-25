from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from django.db import models
from company import models as MODELS_COMP
from contribution import models as MODELS_CONT

class Operatinghour(Basic):
    operating_hour_from = models.TimeField()
    operating_hour_to = models.TimeField()

    def __str__(self):
        return f'{self.operating_hour_from} - {self.operating_hour_to}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['operating_hour_from', 'operating_hour_to'], name='Operatinghour_operating_hour_from_operating_hour_to')]

class Branch(Basic):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(MODELS_COMP.Company, on_delete=models.CASCADE, related_name='branch_company')
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=14, unique=True, blank=True, null=True)
    fax = models.CharField(max_length=100, unique=True, blank=True, null=True)
    address = models.OneToOneField(MODELS_CONT.Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'