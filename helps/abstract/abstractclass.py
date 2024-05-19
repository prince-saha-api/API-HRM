from helps.common.generic import Generichelps as ghelp
from django.db import models 

def generate_unique_code():
    return ghelp().getUniqueCodePattern()

class Timedetails(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: 
        abstract = True

class Timedetailscode(Timedetails):
    code = models.CharField(max_length=30, unique=True, default=generate_unique_code, editable=False)
    class Meta: 
        abstract = True

class Basic(Timedetailscode):
    is_active = models.BooleanField(default=True)
    class Meta: 
        abstract = True

class Createdinfoint(models.Model):
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    class Meta: 
        abstract = True