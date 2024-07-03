from django.core.validators import MinValueValidator, MaxValueValidator
from helps.common.generic import Generichelps as ghelp
from django.core.exceptions import ValidationError
from helps.abstract.abstractclass import Basic
from helps.choice import common as CHOICE
from django.db import models

class Weekdays(Basic):
    day = models.CharField(max_length=10, choices=CHOICE.DAYS, unique=True)
    def __str__(self):
        return f'{self.day}'

class Weeklyholiday(Basic):
    day = models.ManyToManyField(Weekdays, blank=True)
    def __str__(self):
        return f'{[item.day for item in self.day.all()]}'
    
class Generalsettings(Basic):
    fiscalyear_month = models.CharField(max_length=20, choices=CHOICE.MONTHS)
    weekly_holiday = models.ForeignKey(Weeklyholiday, on_delete=models.CASCADE)
    workingday_starts_at = models.TimeField()
    holiday_as_workingday = models.BooleanField(default=False)
    consecutive_days_late_attendance_to_fine = models.IntegerField(default=3)
    consecutive_late_attendance_to_fine = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=100)
    fraction_of_daily_salary_for_halfday = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    max_working_hours_against_timesheet = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(24)], default=8)
    consider_attendance_on_holidays = models.CharField(max_length=15, choices=CHOICE.ATTENDANCE_OVERTIME)
    allow_overtime = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.id} - {self.fiscalyear_month}'
