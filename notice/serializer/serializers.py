from company.serializer import serializers as SRLZER_COMP
from branch.serializer import serializers as SRLZER_BRAN
from department.serializer import serializers as SRLZER_DEPA
from user.serializer import serializers as SRLZER_USER
from rest_framework import serializers
from notice import models

class Noticeboardcompanyserializer(serializers.ModelSerializer):
    company=SRLZER_COMP.Companyserializer(many=False)
    class Meta:
        model = models.Noticeboardcompany
        fields = '__all__'

class Noticeboardbranchserializer(serializers.ModelSerializer):
    branch=SRLZER_BRAN.Branchserializer(many=False)
    class Meta:
      model = models.Noticeboardbranch
      fields = '__all__'

class Noticeboarddepartmentserializer(serializers.ModelSerializer):
    department=SRLZER_DEPA.Departmentserializer(many=False)
    class Meta:
      model = models.Noticeboarddepartment
      fields = '__all__'
    
class Noticeboardemployeeserializer(serializers.ModelSerializer):
    user=SRLZER_USER.Userserializer(many=False)
    class Meta:
      model = models.Noticeboardemployee
      fields = '__all__'

class Noticeboardserializer(serializers.ModelSerializer):
    noticeboardcompany_noticeboard = Noticeboardcompanyserializer(many=True)
    noticeboardbranch_noticeboard = Noticeboardbranchserializer(many=True)
    noticeboarddepartment_noticeboard = Noticeboarddepartmentserializer(many=True)
    noticeboardemployee_noticeboard = Noticeboardemployeeserializer(many=True)
    class Meta:
        model = models.Noticeboard
        fields = '__all__'