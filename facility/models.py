from django.db import models
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic

class Facility(Basic):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.code} -- {self.title}'