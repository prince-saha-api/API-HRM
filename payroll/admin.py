from django.contrib import admin
from payroll import models

admin.site.register([
    models.Payrollearning,
    models.Payrollearningassign,
    models.Payrolldeduction,
    models.Payrolldeductionassign,
    models.Payrolltax,
])
