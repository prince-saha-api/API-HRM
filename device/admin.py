from django.contrib import admin
from device import models

admin.site.register([
    models.Device,
    models.Group,
    models.Devicegroup,
])
