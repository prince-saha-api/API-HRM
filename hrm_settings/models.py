from django.db import models
import calendar
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from datetime import timedelta
from django.db.models import Sum
from helps.choice.common import MONTHS
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Fiscalyear(Basic):
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.from_date} - {self.to_date}'
    def save(self, *args, **kwargs):
        year = self.from_date.year
        self.to_date = self.from_date + timedelta(366 if calendar.isleap(year) else 365)
        print((self.to_date-self.from_date))
        super().save(*args, **kwargs)


class Latefineforfewdays(Basic):
    cost_in_days = models.FloatField(validators=[MinValueValidator(0)], default=0)
    consecutive = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.cost_in_days}'
    def save(self, *args, **kwargs):
        if self.id is not None: Latefineforfewdays.objects.exclude().delete()
        else: Latefineforfewdays.objects.all().delete()
        super().save(*args, **kwargs)


class Workingminutesperday(Basic):
    working_minutes_per_day = models.FloatField(validators=[MinValueValidator(0)], default=540)

    def __str__(self):
        return f'{self.working_minutes_per_day}'
    def save(self, *args, **kwargs):
        if self.id is not None: Workingminutesperday.objects.exclude().delete()
        else: Workingminutesperday.objects.all().delete()
        super().save(*args, **kwargs)

class FixedWorkingdaysinamonth(Basic):
    days = models.IntegerField(default=30)

    def __str__(self):
        return f'{self.days}'
    def save(self, *args, **kwargs):
        if self.id is not None: FixedWorkingdaysinamonth.objects.exclude().delete()
        else: FixedWorkingdaysinamonth.objects.all().delete()
        super().save(*args, **kwargs)