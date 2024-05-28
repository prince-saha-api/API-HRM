from django.db import models
from helps.abstract.abstractclass import Basic, Createdinfoint
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import User, Ethnicgroup
from helps.choice import common as CHOICE

# Create your models here.

class Payrollearning(Basic):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_taxable = models.BooleanField(default=True)
    depends_on_attendance = models.BooleanField(default=True)
    amount_type = models.CharField(max_length=20, choices=CHOICE.AMOUNT_TYPE, blank=True, null=True)
    amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollearningone')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollearningtwo')
    
    def __str__(self):
        return f'{self.title} -- {self.amount_type}'
    
class Payrollearningassign(Basic):
    payrollearning  = models.ForeignKey(Payrollearning, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.payrollearning} -- {self.user}'
    
class Payrolldeduction(Basic):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    exempted_for_tax = models.BooleanField(default=False)
    depends_on_attendance = models.BooleanField(default=False)
    amount_type = models.CharField(max_length=20, choices=CHOICE.AMOUNT_TYPE, blank=True, null=True)
    amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrolldeductionone')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrolldeductiontwo')
    
    def __str__(self):
        return f'{self.title} -- {self.amount_type}'
    
class Payrolldeductionassign(Basic):
    payrolldeduction  = models.ForeignKey(Payrolldeduction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.payrolldeduction} -- {self.user}'
    
class Payrolltax(Basic):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    min_income = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    max_income = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    ethnicgroup = models.ForeignKey(Ethnicgroup, on_delete=models.SET_NULL, blank=True, null=True)
    percentage  = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrolltaxone')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrolltaxtwo')
    
    def __str__(self):
        return f'{self.title} -- {self.employee_group_id}'
    