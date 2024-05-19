from django.contrib import admin
from workingshift import models

admin.site.register([
    models.Globalbuffertimesettings,
    models.Globalbuffertime,
    models.Workingshift
])
