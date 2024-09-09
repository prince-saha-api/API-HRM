from company.serializer import serializers as SRLZER_COMP
from branch.serializer import serializers as SRLZER_BRAN
from department.serializer import serializers as SRLZER_DEPA
from user.serializer.CUSTOM import serializers as CSRLZER_USER
from notice.serializer.CUSTOM import serializers as CSRLZER_NOTI
from rest_framework import serializers
from notice import models

class Noticeboardcompanyserializer(serializers.ModelSerializer):
    noticeboard=CSRLZER_NOTI.Noticeboardserializer(many=False)
    company=SRLZER_COMP.Companyserializer(many=False)
    class Meta:
        model = models.Noticeboardcompany
        fields = ['id', 'noticeboard', 'company']

class Noticeboardbranchserializer(serializers.ModelSerializer):
    noticeboard=CSRLZER_NOTI.Noticeboardserializer(many=False)
    branch=SRLZER_BRAN.Branchserializer(many=False)
    class Meta:
      model = models.Noticeboardbranch
      fields = ['id', 'noticeboard', 'branch']

class Noticeboarddepartmentserializer(serializers.ModelSerializer):
    noticeboard=CSRLZER_NOTI.Noticeboardserializer(many=False)
    department=SRLZER_DEPA.Departmentserializer(many=False)
    class Meta:
      model = models.Noticeboarddepartment
      fields = ['id', 'noticeboard', 'department']
    
class Noticeboardemployeeserializer(serializers.ModelSerializer):
    noticeboard=CSRLZER_NOTI.Noticeboardserializer(many=False)
    user=CSRLZER_USER.Otheruserserializer(many=False)
    class Meta:
      model = models.Noticeboardemployee
      fields = ['id', 'noticeboard', 'user']

class Noticeboardserializer(serializers.ModelSerializer):
    noticeboardcompany_noticeboard = Noticeboardcompanyserializer(many=True)
    noticeboardbranch_noticeboard = Noticeboardbranchserializer(many=True)
    noticeboarddepartment_noticeboard = Noticeboarddepartmentserializer(many=True)
    noticeboardemployee_noticeboard = Noticeboardemployeeserializer(many=True)
    class Meta:
        model = models.Noticeboard
        fields = ['id', 'title', 'noticeboardcompany_noticeboard', 'noticeboardbranch_noticeboard', 'noticeboarddepartment_noticeboard', 'noticeboardemployee_noticeboard', 'description', 'attachment', 'publish_date', 'expiry_date', 'created_by', 'updated_by']