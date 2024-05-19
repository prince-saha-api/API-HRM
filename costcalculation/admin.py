from django.contrib import admin
from costcalculation import models


admin.site.register([
    models.Costtitle,
    models.Subcosttitle
])
