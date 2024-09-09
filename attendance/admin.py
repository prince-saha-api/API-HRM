from django.contrib import admin
from attendance import models

admin.site.register([
    models.Attendance,
    models.Attendancestatus,
    models.Devicelogs,
    models.Remotelogs,
    models.Requestremoteattendance,
    models.Requestmanualattendance,
])
