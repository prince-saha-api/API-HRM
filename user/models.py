from datetime import timedelta
from django.db import models
from django.db.models import JSONField
from helps.model.modelhelps import setSettings
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic, Timedetailscode
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from contribution import models as CNTRIB
from helps.choice import common as CHOICE
from django.db.models import Sum
from device.models import Device, Devicegroup
from helps.validators.common import validate_phone_number, validate_office_id
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

def generate_unique_code():
    return ghelp().getUniqueCodePattern()

def getyear():
    return ghelp().getYear()

def getmonth():
    return ghelp().getMonth()

def uploadphoto(instance, filename):
    return "files/{user}/profilepic/{uniquecode}uniquevalue{filename}".format(user=instance.username, uniquecode=generate_unique_code(), filename=filename)

def uploaddocs(instance, filename):
    if '.pdf' in filename:
        return "files/{user}/userdocs/pdf/{uniquecode}uniquevalue{filename}".format(user=instance.user.username, uniquecode=generate_unique_code(), filename=filename)
    elif '.csv' in filename:
        return "files/{user}/userdocs/csv/{uniquecode}uniquevalue{filename}".format(user=instance.user.username, uniquecode=generate_unique_code(), filename=filename)
    elif '.zip' in filename:
        return "files/{user}/userdocs/zip/{uniquecode}uniquevalue{filename}".format(user=instance.user.username, uniquecode=generate_unique_code(), filename=filename)
    elif '.jpg' in filename or '.jpeg' in filename or '.png' in filename or '.PNG' in filename or '.gif':
        return "files/{user}/userdocs/image/{uniquecode}uniquevalue{filename}".format(user=instance.user.username, uniquecode=generate_unique_code(), filename=filename)
    else:
        return "files/{user}/userdocs/others/{uniquecode}uniquevalue{filename}".format(user=instance.user.username, uniquecode=generate_unique_code(), filename=filename)


class Responsibility(Basic):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.title} - {self.is_active}'
class Requiredskill(Basic):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.title} - {self.is_active}'

class Designation(Basic):
    name = models.CharField(max_length=50, unique=True)
    responsibility = models.ManyToManyField(Responsibility)
    required_skill = models.ManyToManyField(Requiredskill)

    def __str__(self):
        return f'{self.name} - {self.is_active}'
    
    
class Permission(Basic):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name} - {self.is_active}'
    
class Role(Basic):
    name = models.CharField(max_length=50, unique=True)
    permission = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f'{self.name} - {self.is_active}'
    
class Grade(Basic):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name} - {self.is_active}'
    
class Shift(Basic):
    name = models.CharField(max_length=50, unique=True)
    in_time = models.TimeField()
    out_time = models.TimeField()
    late_tolerance_time = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    created_by = models.IntegerField()
    updated_by = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['in_time', 'out_time'], name='Shift_in_time_out_time')]

    def __str__(self):
        return f'{self.name} -- {self.code}'
    
class Religion(Basic):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

class User(AbstractUser, Timedetailscode):
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True)
    role = models.ManyToManyField(Role, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, blank=True, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=25, choices=CHOICE.BLOOD_GROUP, blank=True, null=True)
    fathers_name = models.CharField(max_length=150, blank=True, null=True)
    mothers_name = models.CharField(max_length=150, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=CHOICE.MARITAL_STATUS, default=CHOICE.MARITAL_STATUS[0][1])
    gender = models.CharField(max_length=10, choices=CHOICE.GENDER, blank=True, null=True)
    spouse_name = models.CharField(max_length=150, blank=True, null=True)
    present_address = models.OneToOneField(CNTRIB.Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='userseven')
    permanent_address = models.OneToOneField(CNTRIB.Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='usereight')
    religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    personal_phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    nid_passport_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    tin_no = models.CharField(max_length=50, unique=True, blank=True, null=True)

    
    bank_account = models.OneToOneField(CNTRIB.Bankaccount, on_delete=models.SET_NULL, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    official_id = models.CharField(max_length=11, validators=[validate_office_id], unique=True, blank=True, null=True)
    official_email = models.EmailField(blank=True)
    official_phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    employee_type = models.CharField(max_length=30, choices=CHOICE.EMPLOYEE_TYPE, blank=True, null=True)
    allow_overtime = models.BooleanField(default=False)
    allow_remote_checkin = models.BooleanField(default=False)
    job_status = models.CharField(max_length=30, choices=CHOICE.JOB_STATUS, default=CHOICE.JOB_STATUS[0][1])
    official_note = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to=uploadphoto, blank=True, null=True)
    rfid = models.CharField(max_length=50, unique=True, blank=True, null=True)


    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userone')
    expense_approver = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='usertwo')
    leave_approver = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userthree')
    shift_request_approver = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userfour')
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userfive')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='usersix')


    def __str__(self):
        return f'{self.username} - {self.is_active}'
    
class Employeecontact(Basic):
    name =  models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField(validators=[MinValueValidator(10)], blank=True, null=True)
    phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    email = models.EmailField(blank=True)
    address = models.OneToOneField(CNTRIB.Address, on_delete=models.SET_NULL, blank=True, null=True)
    relation = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.relation}'
    

class Employeedocs(Basic):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to=uploaddocs, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'
    
class Employeeacademichistory(Basic):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board_institute_name = models.CharField(max_length=150)
    certification = models.CharField(max_length=150)
    level = models.CharField(max_length=50)
    score_grade = models.CharField(max_length=4)
    year_of_passing = models.IntegerField(validators=[MinValueValidator(1950)])

    def __str__(self):
        return f'{self.board_institute_name}'
    
class Employeeexperiencehistory(Basic):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f'{self.company_name}'

class Ethnicgroup(Basic):
    name = models.CharField(max_length=50, unique=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'

class Groupofdevicegroup(Basic):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    devicegroup = models.ManyToManyField(Devicegroup, blank=True)

    def __str__(self):
        return f'{self.user.username}'

class Shiftchangelog(Basic):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shiftchangelogone')
    decision_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='shiftchangelogtwo')
    
    previouseshift = models.ForeignKey(Shift, on_delete=models.SET_NULL, blank=True, null=True, related_name='shiftchangelogthree')
    newshift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='shiftchangelogfour')
    
    date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'date'], name='Shiftchangelog_user_date')]

    def __str__(self):
        return f'{self.code} -- {self.user.username} -- {self.newshift.name}'

class Shiftchangerequest(Basic):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shiftchangerequestone')
    reqshiftid = models.ForeignKey(Shift, on_delete=models.CASCADE)
    fromdate = models.DateField()
    todate = models.DateField()
    reqnote = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICE.STATUS, default=CHOICE.STATUS[0][1])
    adminnote = models.TextField(blank=True, null=True)

    decision_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='shiftchangerequesttwo')

    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    def __str__(self):
        return f'{self.code} -- {self.user.username}'
    
    def clean(self):
        errors=[]
        if self.user:
            if self.user.shift:
                if self.reqshiftid:
                    if self.user.shift.name == self.reqshiftid.name: errors.append('Your requested shift is already assigned to you!')
        if errors: raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.status == CHOICE.STATUS[1][1]:
            daycount = (self.todate - self.fromdate).days + 1
            for day in range(daycount):
                date = self.fromdate + timedelta(day)
                try:
                    shiftchangelog = Shiftchangelog()

                    shiftchangelog.user = self.user
                    if self.decision_by: shiftchangelog.decision_by = self.decision_by
                    if self.user.shift: shiftchangelog.previouseshift = self.user.shift
                    shiftchangelog.newshift = self.reqshiftid
                    shiftchangelog.date = date
                    if self.reqnote: shiftchangelog.reason = self.reqnote
                    shiftchangelog.save()
                except: pass
        else:
            daycount = (self.todate - self.fromdate).days + 1
            for day in range(daycount):
                date = self.fromdate + timedelta(day)
                shiftchangelog = Shiftchangelog.objects.filter(date=date, user=self.user)
                if shiftchangelog.exists(): shiftchangelog.delete()

        super().save(*args, **kwargs)

class Salaryallocation(Basic):
    name = models.CharField(max_length=100, unique=True)
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)

    def __str__(self):
        return f'{self.name} - {self.percentage}'
    def clean(self):
        errors=[]
        percentage = Salaryallocation.objects.all().aggregate(Sum('percentage'))['percentage__sum']
        if percentage is not None:
            if percentage+self.percentage>100:
                errors.append(f'{self.percentage} will exceed 100%!')
        if errors: raise ValidationError(errors)

class Perdaysalary(Basic):
    calculation_based_on = models.ForeignKey(Salaryallocation, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f'{self.calculation_based_on}'
    # def save(self, *args, **kwargs):
    #     if self.id is not None: Perdaysalary.objects.exclude().delete()
    #     else: Perdaysalary.objects.all().delete()
    #     super().save(*args, **kwargs)

# class Updatesalaryconfig(Basic):
#     backup_will_be_deleted_after_nth_records = models.IntegerField(validators=[MinValueValidator(1)], default=5)
#     def __str__(self):
#         return f'{self.backup_will_be_deleted_after_nth_records}'
#     def save(self, *args, **kwargs):
#         if self.id is not None: Updatesalaryconfig.objects.exclude().delete()
#         else: Updatesalaryconfig.objects.all().delete()
#         super().save(*args, **kwargs)
class Salary(Basic):
    gross_salary = models.FloatField(validators=[MinValueValidator(0)])
    dummy_salary = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    active_dummy_salary = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.code} - {self.gross_salary} - {self.dummy_salary}'
    # def save(self, *args, **kwargs):
    #     self.code = setSettings(self.id, self.code, 'SLRYI', Updatesalaryconfig, Updatesalary)

    #     update_info = {
    #         'gross_salary': self.gross_salary,
    #         'dummy_salary': self.dummy_salary,
    #         'custom_user': self.user.id,
    #         'updated_by': self.created_by,
    #         'active_dummy_salary': self.active_dummy_salary}
    #     if self.id != None: update_info['updated_by']=self.updated_by
    #     Updatesalary.objects.create(code=self.code, update_info=update_info)
    #     super().save(*args, **kwargs)

class Employeeincrementrecord(Basic):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    effective_from = models.DateField()
    increment_on = models.CharField(max_length=50, blank=True, null=True)
    prev_salary = models.FloatField(validators=[MinValueValidator(0)])
    new_salary = models.FloatField(validators=[MinValueValidator(0)])
    increment_amount = models.FloatField(validators=[MinValueValidator(0)])
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    bank_amount = models.FloatField(validators=[MinValueValidator(0)])
    cash_amount = models.FloatField(validators=[MinValueValidator(0)])
    status = models.CharField(max_length=50, choices=(('Joining', 'Joining'), ('Increment', 'Increment'), ('Promotion', 'Promotion')), blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.percentage}'
    
# class Updatesalary(models.Model)2
#     update_info = JSONField(default=dict)
#     code = models.CharField(max_length=30)
#     def __str__(self):
#         return f'{self.code}'


# class Updatepaymentrecordconfig(Basic):
#     backup_will_be_deleted_after_nth_records = models.IntegerField(validators=[MinValueValidator(1)], default=5)
#     def __str__(self):
#         return f'{self.backup_will_be_deleted_after_nth_records}'
#     def save(self, *args, **kwargs):
#         if self.id is not None: Updatepaymentrecordconfig.objects.exclude().delete()
#         else: Updatepaymentrecordconfig.objects.all().delete()
#         super().save(*args, **kwargs)

class Paymentrecord(Basic):
    salary_year = models.IntegerField()
    salary_month = models.CharField(max_length=20, choices=CHOICE.MONTHS)
    salary_gross = models.FloatField(validators=[MinValueValidator(0)])
    salary_paid = models.FloatField(validators=[MinValueValidator(0)])
    salary_deduction = models.FloatField(validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    details = JSONField(default=dict)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['salary_year', 'salary_month', 'user'], name='Paymentrecord_salary_year_salary_month_user')]
    def __str__(self):
        return f'{self.user.username}'
    # def save(self, *args, **kwargs):
    #     self.code = setSettings(self.id, self.code, 'SLRYR', Updatepaymentrecordconfig, Updatepaymentrecord)

    #     update_info = {
    #         'salary_year': self.salary_year,
    #         'salary_month': self.salary_month,
    #         'salary_gross': self.salary_gross,
    #         'salary_paid': self.salary_paid,
    #         'salary_deduction': self.salary_deduction,

    #         'user': self.user.id,
    #         'created_by': self.created_by,
    #         'updated_by': self.created_by,
    #         }
    #     if self.id != None: update_info['updated_by']=self.updated_by
    #     Updatepaymentrecord.objects.create(code=self.code, update_info=update_info)
    #     super().save(*args, **kwargs)

# class Updatepaymentrecord(models.Model):
#     update_info = JSONField(default=dict)

#     code = models.CharField(max_length=30)
#     def __str__(self):
#         return f'{self.code}'

# class Bonusconfig(Basic):
#     calculation_based_on = models.ForeignKey(Salaryallocation, on_delete=models.SET_NULL, blank=True, null=True)
#     def __str__(self):
#         return f'{self.calculation_based_on.name}'
#     def save(self, *args, **kwargs):
#         if self.id is not None: Bonusconfig.objects.exclude().delete()
#         else: Bonusconfig.objects.all().delete()
#         super().save(*args, **kwargs)
    
class Bonus(Basic):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=15, choices=CHOICE.CALCULATION_TYPE, default=CHOICE.CALCULATION_TYPE[0][1])
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    amount = models.FloatField(validators=[MinValueValidator(0)], default=0, blank=True, null=True)
    dummy_amount = models.FloatField(validators=[MinValueValidator(0)], default=0, blank=True, null=True)
    # active_dummy_amount = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True)
    year = models.IntegerField(default=getyear, validators=[MinValueValidator(2020)])
    month = models.CharField(max_length=20, choices=CHOICE.MONTHS, default=CHOICE.MONTHS[getmonth()-1][1])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonusone')
    hand_over_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='bonustwo')

    def __str__(self):
        return f'{self.title} - {self.amount} - {self.dummy_amount}'
    # def clean(self):
    #     errors=[]
    #     if self.type == CHOICE.CALCULATION_TYPE[0][1]:
    #         bonusconfig = Bonusconfig.objects.all()
    #         if not bonusconfig: errors.append('please set Bonusconfig first!')
    #         if self.user:
    #             if ghelp().getGrossSalary(self.user, Salary) == None: errors.append('Bonus will be calculated based on salary but salaryinfo is missing!')
    #         else: errors.append('please select CustomUser!')
    #     if not self.user:
    #         if 'please select CustomUser!' not in errors: errors.append('please select CustomUser!')
    #     if errors: raise ValidationError(errors)
    # def save(self, *args, **kwargs):
    #     if self.type == CHOICE.CALCULATION_TYPE[0][1]:
    #         salary = ghelp().getGrossSalary(self.user, Salary)
    #         if salary != None:
    #             portionofsalary = ghelp().getOnePortionOfSalaryAccordingToConfig(salary, Bonusconfig)
    #             if portionofsalary != None: self.amount = (portionofsalary*self.percentage)/100
    #     elif self.type == CHOICE.CALCULATION_TYPE[1][1]: self.percentage = 0

    #     if self.id == None: self.code = ghelp().generateUniqueCode('BONUS')
    #     super().save(*args, **kwargs)
    
class Mobilenumber(Basic):
    phone_number = models.CharField(max_length=14, validators=[validate_phone_number], unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.phone_number} - {self.user.username}'