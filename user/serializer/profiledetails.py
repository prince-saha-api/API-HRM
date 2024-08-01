from rest_framework import serializers
from user import models as MODELS_USER
from contribution import models as MODELS_CONT

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
        fields = ['id', 'first_name', 'first_name', 'official_id']


class Userserializer(serializers.ModelSerializer):
    designation=Designationserializer(many=False)
    religion=Religionserializer(many=False)
    present_address=Addressserializer(many=False)
    permanent_address=Addressserializer(many=False)
    grade=Gradeserializer(many=False)
    shift=Shiftserializer(many=False)
    bank_account=Bankaccountserializer(many=False)
    employee_contact=Employeecontactserializer(many=True)
    employee_docs=Employeedocsserializer(many=True)
    employee_academichistory=Employeeacademichistoryserializer(many=True)
    employee_experiencehistory=Employeeexperiencehistoryserializer(many=True)
    supervisor=Otheruserserializer(many=False)
    expense_approver=Otheruserserializer(many=False)
    leave_approver=Otheruserserializer(many=False)
    shift_request_approver=Otheruserserializer(many=False)
    role_permission=Rolepermissionserializer(many=True)
    class Meta:
        model = MODELS_USER.User
        # fields = '__all__'
        exclude = ('password', 'uniqueid', 'dummy_salary', 'created_by', 'updated_by')