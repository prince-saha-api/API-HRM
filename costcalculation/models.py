from django.db import models
from django.core.exceptions import ValidationError
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from django.core.validators import MinValueValidator, MaxValueValidator

class Costtitle(Basic):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.title} - {self.code}'
    def save(self, *args, **kwargs):
        if self.code == None:
            self.code = ghelp().generateUniqueCode('CSTTL')
        super().save(*args, **kwargs)

class Subcosttitle(Basic):
    cost_title = models.ForeignKey(Costtitle, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    range_start = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    range_end = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    cost = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f'{self.title} - {self.code}'
    def clean(self):
        errors=[]
        subcosttitle = Subcosttitle.objects.filter(code=self.cost_title.code).order_by('-id').first()
        if subcosttitle:
            if subcosttitle.range_end > 0:
                if subcosttitle.range_end + 1 != self.range_start:
                    errors.append(f'range_start should be {subcosttitle.range_end + 1}')
                if self.range_start >= self.range_end:
                    errors.append(f'range_start < range_end')
            else: errors.append(f'previous range_end can\'t be zero!')
        if errors: raise ValidationError(errors)
    def save(self, *args, **kwargs):
        self.code = self.cost_title.code
        super().save(*args, **kwargs)