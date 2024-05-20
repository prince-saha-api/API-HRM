from django.db import models
from user.models import User
from branch.models import Branch
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from helps.validators.common import validate_phone_number

class Department(Basic):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    manager = models.ManyToManyField(User)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.name} -- {self.branch.company.basic_information.name} - {self.branch.name}'
    
class Departmentmobilenumber(Basic):
    phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.phone} - {self.department.branch.company.basic_information.name} - {self.department.branch.name}'

class Departmentemail(Basic):
    email = models.EmailField(unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.email} - {self.department.branch.company.basic_information.name} - {self.department.branch.name}'

class Departmentimage(Basic):
    image = models.URLField(max_length=200, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.department.branch.company.basic_information.name} - {self.department.branch.name}'