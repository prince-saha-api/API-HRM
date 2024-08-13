from django.contrib import admin
from notice import models

admin.site.register([
    models.Noticeboard,
    models.Noticeboardcompany,
    models.Noticeboardbranch,
    models.Noticeboarddepartment,
    models.Noticeboardemployee
])