from datetime import timedelta
from django.db import models
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic, Timedetailscode
from django.core.validators import MinValueValidator, MaxValueValidator
from contribution import models as CNTRIB
from helps.choice import common as CHOICE
from django.db.models import Sum
from helps.validators.common import validate_phone_number, validate_office_id
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
# from company import models as MODELS_COMP
# from branch import models as MODELS_BRAN
# from department import models as MODELS_DEPA

def generate_unique_code():
    return ghelp().getUniqueCodePattern()

def getyear():
    return ghelp().getYear()

def getmonth():
    return ghelp().getMonth()

def uploadphoto(instance, filename):
    return "user/{unique}/profilepic/{uniquecode}uniquevalue{filename}".format(unique=instance.uniqueid, uniquecode=generate_unique_code(), filename=filename)

def uploaddocs(instance, filename):
    if '.pdf' in filename:
        return "user/{unique}/userdocs/pdf/{uniquecode}uniquevalue{filename}".format(unique=instance.user.uniqueid, uniquecode=generate_unique_code(), filename=filename)
    elif '.csv' in filename:
        return "user/{unique}/userdocs/csv/{uniquecode}uniquevalue{filename}".format(unique=instance.user.uniqueid, uniquecode=generate_unique_code(), filename=filename)
    elif '.zip' in filename:
        return "user/{unique}/userdocs/zip/{uniquecode}uniquevalue{filename}".format(unique=instance.user.uniqueid, uniquecode=generate_unique_code(), filename=filename)
    elif '.jpg' in filename or '.jpeg' in filename or '.png' in filename or '.PNG' in filename or '.gif':
        return "user/{unique}/userdocs/image/{uniquecode}uniquevalue{filename}".format(unique=instance.user.uniqueid, uniquecode=generate_unique_code(), filename=filename)
    else:
        return "user/{unique}/userdocs/others/{uniquecode}uniquevalue{filename}".format(unique=instance.user.uniqueid, uniquecode=generate_unique_code(), filename=filename)

class Responsibility(Basic):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.title} - {self.is_active}'


class Requiredskill(Basic):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.title} - {self.is_active}'  


class Permission(Basic):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.id} - {self.name} - {self.is_active}'


class Rolepermission(Basic):
    name = models.CharField(max_length=50, unique=True)
    permission = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f'{self.name} - {self.is_active}'


class Grade(Basic):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name} - {self.is_active}'
    
class Designation(Basic):
    name = models.CharField(max_length=50, unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, blank=True, null=True)
    responsibility = models.ManyToManyField(Responsibility, blank=True)
    required_skill = models.ManyToManyField(Requiredskill, blank=True)

    def __str__(self):
        return f'{self.name} - {self.is_active}'
    
class Shift(Basic):
    name = models.CharField(max_length=50, unique=True)
    in_time = models.TimeField()
    out_time = models.TimeField()
    late_tolerance_time = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['in_time', 'out_time'], name='Shift_in_time_out_time')]

    def __str__(self):
        return f'{self.name} -- {self.code}'
    
class Religion(Basic):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

class User(AbstractUser, Timedetailscode):
    uniqueid = models.CharField(max_length=18, unique=True, default=generate_unique_code)

    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True) # Mandatory
    # company = models.ForeignKey(MODELS_COMP.Company, on_delete=models.SET_NULL, blank=True, null=True)
    # branch = models.ForeignKey(MODELS_BRAN.Branch, on_delete=models.SET_NULL, blank=True, null=True)
    ###
    dob = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=25, choices=CHOICE.BLOOD_GROUP, blank=True, null=True)
    fathers_name = models.CharField(max_length=150, blank=True, null=True)
    mothers_name = models.CharField(max_length=150, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=CHOICE.MARITAL_STATUS, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=CHOICE.GENDER, blank=True, null=True)
    spouse_name = models.CharField(max_length=150, blank=True, null=True)
    ###
    #####
    religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    personal_email = models.EmailField(blank=True)
    personal_phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    nid_passport_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    tin_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    bank_account = models.OneToOneField(CNTRIB.Bankaccount, on_delete=models.SET_NULL, blank=True, null=True)
    #####
    ######
    official_id = models.CharField(max_length=11, validators=[validate_office_id], unique=True, blank=True, null=True)
    official_email = models.EmailField(blank=True)
    official_phone = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    employee_type = models.CharField(max_length=30, choices=CHOICE.EMPLOYEE_TYPE, blank=True, null=True)
    gross_salary = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    basic_salary = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    payment_in = models.CharField(max_length=50, choices=CHOICE.PAYMENT_IN, blank=True, null=True)
    #######
    #########
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userone')
    expense_approver = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='usertwo')
    leave_approver = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userthree')
    shift_request_approver = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userfour')
    #########
    role_permission = models.ManyToManyField(Rolepermission, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, blank=True, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, blank=True, null=True)
    ###
    present_address = models.OneToOneField(CNTRIB.Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='userseven')
    permanent_address = models.OneToOneField(CNTRIB.Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='usereight')
    #####
    dummy_salary = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    #######
    allow_overtime = models.BooleanField(default=False)
    allow_remote_checkin = models.BooleanField(default=False)
    active_dummy_salary = models.BooleanField(default=False)
    job_status = models.CharField(max_length=30, choices=CHOICE.JOB_STATUS, blank=True, null=True)
    official_note = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to=uploadphoto, blank=True, null=True)
    rfid = models.CharField(max_length=50, unique=True, blank=True, null=True)
    #########
    hr_password = models.CharField(max_length=550, blank=True, null=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userfive')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='usersix')

    def __str__(self):
        return f'{self.username} - {self.is_active}'
    
    def save(self, *args, **kwargs):
        if self.marital_status in [item[1] for item in CHOICE.MARITAL_STATUS if item[1] != 'Married']: self.spouse_name = ''
        super().save(*args, **kwargs)


class Employeecontact(Basic):
    name =  models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_contact')
    age = models.IntegerField(validators=[MinValueValidator(10)], blank=True, null=True)
    phone_no = models.CharField(max_length=14, validators=[validate_phone_number], unique=True, blank=True, null=True)
    email = models.EmailField(blank=True)
    address = models.OneToOneField(CNTRIB.Address, on_delete=models.SET_NULL, blank=True, null=True)
    relation = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.relation}'
    

class Employeedocs(Basic):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_docs')
    attachment = models.FileField(upload_to=uploaddocs, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'
    
class Employeeacademichistory(Basic):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_academichistory')
    board_institute_name = models.CharField(max_length=150)
    certification = models.CharField(max_length=150)
    level = models.CharField(max_length=50)
    score_grade = models.CharField(max_length=4) # Non Mandatory
    year_of_passing = models.IntegerField(validators=[MinValueValidator(1950)])

    def __str__(self):
        return f'{self.board_institute_name}'
    
class Employeeexperiencehistory(Basic):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_experiencehistory')
    company_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f'{self.company_name}'

class Ethnicgroup(Basic):
    name = models.CharField(max_length=50, unique=True)
    user = models.ManyToManyField(User, blank=True, related_name='ethnicgroup_user')

    def __str__(self):
        return f'{self.name}'


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
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='shiftchangerequestthree')
    
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

    
class Note(Basic):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_user')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    priority  = models.CharField(max_length=20, choices=CHOICE.PRIORITY)
    reminder = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='note_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='note_updated_by')
    

    def __str__(self):
        return f'{self.title} - {self.user.username}'