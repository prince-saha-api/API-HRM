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

class Workingshift(Basic):
    start_from = models.TimeField(null=True)
    end_at = models.TimeField(null=True)
    def __str__(self):
        return f'{self.id} -- {self.start_from} -- {self.end_at}'
    
    def clean(self):
        errors=[]
        globalbuffertime = Globalbuffertime.objects.filter(is_active=True)
        if globalbuffertime:
            in_buffer = globalbuffertime[0].buffer_time_for_enter_minutes
            out_buffer = globalbuffertime[0].buffer_time_for_leave_minutes

            start_from = datetime.strptime(f'{date.today()} {self.start_from}', '%Y-%d-%m %H:%M:%S')
            end_at = datetime.strptime(f'{date.today()} {self.end_at}', '%Y-%d-%m %H:%M:%S')
            diff_in_sec = int((end_at-start_from).total_seconds())
            if diff_in_sec>0:
                if not (diff_in_sec/60>in_buffer and diff_in_sec/60>out_buffer and diff_in_sec/60>in_buffer+out_buffer):
                    errors.append('Invalid in time and out time according to GlobalBufferTime!')
            else:
                errors.append('start_from > end_at')
        else:
            errors.append('Either Create a GlobalBufferTime records or active a GlobalBufferTime records!')
        if errors:
            raise ValidationError(errors)