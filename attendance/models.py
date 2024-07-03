from django.db import models
from user.models import User, Shiftchangelog
from helps.choice.common import ATTENDANCE_FROM, STATUS
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from hrm_settings import models as MODELS_HRMS
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Timedetails, Timedetailscode
from workingshift.models import Globalbuffertime

class Attendance(Timedetails):
    date = models.DateField()

    in_time = models.TimeField(blank=True, null=True)
    out_time = models.TimeField(blank=True, null=True)

    in_negative_minutes = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    in_positive_minutes = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    out_negative_minutes = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    out_positive_minutes = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    late_in_based_on_buffertime = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    early_leave_based_on_buffertime = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    total_minutes = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    in_out_times = ArrayField(models.TimeField(blank=True, null=True), null=True, blank=True)
    # holiday = models.ForeignKey(Holiday, on_delete=models.SET_NULL, null=True, blank=True)
    # office_off_day = models.ForeignKey(MODELS_HRMS.Weeklyholiday, on_delete=models.SET_NULL, null=True, blank=True)
    buffer_time_minutes = models.CharField(max_length=25, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    attendance_from = models.CharField(max_length=20, choices=ATTENDANCE_FROM)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['date', 'employee'], name='Attendance_date_employee')]
    def __str__(self):
        return f'{self.date} - {self.employee.username} - {self.in_time} - {self.out_time} - {self.total_minutes} - {self.late_in_based_on_buffertime} - {self.early_leave_based_on_buffertime}'

    def save(self, *args, **kwargs):
        self.date = f'{self.date}'

        if self.in_out_times == None:
            in_out_times = []
            if self.in_time: in_out_times.append(self.in_time)
            if self.out_time: in_out_times.append(self.out_time)
            self.in_out_times = in_out_times

        if len(self.in_out_times) == 0:
            if self.in_time: self.in_out_times.append(self.in_time)
            if self.out_time: self.in_out_times.append(self.out_time)

        shiftchangelog = Shiftchangelog.objects.filter(date=self.date, user=self.employee)

        if shiftchangelog.exists():
            shiftchangelog = shiftchangelog.first()
            shift = shiftchangelog.newshift

            details = ghelp().getattendancedetails(Globalbuffertime, MODELS_HRMS.Weeklyholiday, shift, self.date, self.in_time, self.out_time)
            self.in_negative_minutes = details['in_negative_minutes']
            self.in_positive_minutes = details['in_positive_minutes']
            self.out_negative_minutes = details['out_negative_minutes']
            self.out_positive_minutes = details['out_positive_minutes']
            
            self.late_in_based_on_buffertime = details['late_in_based_on_buffertime']
            self.early_leave_based_on_buffertime = details['early_leave_based_on_buffertime']

            self.total_minutes = details['total_minutes']
            # if details['office_off_day']: self.office_off_day = details['office_off_day']
        else:
            shift = self.employee.shift

            details = ghelp().getattendancedetails(Globalbuffertime, MODELS_HRMS.Weeklyholiday, shift, self.date, self.in_time, self.out_time)
            self.in_negative_minutes = details['in_negative_minutes']
            self.in_positive_minutes = details['in_positive_minutes']
            self.out_negative_minutes = details['out_negative_minutes']
            self.out_positive_minutes = details['out_positive_minutes']

            self.late_in_based_on_buffertime = details['late_in_based_on_buffertime']
            self.early_leave_based_on_buffertime = details['early_leave_based_on_buffertime']
            self.buffer_time_minutes = details['buffer_time_minutes']

            self.total_minutes = details['total_minutes']
            # if details['office_off_day']: self.office_off_day = details['office_off_day']

        super().save(*args, **kwargs)

class Devicelogs(Timedetails):
    date = models.DateField()
    in_time = models.TimeField()
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
    
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['employee', 'date', 'time'], name='Remotelogs_employee_date_time')]
    def __str__(self):
        return f'{self.date} - {self.employee.username}'

class Requestremoteattendance(Timedetailscode):
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()

    in_out_times = ArrayField(models.TimeField(blank=True, null=True), null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default=STATUS[0][1])
    reject_reason = models.CharField(max_length=200, blank=True, null=True)

    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='requestremoteattendanceone')
    decisioned_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='requestremoteattendancetwo')

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

    status = models.CharField(max_length=20, choices=STATUS, default=STATUS[0][1])
    reject_reason = models.CharField(max_length=200, blank=True, null=True)

    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='requestmanualattendanceone')
    decisioned_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='requestmanualattendancetwo')

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