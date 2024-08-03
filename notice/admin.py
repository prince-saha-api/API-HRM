from django.contrib import admin
from notice import models

admin.site.register([
    models.Noteboard,
    models.Noticeboardcompany,
    models.Noticeboardbranch,
    models.Noticeboarddepartment,
    models.Noticeboardemployee
])