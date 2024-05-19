from django.contrib import admin
from hrm_settings import models

admin.site.register([
    models.Fiscalyear,
    models.Latefineforfewdays,
    models.Workingminutesperday,
    models.FixedWorkingdaysinamonth,
])