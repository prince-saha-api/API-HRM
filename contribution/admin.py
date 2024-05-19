from django.contrib import admin
from contribution import models

admin.site.register([
    models.Address,
    models.Bankaccounttype,
    models.Bankaccount,
])