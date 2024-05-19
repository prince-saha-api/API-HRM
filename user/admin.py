from django.contrib import admin
from user import models

admin.site.register([
    models.Responsibility,
    models.Requiredskill,
    models.Designation,
    models.Permission,
    models.Role,
    models.Grade,
    models.Religion,
    models.Shift,
    models.User,
    models.Employeecontact,
    models.Employeedocs,
    models.Employeeacademichistory,
    models.Employeeexperiencehistory,
    models.Ethnicgroup,
    models.Groupofdevicegroup,
    models.Shiftchangelog,
    models.Shiftchangerequest,
    models.Salaryallocation,
    models.Perdaysalary,
    models.Salary,
    models.Employeeincrementrecord,
    models.Paymentrecord,
    models.Bonus,
    models.Mobilenumber
])