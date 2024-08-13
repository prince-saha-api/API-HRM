from django.db import models
from helps.abstract.abstractclass import Basic
from user import models as MODELS_USER
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN
from department import models as MODELS_DEPA


# Create your models here.
class Noteboard(Basic):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to=MODELS_USER.uploaddocs, blank=True, null=True)
    publish_date = models.DateField(auto_created= True, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)

    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='Noteboardone')
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='Noteboardtwo')
    
    def __str__(self):
        return f'{self.title}'
    
class Noticeboardcompany(Basic):
    noteboard = models.ForeignKey(Noteboard, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(MODELS_COMP.Company, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.noteboard} - {self.company}'
    
class Noticeboardbranch(Basic):
    noteboard = models.ForeignKey(Noteboard, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.ForeignKey(MODELS_BRAN.Branch, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.noteboard} - {self.branch}'
    
class Noticeboarddepartment(Basic):
    noteboard = models.ForeignKey(Noteboard, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(MODELS_DEPA.Department, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.noteboard} - {self.department}'
    
class Noticeboardemployee(Basic):
    noteboard = models.ForeignKey(Noteboard, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.noteboard} - {self.user}'