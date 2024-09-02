from django.db import models
from user import models as MODELS_USER
from django.contrib.postgres.fields import ArrayField
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from django.core.exceptions import ValidationError
from helps.choice import common as CHOICE
from django.core.validators import MinValueValidator, MaxValueValidator
from hrm_settings import models as MODELS_SETT

def generate_unique_code():
    return ghelp().getUniqueCodePattern()

def upload_leaverequest_file(instance, filename):
    return "files/user/{unique}/leaverequest/{uniquecode}uniquevalue{filename}".format(unique=instance.user.uniqueid, uniquecode=generate_unique_code(), filename=filename)


class Holiday(Basic):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField()
    is_recuring = models.BooleanField(default=True)
    employee_grade = models.ForeignKey(MODELS_USER.Grade, on_delete=models.SET_NULL, blank=True, null=True)

    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='holidayone')
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='holidaytwo')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['title', 'date'], name='Holiday_title_date')]

    def __str__(self):
        return f'{self.code} - {self.title}'
    
class Leavepolicy(Basic):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    allocation_days = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    leave_type = models.CharField(max_length=20, choices=CHOICE.LEAVE_TYPE)

    max_consecutive_days = models.IntegerField(validators=[MinValueValidator(0)], default=1) # done
    
    require_attachment = models.BooleanField(default=True) # done
    
    is_optional = models.BooleanField(default=False)
    is_calendar_day = models.BooleanField(default=False) # done

    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='leavepolicyone')
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='leavepolicytwo')

    def __str__(self):
        return f'{self.name}'
    
class Leavepolicyassign(Basic):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='leavepolicyassign_user')
    leavepolicy = models.ForeignKey(Leavepolicy, on_delete=models.CASCADE)

    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='leavepolicyassign_updated_by')
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='leavepolicyassign_created_by')
    
    def __str__(self):
        return f'{self.user.username} - {self.leavepolicy.name}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'leavepolicy'], name='Leavepolicyassign_user_leavepolicy')]
    
class Approvedleave(Basic):
    leavepolicy = models.ForeignKey(Leavepolicy, on_delete=models.CASCADE)
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='leaveallocationone')
    date = models.DateField()

    approved_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='leaveallocationtwo')

    def __str__(self):
        return f'{self.user.username} - { self.leavepolicy.name}'
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['leavepolicy', 'user', 'date'], name='Leaveallocation_leavepolicy_user_date')]

class Leavesummary(Basic):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='leavesummary_user')
    leavepolicy = models.ForeignKey(Leavepolicy, on_delete=models.CASCADE, related_name='leavesummary_leavepolicy')
    total_allocation = models.IntegerField(validators=[MinValueValidator(1)])
    total_consumed = models.IntegerField(validators=[MinValueValidator(0)])
    total_left  = models.IntegerField(validators=[MinValueValidator(0)])
    fiscal_year = models.ForeignKey(MODELS_SETT.Fiscalyear, on_delete=models.CASCADE, related_name='leavesummary_fiscal_year')

    def __str__(self):
        return f'{self.total_left} - {self.user.username} - { self.leavepolicy.name}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'leavepolicy'], name='Leavesummary_user_leavepolicy')]

class Leaverequest(Basic):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='leaverequestone')
    leavepolicy = models.ForeignKey(Leavepolicy, on_delete=models.CASCADE, related_name='leavepolicy_leaverequest')
    request_type = models.CharField(max_length=20, choices=CHOICE.LEAVEREQUEST_TYPE)
    exchange_with = models.ForeignKey(Leavepolicy, on_delete=models.SET_NULL, blank=True, null=True, related_name='exchange_with_leaverequest')
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    total_leave = models.IntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    valid_leave_dates = ArrayField(models.DateField(blank=True, null=True), null=True, blank=True)
    attachment = models.FileField(upload_to=upload_leaverequest_file, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICE.STATUS, default=CHOICE.STATUS[0][1])
    reason = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='leaverequesttwo')

    def __str__(self):
        return f'{self.user.username} - {self.leavepolicy.name} - {self.status}'