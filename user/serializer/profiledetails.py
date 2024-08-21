from rest_framework import serializers
from user import models as MODELS_USER
from contribution import models as MODELS_CONT
from jobrecord import models as MODELS_JOBR
from department import models as MODELS_DEPA
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN

class Permissionserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Permission
        fields = ['id', 'name']

class Rolepermissionserializer(serializers.ModelSerializer):
    permission=Permissionserializer(many=True)
    class Meta:
        model = MODELS_USER.Rolepermission
        fields = ['id', 'name', 'permission']

class Addressserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_CONT.Address
        fields = ['id', 'name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']

class Religionserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Religion
        fields = ['id', 'name']

class Gradeserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Grade
        fields = ['id', 'name']

class Shiftserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Shift
        fields = ['id', 'name', 'in_time', 'out_time', 'late_tolerance_time']

class Designationserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Designation
        fields = ['id', 'name']

class Employeecontactserializer(serializers.ModelSerializer):
    address=Addressserializer(many=False)
    class Meta:
        model = MODELS_USER.Employeecontact
        fields = ['id', 'name', 'age', 'phone_no', 'email', 'address', 'relation']

class Employeedocsserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Employeedocs
        fields = ['id', 'title', 'attachment']

class Employeeacademichistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Employeeacademichistory
        fields = ['id', 'board_institute_name', 'certification', 'level', 'score_grade', 'year_of_passing']

class Employeeexperiencehistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Employeeexperiencehistory
        fields = ['id', 'company_name', 'designation', 'address', 'from_date', 'to_date']

class Bankaccounttypeserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_CONT.Bankaccounttype
        fields = ['id', 'name']

class Bankaccountserializer(serializers.ModelSerializer):
    account_type=Bankaccounttypeserializer(many=False)
    address=Addressserializer(many=False)
    class Meta:
        model = MODELS_CONT.Bankaccount
        fields = ['id', 'bank_name', 'branch_name', 'account_type', 'account_no', 'routing_no', 'swift_bic', 'address']

class Otheruserserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.User
        fields = ['id', 'first_name', 'last_name', 'official_id', 'photo']

class Employeejobhistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_JOBR.Employeejobhistory
        exclude = ('is_active', 'code', 'created_at', 'updated_at')

class Basicinformationserializer(serializers.ModelSerializer):
    address=Addressserializer(many=False)
    class Meta:
        model = MODELS_COMP.Basicinformation
        exclude = ('is_active', 'code', 'created_at', 'updated_at')

class Companyserializer(serializers.ModelSerializer):
    basic_information=Basicinformationserializer(many=False)
    class Meta:
        model = MODELS_COMP.Company
        fields = ['id', 'basic_information']

class Branchserializer(serializers.ModelSerializer):
    company=Companyserializer(many=False)
    class Meta:
        model = MODELS_BRAN.Branch
        fields = ['id', 'name', 'company', 'description', 'email', 'phone', 'fax', 'address']

class Departmentserializer(serializers.ModelSerializer):
    address=Addressserializer(many=False)
    branch=Branchserializer(many=False)
    class Meta:
        model = MODELS_DEPA.Department
        exclude = ('manager', 'company', 'user', 'is_active', 'code', 'created_at', 'updated_at')

class Ethnicgroupserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Ethnicgroup
        fields = ['id', 'name']

class Userserializer(serializers.ModelSerializer):
    designation=Designationserializer(many=False)
    religion=Religionserializer(many=False)
    present_address=Addressserializer(many=False)
    permanent_address=Addressserializer(many=False)
    grade=Gradeserializer(many=False)
    shift=Shiftserializer(many=False)
    bank_account=Bankaccountserializer(many=False)
    departmenttwo=Departmentserializer(many=True)
    ethnicgroup_user=Ethnicgroupserializer(many=True)
    employee_contact=Employeecontactserializer(many=True)
    employee_docs=Employeedocsserializer(many=True)
    employeejobhistory_user=Employeejobhistoryserializer(many=True)
    employee_academichistory=Employeeacademichistoryserializer(many=True)
    employee_experiencehistory=Employeeexperiencehistoryserializer(many=True)
    supervisor=Otheruserserializer(many=False)
    expense_approver=Otheruserserializer(many=False)
    leave_approver=Otheruserserializer(many=False)
    shift_request_approver=Otheruserserializer(many=False)
    role_permission=Rolepermissionserializer(many=True)
    class Meta:
        model = MODELS_USER.User
        exclude = ('password', 'uniqueid', 'dummy_salary', 'created_by', 'updated_by')