from django.db import models
from helps.abstract.abstractclass import Basic
from helps.common.generic import Generichelps as ghelp
from django.core.validators import MinValueValidator, MaxValueValidator
from user import models as MODELS_USER
from helps.choice import common as CHOICE
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN
from department import models as MODELS_DEPA

def generate_unique_code():
    return ghelp().getUniqueCodePattern()

def uploadjobhistory(instance, filename):
    return "user/{unique}/job_history/{uniquecode}uniquevalue{filename}".format(unique=instance.user.uniqueid, uniquecode=generate_unique_code(), filename=filename)


class Employeejobhistory(Basic):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='employeejobhistory_user')
    effective_from = models.DateField()
    increment_on = models.CharField(max_length=50, choices=CHOICE.INCREMENT_ON, blank=True, null=True)
    salary = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    increment_amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    
    company = models.ForeignKey(MODELS_COMP.Company, on_delete=models.SET_NULL, blank=True, null=True, related_name='employeejobhistory_company')
    branch = models.ForeignKey(MODELS_BRAN.Branch, on_delete=models.SET_NULL, blank=True, null=True, related_name='employeejobhistory_branch')
    department = models.ForeignKey(MODELS_DEPA.Department, on_delete=models.SET_NULL, blank=True, null=True, related_name='employeejobhistory_department')
    designation = models.ForeignKey(MODELS_USER.Designation, on_delete=models.SET_NULL, blank=True, null=True, related_name='employeejobhistory_designation')
    employee_type = models.CharField(max_length=50, blank=True, null=True)

    date = models.DateField(blank=True, null=True)
    status_adjustment = models.CharField(max_length=50, choices=CHOICE.STATUS_ADJUSTMENT, blank=True, null=True)
    appraisal_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='employeejobhistory_appraisal_by')
    comment = models.TextField(blank=True, null=True)
    doc = models.FileField(upload_to=uploadjobhistory, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'