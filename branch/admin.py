from django.contrib import admin
from branch import models

admin.site.register([
    models.Operatinghour,
    models.Branch,
    models.Branchphonenumber,
    models.Branchemail,
    models.Contactperson
])
