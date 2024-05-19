from django.contrib import admin
from facility import models

admin.site.register([
    models.Facility,
])