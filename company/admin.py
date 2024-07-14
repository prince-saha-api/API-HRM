from django.contrib import admin
from company import models

admin.site.register([
    models.Basicinformation,
    models.Companymobilenumber,
    models.Companyemail,
    models.Company,
    models.Bankinformation,
])