from rest_framework import serializers
from user import models as MODELS_USER
from department import models as MODELS_DEPA
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN

from jobrecord import models

class Designationserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.Designation
        fields = ['id', 'name']

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.User
        fields = ['id', 'first_name', 'last_name']

class Basicinformationserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_COMP.Basicinformation
        fields = ['id', 'name']

class Companyserializer(serializers.ModelSerializer):
    basic_information=Basicinformationserializer(many=False)
    class Meta:
        model = MODELS_COMP.Company
        fields = ['id', 'basic_information']

class Branchserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_BRAN.Branch
        fields = ['id', 'name']

class Departmentserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_DEPA.Department
        fields = ['id', 'name']

class Employeejobhistoryserializer(serializers.ModelSerializer):
    user=Userserializer(many=False)
    company=Companyserializer(many=False)
    branch=Branchserializer(many=False)
    department=Departmentserializer(many=False)
    designation=Designationserializer(many=False)
    class Meta:
        model = models.Employeejobhistory
        fields = '__all__'