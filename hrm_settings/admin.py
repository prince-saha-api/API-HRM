from django.contrib import admin
from hrm_settings import models

admin.site.register([
    models.Fiscalyear,
    models.Weekdays,
    models.Weeklyholiday,
    models.Generalsettings
])