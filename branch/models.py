from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from django.db import models
from facility.models import *
from user.models import User
from company.models import Company
from helps.validators.common import validate_phone_number
from django.core.validators import MinValueValidator, MaxValueValidator
from contribution import models as CNTRIB

class Operatinghour(Basic):
    operating_hour_from = models.TimeField()
    operating_hour_to = models.TimeField()

    def __str__(self):
        return f'{self.operating_hour_from} - {self.operating_hour_to}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['operating_hour_from', 'operating_hour_to'], name='Operatinghour_operating_hour_from_operating_hour_to')]

class Branch(Basic):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branchone')
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    fax = models.CharField(max_length=100, unique=True, blank=True, null=True)
    address = models.OneToOneField(CNTRIB.Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.company.basic_information.name} - {self.name}'

class Branchphonenumber(Basic):
    phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.branch.company.basic_information.name} - {self.branch.name} - {self.phone}'

class Branchemail(Basic):
    email = models.EmailField(unique=True, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.branch.company.basic_information.name} - {self.branch.name} - {self.email}'

class Contactperson(Basic):
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.branch.company.basic_information.name} - {self.branch.name} - {self.person.username}'