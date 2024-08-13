from django.db import models
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from user import models as MODELS_USER
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN
from department import models as MODELS_DEPA

def generate_unique_code():
    return ghelp().getUniqueCodePattern()


def uploaddocs(instance, filename):
    return "static/noticeboardattachment/{uniquecode}uniquevalue{filename}".format(uniquecode=generate_unique_code(), filename=filename)

# Create your models here.
class Noticeboard(Basic):
    title = models.CharField(max_length=100)
    description = models.TextField()
    attachment = models.FileField(upload_to=uploaddocs, blank=True, null=True)
    publish_date = models.DateField(auto_created= True, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)

    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='Noticeboardone')
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='Noticeboardtwo')
    
    def __str__(self):
        return f'{self.title}'
    
class Noticeboardcompany(Basic):
    noticeboard = models.ForeignKey(Noticeboard, on_delete=models.CASCADE, default=None)
    company = models.ForeignKey(MODELS_COMP.Company, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.noticeboard} - {self.company}'
    
class Noticeboardbranch(Basic):
    noticeboard = models.ForeignKey(Noticeboard, on_delete=models.CASCADE, default=None)
    branch = models.ForeignKey(MODELS_BRAN.Branch, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.noticeboard} - {self.branch}'
    
class Noticeboarddepartment(Basic):
    noticeboard = models.ForeignKey(Noticeboard, on_delete=models.CASCADE, default=None)
    department = models.ForeignKey(MODELS_DEPA.Department, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.noticeboard} - {self.department}'
    
class Noticeboardemployee(Basic):
    noticeboard = models.ForeignKey(Noticeboard, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.noticeboard} - {self.user}'