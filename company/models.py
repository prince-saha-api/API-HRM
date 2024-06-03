from django.db import models
from django.db.models import JSONField
from user import models as MODELS_USER
from helps.model.modelhelps import setSettings
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

class Updatecompanytypeconfig(Basic):
    backup_will_be_deleted_after_nth_records = models.IntegerField(validators=[MinValueValidator(1)], default=5)

    def __str__(self):
        return f'{self.backup_will_be_deleted_after_nth_records}'
    def save(self, *args, **kwargs):
        if self.id is not None: Updatecompanytypeconfig.objects.exclude().delete()
        else: Updatecompanytypeconfig.objects.all().delete()
        super().save(*args, **kwargs)

class Companytype(Basic):
    name = models.CharField(max_length=50)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.code} - {self.name}'
    def save(self, *args, **kwargs):

        self.code = setSettings(self.id, self.code, 'CMPTP', Updatecompanytypeconfig, Updatecompanytype)

        update_info = {'name': self.name,'updated_by': self.created_by,'is_active': self.is_active}
        if self.id != None: update_info['updated_by']=self.updated_by
        Updatecompanytype.objects.create(code=self.code, update_info=update_info)
        super().save(*args, **kwargs)

class Updatecompanytype(Basic):
    update_info = JSONField(default=dict)
 
    def __str__(self):
        return f'{self.code}'

# class Updatebasicinformationconfig(Basic):
#     backup_will_be_deleted_after_nth_records = models.IntegerField(validators=[MinValueValidator(1)], default=5)
#     def __str__(self):
#         return f'{self.backup_will_be_deleted_after_nth_records}'
#     def save(self, *args, **kwargs):
#         if self.id is not None: Updatebasicinformationconfig.objects.exclude().delete()
#         else: Updatebasicinformationconfig.objects.all().delete()
#         super().save(*args, **kwargs)

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

    cupdated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='basicinformationone')
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='basicinformationtwo')

    def __str__(self):
        return f'{self.name}'
    # def save(self, *args, **kwargs):
    #     self.code = setSettings(self.id, self.code, 'BASIC', Updatebasicinformationconfig, Updatebasicinformation)
    #     update_info = {'name': self.name,
    #                    'legal_name': self.legal_name,
    #                    'establishment_date': ghelp().convertDateformat_STR_y_m_d(self.establishment_date),
    #                    'type': self.type.id,
    #                    'business_registration_number': self.business_registration_number,
    #                    'tax_id_number': self.tax_id_number,
    #                    'description': self.description,
    #                    'website_url': self.website_url,
    #                    'primary_email': self.primary_email,
    #                    'primary_phone_number': self.primary_phone_number,
    #                    'updated_by': self.created_by,
    #                    'is_active': self.is_active
    #                    }
    #     if self.id != None: update_info['updated_by']=self.updated_by
    #     Updatebasicinformation.objects.create(code=self.code, update_info=update_info)
    #     super().save(*args, **kwargs)


# class Updatebasicinformation(Basic):
#     update_info = JSONField(default=dict)
#     def __str__(self):
#         return f'{self.code}'

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

class Company(Basic):
    basic_information = models.OneToOneField(Basicinformation, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.OneToOneField(MODELS_CONT.Address, on_delete=models.SET_NULL, blank=True, null=True)
    company_owner = models.ManyToManyField(MODELS_USER.User)

    def __str__(self):
        return f'{self.basic_information.name}'

class Bankinformation(Basic):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank_account = models.OneToOneField(MODELS_CONT.Bankaccount, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.company.basic_information.name} -- {self.bank_account.bank_name}'