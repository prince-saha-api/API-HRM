from django.core.validators import MinValueValidator, MaxValueValidator
from helps.abstract.abstractclass import Basic, Createdinfoint
from django.db import models


class Address(Basic, Createdinfoint):
    name = models.CharField(max_length=100, blank=True, null=True)
    alias = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state_division = models.CharField(max_length=50, blank=True, null=True)
    post_zip_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)], blank=True, null=True)
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)], blank=True, null=True)

    def __str__(self):
        return f'{self.city} -- {self.address}'
    
class Bankaccounttype(Basic):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.code} -- {self.name}'
    
class Bankaccount(Basic):
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.ForeignKey(Bankaccounttype, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=50, blank=True, null=True)
    routing_no = models.CharField(max_length=50, blank=True, null=True)
    swift_bic = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.bank_name} -- {self.address}'
