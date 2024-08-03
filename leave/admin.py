from django.contrib import admin
from leave import models

admin.site.register([
    models.Holiday,
    models.Leavepolicy,
    models.Leavepolicyassign,
    models.Approvedleave,
    models.Leavesummary,
    models.Leaverequest
])