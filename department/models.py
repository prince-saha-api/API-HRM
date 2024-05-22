from django.db import models
from user.models import User
from company.models import Company
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from helps.validators.common import validate_phone_number

class Department(Basic):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    manager = models.ManyToManyField(User, blank=True, related_name='departmentone')
    user = models.ManyToManyField(User, blank=True, related_name='departmenttwo')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
    
class Departmentmobilenumber(Basic):
    phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.phone}'

class Departmentemail(Basic):
    email = models.EmailField(unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.email}'

class Departmentimage(Basic):
    image = models.URLField(max_length=200, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.department.name}'