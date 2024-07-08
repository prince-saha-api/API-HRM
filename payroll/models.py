from django.db import models
from helps.abstract.abstractclass import Basic, Createdinfoint
from django.core.validators import MinValueValidator, MaxValueValidator
from user import models as MODELS_USER
from hrm_settings import models as MODELS_SETT
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN
from department import models as MODELS_DEPA
from contribution import models as MODELS_CONT
from helps.choice import common as CHOICE

class Payrollearning(Basic):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_taxable = models.BooleanField(default=True)
    depends_on_attendance = models.BooleanField(default=False)
    amount_type = models.CharField(max_length=20, choices=CHOICE.AMOUNT_TYPE, default=CHOICE.AMOUNT_TYPE[0][1])
    amount = models.FloatField(validators=[MinValueValidator(0)])

    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollearningone')
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollearningtwo')
    
    def __str__(self):
        return f'{self.title} -- {self.amount_type}'
    
class Payrollearningassign(Basic):
    payrollearning  = models.ForeignKey(Payrollearning, on_delete=models.CASCADE)
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.payrollearning} -- {self.user}'

class Payrolldeduction(Basic):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    exempted_for_tax = models.BooleanField(default=False)
    depends_on_attendance = models.BooleanField(default=False)
    amount_type = models.CharField(max_length=20, choices=CHOICE.AMOUNT_TYPE, default=CHOICE.AMOUNT_TYPE[0][1])
    amount = models.FloatField(validators=[MinValueValidator(0)])
    
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrolldeductionone')
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrolldeductiontwo')
    
    def __str__(self):
        return f'{self.title} -- {self.amount_type}'
    
class Payrolldeductionassign(Basic):
    payrolldeduction  = models.ForeignKey(Payrolldeduction, on_delete=models.CASCADE)
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.payrolldeduction} -- {self.user}'

class Payrolltax(Basic):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    min_income = models.FloatField(validators=[MinValueValidator(0)])
    max_income = models.FloatField(validators=[MinValueValidator(0)])
    ethnicgroup = models.ForeignKey(MODELS_USER.Ethnicgroup, on_delete=models.SET_NULL, blank=True, null=True)
    percentage  = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrolltaxone')
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrolltaxtwo')
    
    def __str__(self):
        return f'{self.title} -- {self.ethnicgroup}'
    
# class Payrollloanmaster(Basic):
#     title = models.CharField(max_length=100)
#     user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='payrollloanmasterone')
#     loan_type = models.CharField(max_length=20, choices=CHOICE.LOAN_TYPE, default=CHOICE.LOAN_TYPE[1][1])
#     amount = models.FloatField(validators=[MinValueValidator(0)])
#     disbursment_date = models.DateField(blank=True, null=True)
#     adjustment_type = models.CharField(max_length=20, choices=CHOICE.ADJUSTMENT_TYPE, default=CHOICE.ADJUSTMENT_TYPE[0][1])
#     no_of_installment = models.IntegerField()
#     installment_left = models.IntegerField(blank=True, null=True)
#     installment_amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True) # can't be blank, auto calculation 
#     installment_start_from = models.DateField(blank=True, null=True)
#     repayment_completion_date = models.DateField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)

#     updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollloanmastertwo')
#     created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollloanmasterthree')
    
#     def __str__(self):
#         return f'{self.title} -- {self.loan_type}'
    
# class Payrollloanrequest(Basic):
#     title = models.CharField(max_length=100)
#     user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='Payrollloanrequestone')
#     loan_type = models.CharField(max_length=20, choices=CHOICE.LOAN_TYPE, default=CHOICE.LOAN_TYPE[1][1])
#     amount = models.FloatField(validators=[MinValueValidator(0)])
#     adjustment_type = models.CharField(max_length=20, choices=CHOICE.ADJUSTMENT_TYPE, blank=True, null=True)
#     no_of_installment = models.IntegerField()
#     reason = models.TextField()
#     status = models.CharField(max_length=20, choices=CHOICE.STATUS, default=CHOICE.STATUS[0][1])
#     decision_by = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='payrollloanrequesttwo')

#     updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollloanrequestthree')
#     created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollloanrequestfour')
    
#     def __str__(self):
#         return f'{self.title} -- {self.loan_type}'
    
# class Payrollloaninstallments(Basic):
#     payrollloanrequest = models.ForeignKey(Payrollloanrequest, on_delete=models.CASCADE)
#     receiving_date = models.DateField()
    
#     updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollloaninstallmentsone')
#     created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollloaninstallmentstwo')
    
#     def __str__(self):
#         return f'{self.payrollloanrequest} -- {self.receiving_date}'
    
# class Payrollincentivebonus(Basic):
#     title = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     amount_type = models.CharField(max_length=20, choices=CHOICE.AMOUNT_TYPE, blank=True, null=True)
#     amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     issuing_date = models.DateField()
#     disbursment_date = models.DateField()
#     is_taxable = models.BooleanField(default=True)

#     updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollincentivebonusone')
#     created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollincentivebonustwo')
    
#     def __str__(self):
#         return f'{self.title} -- {self.amount_type}'
    
# class Payrollincentivebonusallocation(Basic):
#     payrollincentivebonus = models.ForeignKey(Payrollincentivebonus, on_delete=models.CASCADE)
#     user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE)
#     amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     taxable_amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     status = models.CharField(max_length=20, choices=CHOICE.STATUS, blank=True, null=True)
 
#     def __str__(self):
#         return f'{self.payrollincentivebonus} -- {self.status}'

# class Payrollemployeeincomesummery(Basic):
#     user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE)
#     fiscalyear = models.ForeignKey(MODELS_SETT.Fiscalyear, on_delete=models.CASCADE)
#     no_of_month = models.IntegerField()
#     gross_income  = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     total_deduction = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     net_income = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     income_tax = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
 
#     def __str__(self):
#         return f'{self.gross_income} -- {self.user}'
    
# class Payrollentry(Basic):
#     title = models.CharField(max_length=100)
#     posting_date = models.DateField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     company = models.ForeignKey(MODELS_COMP.Company, on_delete=models.CASCADE)
#     branch = models.ForeignKey(MODELS_BRAN.Branch, on_delete=models.CASCADE)
#     department = models.ForeignKey(MODELS_DEPA.Department, on_delete=models.CASCADE)
#     grade = models.ForeignKey(MODELS_USER.Grade, on_delete=models.CASCADE)
#     designation = models.ForeignKey(MODELS_USER.Designation, on_delete=models.CASCADE)
#     bankaccount = models.ForeignKey(MODELS_CONT.Bankaccount, on_delete=models.CASCADE)
#     gross_payable  = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     total_deduction = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     total_tax = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     net_payable = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

#     updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollentryone')
#     created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollentrytwo')
    
#     def __str__(self):
#         return f'{self.title} -- {self.posting_date}'

# class Payrollsalaryslipmaster(Basic):
#     payrollentry = models.ForeignKey(Payrollentry, on_delete=models.CASCADE, blank=True, null=True, related_name='payrollsalaryslipmasterone')
#     user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='payrollsalaryslipmastertwo')
#     posting_date = models.DateField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     disburs_date = models.DateField()
#     total_earning = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     total_deduction = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     net_payable = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     status = models.CharField(max_length=20, choices=CHOICE.STATUS, blank=True, null=True)

#     updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollsalaryslipmasterthree')
#     created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='payrollsalaryslipmasterfour')
    
#     def __str__(self):
#         return f'{self.posting_date} -- {self.net_payable}'

# class Payrollsalaryslipentity(Basic):
#     payrollsalaryslipmaster = models.ForeignKey(Payrollsalaryslipmaster, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     slug = models.CharField(max_length=100, blank=True, null=True)
#     earn_deduct = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
#     amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

#     def __str__(self):
#         return f'{self.name} -- {self.amount}'
