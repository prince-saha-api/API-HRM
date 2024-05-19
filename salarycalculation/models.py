# from django.db import models
# from django.db.models import Sum
# from django.db.models import JSONField
# from customuser.models import User
# from helps.choice.common import CALCULATION_TYPE
# from helps.common.generic import Generichelps as ghelp
# from helps.abstract.abstractclass import Basic
# from helps.model.modelhelps import setSettings
# from django.core.exceptions import ValidationError
# from django.core.validators import MinValueValidator, MaxValueValidator

# class Updatesalaryinfoconfig(Basic):
#     backup_will_be_deleted_after_nth_records = models.IntegerField(validators=[MinValueValidator(1)], default=5)
#     def __str__(self):
#         return f'{self.backup_will_be_deleted_after_nth_records}'
#     def save(self, *args, **kwargs):
#         if self.id is not None: Updatesalaryinfoconfig.objects.exclude().delete()
#         else: Updatesalaryinfoconfig.objects.all().delete()
#         super().save(*args, **kwargs)

# class Salaryinfo(Basic):
#     gross_salary = models.FloatField(validators=[MinValueValidator(0)])
#     dummy_salary = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     custom_user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_by = models.IntegerField()
#     updated_by = models.IntegerField()
#     active_dummy_salary = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.code} - {self.gross_salary} - {self.dummy_salary}'
#     def save(self, *args, **kwargs):
#         self.code = setSettings(self.id, self.code, 'SLRYI', Updatesalaryinfoconfig, Updatesalaryinfo)

#         update_info = {
#             'gross_salary': self.gross_salary, 
#             'dummy_salary': self.dummy_salary, 
#             'custom_user': self.custom_user.id, 
#             'updated_by': self.created_by, 
#             'active_dummy_salary': self.active_dummy_salary}
#         if self.id != None: update_info['updated_by']=self.updated_by
#         Updatesalaryinfo.objects.create(code=self.code, update_info=update_info)
#         super().save(*args, **kwargs)

# class Updatesalaryinfo(models.Model):
#     code = models.CharField(max_length=30)
#     update_info = JSONField(default=dict)

#     def __str__(self):
#         return f'{self.code}'