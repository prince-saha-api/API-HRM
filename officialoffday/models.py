from django.db import models
from helps.choice.common import DAYS
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic


# class Offday(Basic):
#     day = models.CharField(max_length=10, choices=DAYS, unique=True)

#     def __str__(self):
#         return f'{self.day} {Offday.objects.filter(is_active=True).count()}'