from django.db import models
from user import models as MODELS_USER
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN
from contribution import models as MODELS_CONT
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic

class Department(Basic):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=14, unique=True, blank=True, null=True)
    fax = models.CharField(max_length=100, unique=True, blank=True, null=True)
    address = models.OneToOneField(MODELS_CONT.Address, on_delete=models.SET_NULL, blank=True, null=True)
    manager = models.ManyToManyField(MODELS_USER.User, blank=True, related_name='departmentone')
    user = models.ManyToManyField(MODELS_USER.User, blank=True, related_name='departmenttwo')
    company = models.ForeignKey(MODELS_COMP.Company, on_delete=models.SET_NULL, blank=True, null=True) # Will be remove later
    branch = models.ForeignKey(MODELS_BRAN.Branch, on_delete=models.CASCADE, related_name='department_branch')

    def __str__(self):
        return f'{self.name}'