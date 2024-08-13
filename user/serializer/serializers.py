from contribution.serializer import serializers as SRLZER_CONT
from department.serializer import serializers as SRLZER_DEPA
from rest_framework import serializers
from user import models

class Religionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Religion
        fields = '__all__'
class Gradeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = '__all__'

class Shiftserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shift
        fields = '__all__'

class Designationserializer(serializers.ModelSerializer):
    grade=Gradeserializer(many=False)
    class Meta:
        model = models.Designation
        fields = '__all__'

class Employeecontactserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employeecontact
        fields = '__all__'

class Employeedocsserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employeedocs
        fields = '__all__'

class Employeeacademichistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employeeacademichistory
        fields = '__all__'


class Employeeexperiencehistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employeeexperiencehistory
        fields = '__all__'

class Ethnicgroupserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ethnicgroup
        fields = '__all__'

class Userserializer(serializers.ModelSerializer):
    designation=Designationserializer(many=False)
    religion=Religionserializer(many=False)
    grade=Gradeserializer(many=False)
    shift=Shiftserializer(many=False)
    bank_account=SRLZER_CONT.Bankaccountserializer(many=False)
    departmenttwo=SRLZER_DEPA.Departmentserializer(many=True)
    ethnicgroup_user=Ethnicgroupserializer(many=True)
    employee_contact=Employeecontactserializer(many=True)
    employee_docs=Employeedocsserializer(many=True)
    employee_academichistory=Employeeacademichistoryserializer(many=True)
    employee_experiencehistory=Employeeexperiencehistoryserializer(many=True)
    class Meta:
        model = models.User
        fields = '__all__'

class Responsibilityserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Responsibility
        fields = '__all__'

class Requiredskillserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Requiredskill
        fields = '__all__'

class Permissionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'

class Rolepermissionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rolepermission
        fields = '__all__'

class Shiftchangerequestserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shiftchangerequest
        fields = '__all__'

class Shiftchangelogserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shiftchangelog
        fields = '__all__'

class Noteserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = '__all__'