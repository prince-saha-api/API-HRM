from rest_framework import serializers
from user import models

class Userserializer(serializers.ModelSerializer):
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

class Designationserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Designation
        fields = '__all__'

class Gradeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = '__all__'

class Shiftserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shift
        fields = '__all__'

class Religionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Religion
        fields = '__all__'

class Permissionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'

class Rolepermissionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rolepermission
        fields = '__all__'

class Ethnicgroupserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ethnicgroup
        fields = '__all__'

class Shiftchangerequestserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shiftchangerequest
        fields = '__all__'

class Shiftchangelogserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shiftchangelog
        fields = '__all__'

class Employeecontactserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employeecontact
        fields = '__all__'

class Employeeacademichistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employeeacademichistory
        fields = '__all__'

class Employeeexperiencehistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employeeexperiencehistory
        fields = '__all__'