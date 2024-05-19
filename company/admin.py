from django.contrib import admin
from company import models

admin.site.register([
    models.Updatecompanytypeconfig,
    models.Companytype,
    models.Updatecompanytype,
    models.Updatebasicinformationconfig,
    models.Basicinformation,
    models.Updatebasicinformation,
    models.Companymobilenumber,
    models.Companyemail,
    models.Company,
    models.Bankinformation,
])