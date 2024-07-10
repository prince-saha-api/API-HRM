from django.db import models
from django.db.models import JSONField
from user import models as MODELS_USER
from helps.validators.company.validator import *
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from helps.validators.common import validate_phone_number
from django.core.validators import MinValueValidator, MaxValueValidator
from contribution import models as MODELS_CONT

def generate_unique_code():
    return ghelp().getUniqueCodePattern()

def uploadcompanylogo(instance, filename):
    return "files/company/{name}/logo/{uniquecode}uniquevalue{filename}".format(name=instance.name, uniquecode=generate_unique_code(), filename=filename)

class Companytype(Basic):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return f'{self.id} - {self.code} - {self.name}'


class Basicinformation(Basic):
    name = models.CharField(max_length=100, unique=True)
    legal_name = models.CharField(max_length=100, blank=True, null=True)
    establishment_date = models.DateField(blank=True, null=True)
    industry_type = models.ForeignKey(Companytype, on_delete=models.SET_NULL, blank=True, null=True)
    business_registration_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    tax_id_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    bin_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website_url = models.URLField(max_length=200, unique=True, blank=True, null=True)
    primary_email = models.EmailField(unique=True, blank=True, null=True)
    primary_phone_number = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    fax = models.CharField(max_length=100, unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to=uploadcompanylogo, blank=True, null=True)
    address = models.OneToOneField(MODELS_CONT.Address, on_delete=models.SET_NULL, blank=True, null=True)

    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='basicinformationone')
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='basicinformationtwo')

    def __str__(self):
        return f'{self.name}'

class Companymobilenumber(Basic):
    phone_number = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    company = models.ForeignKey(Basicinformation, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.phone_number}'

class Companyemail(Basic):
    email = models.EmailField(unique=True, blank=True, null=True)
    company = models.ForeignKey(Basicinformation, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.email}'

required_fields = ['company_owner']
class Company(Basic):
    basic_information = models.OneToOneField(Basicinformation, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.OneToOneField(MODELS_CONT.Address, on_delete=models.SET_NULL, blank=True, null=True)
    company_owner = models.ManyToManyField(MODELS_USER.User, blank=True)

    def __str__(self):
        return f'{self.basic_information.name}'

class Bankinformation(Basic):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank_account = models.OneToOneField(MODELS_CONT.Bankaccount, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.company.basic_information.name} -- {self.bank_account.bank_name}'