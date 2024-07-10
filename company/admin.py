from django.contrib import admin
from company import models

admin.site.register([
    models.Companytype,
    models.Basicinformation,
    models.Companymobilenumber,
    models.Companyemail,
    models.Company,
    models.Bankinformation,
])