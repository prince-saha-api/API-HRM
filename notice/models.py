from django.db import models
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from user import models as MODELS_USER
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN
from department import models as MODELS_DEPA

def generate_unique_code():
    return ghelp().getUniqueCodePattern()

def upload_noticeboard_files(instance, filename):
    return "files/notice/{uniquecode}uniquevalue{filename}".format(uniquecode=generate_unique_code(), filename=filename)


class Noticeboard(Basic):
    title = models.CharField(max_length=100)
    description = models.TextField()
    attachment = models.FileField(upload_to=upload_noticeboard_files, blank=True, null=True)
    publish_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)

    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='noticeboard_created_by')
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='noticeboard_updated_by')
    
    def __str__(self):
        return f'{self.title}'
    
class Noticeboardcompany(Basic):
    noticeboard = models.ForeignKey(Noticeboard, on_delete=models.CASCADE, related_name='noticeboardcompany_noticeboard')
    company = models.ForeignKey(MODELS_COMP.Company, on_delete=models.CASCADE, related_name='noticeboardcompany_company')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['noticeboard', 'company'], name='notice_company')]
    def __str__(self):
        return f'{self.noticeboard} - {self.company}'
    
class Noticeboardbranch(Basic):
    noticeboard = models.ForeignKey(Noticeboard, on_delete=models.CASCADE, related_name='noticeboardbranch_noticeboard')
    branch = models.ForeignKey(MODELS_BRAN.Branch, on_delete=models.CASCADE, related_name='noticeboardbranch_branch')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['noticeboard', 'branch'], name='notice_branch')]
    def __str__(self):
        return f'{self.noticeboard} - {self.branch}'
    
class Noticeboarddepartment(Basic):
    noticeboard = models.ForeignKey(Noticeboard, on_delete=models.CASCADE, related_name='noticeboarddepartment_noticeboard')
    department = models.ForeignKey(MODELS_DEPA.Department, on_delete=models.CASCADE, related_name='noticeboarddepartment_department')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['noticeboard', 'department'], name='notice_department')]
    def __str__(self):
        return f'{self.noticeboard} - {self.department}'
    
class Noticeboardemployee(Basic):
    noticeboard = models.ForeignKey(Noticeboard, on_delete=models.CASCADE, related_name='noticeboardemployee_noticeboard')
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='noticeboardemployee_user')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['noticeboard', 'user'], name='notice_user')]
    def __str__(self):
        return f'{self.noticeboard} - {self.user}'