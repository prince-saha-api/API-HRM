from django.contrib import admin
from hrm_settings import models

admin.site.register([
    models.Weekdays,
    models.Weeklyholiday,
    models.Generalsettings
])