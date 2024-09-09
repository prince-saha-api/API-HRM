from django.db import models
from user import models as MODELS_USER
from department import models as MODELS_DEPA
from helps.choice import common as CHOICE
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Timedetails, Timedetailscode

class Attendance(Timedetails):
    date = models.DateField()

    in_time = models.TimeField(blank=True, null=True)
    out_time = models.TimeField(blank=True, null=True)

    late_time = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    early_leave = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    over_time = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    working_minutes = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    total_minutes = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    
    employee = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(MODELS_DEPA.Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey(MODELS_USER.Designation, on_delete=models.SET_NULL, null=True, blank=True)
    shift = models.ForeignKey(MODELS_USER.Shift, on_delete=models.SET_NULL, null=True, blank=True)

    attendance_mode = models.CharField(max_length=20, choices=CHOICE.ATTENDANCE_FROM)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['date', 'employee'], name='Attendance_date_employee')]
    def __str__(self):
        return f'{self.date} - {self.employee.username} - {self.in_time} - {self.out_time} - {self.total_minutes}'

class Attendancestatus(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=CHOICE.ATTENDANCE_STATUS)
    def __str__(self):
        return f'{self.attendance.date} - {self.attendance.employee.username} - {self.status}'

class Devicelogs(Timedetails):
    date = models.DateField()
    in_time = models.TimeField()
    employee = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['employee', 'date', 'in_time'], name='Devicelogs_employee_date_in_time')]
    def __str__(self):
        return f'{self.date} - {self.employee.username}'

class Remotelogs(Timedetails):
    date = models.DateField()
    time = models.TimeField()

    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)], blank=True, null=True)
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)], blank=True, null=True)

    device = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    
    employee = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['employee', 'date', 'time'], name='Remotelogs_employee_date_time')]
    def __str__(self):
        return f'{self.date} - {self.employee.username}'

class Requestremoteattendance(Timedetailscode):
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()

    in_out_times = ArrayField(models.TimeField(blank=True, null=True), null=True, blank=True)

    status = models.CharField(max_length=20, choices=CHOICE.STATUS, default=CHOICE.STATUS[0][1])
    reject_reason = models.CharField(max_length=200, blank=True, null=True)

    requested_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='requestremoteattendanceone')
    decisioned_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='requestremoteattendancetwo')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['requested_by', 'date'], name='Requestremoteattendance_requested_by_date')]
    def __str__(self):
        return f'{self.date} - {self.requested_by.username} - {self.status}'
    
    # def save(self, *args, **kwargs):
    #     if self.status == STATUS[1][1]:
    #         Attendance(
    #             date=self.date,
    #             in_time=self.in_time,
    #             out_time=self.out_time,
    #             in_out_times=self.in_out_times,
    #             employee=self.requested_by,
    #             attendance_from=ATTENDANCE_FROM[2][1]
    #         ).save()
    #     else:
    #         attendance = Attendance.objects.filter(date=self.date, employee=self.requested_by)
    #         if attendance.exists(): attendance.delete()
    #     super().save(*args, **kwargs)

class Requestmanualattendance(Timedetailscode):
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()

    admin_note = models.CharField(max_length=200, blank=True, null=True)

    status = models.CharField(max_length=20, choices=CHOICE.STATUS, default=CHOICE.STATUS[0][1])
    reject_reason = models.CharField(max_length=200, blank=True, null=True)

    requested_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='requestmanualattendanceone')
    decisioned_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='requestmanualattendancetwo')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['requested_by', 'date'], name='Requestmanualattendance_requested_by_date')]
    def __str__(self):
        return f'{self.date} - {self.requested_by.username} - {self.status}'
    
    # def save(self, *args, **kwargs):
    #     if self.status == STATUS[1][1]:
    #         Attendance(
    #             date=self.date,
    #             in_time=self.in_time,
    #             out_time=self.out_time,
    #             employee=self.requested_by,
    #             attendance_from=ATTENDANCE_FROM[1][1]
    #         ).save()
    #     else:
    #         attendance = Attendance.objects.filter(date=self.date, employee=self.requested_by)
    #         if attendance.exists(): attendance.delete()
    #     super().save(*args, **kwargs)