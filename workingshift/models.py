from django.db import models
from datetime import date, datetime
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import pytz
from hrm.settings import TIME_ZONE

tzInfo = pytz.timezone(TIME_ZONE)

class Globalbuffertimesettings(Basic):
    will_all_the_row_delete = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.will_all_the_row_delete}'
    def save(self, *args, **kwargs):
        Globalbuffertimesettings.objects.all().delete()
        super().save(*args, **kwargs)

class Globalbuffertime(Basic):
    buffer_time_for_enter_minutes = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    buffer_time_for_leave_minutes = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f'{self.id} -- {self.buffer_time_for_enter_minutes} -- {self.buffer_time_for_leave_minutes} -- {self.active}'

    def save(self, *args, **kwargs):
        if self.is_active:
            globalbuffertimesettings = Globalbuffertimesettings.objects.all()
            if globalbuffertimesettings:
                if globalbuffertimesettings[0].will_all_the_row_delete:
                    Globalbuffertime.objects.all().delete()
                else:
                    Globalbuffertime.objects.all().update(is_active=False)
            else:
                Globalbuffertime.objects.all().update(is_active=False)
        super().save(*args, **kwargs)