from rest_framework import serializers
from notice import models

class Noticeboardserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Noticeboard
        fields = '__all__'

class Noticeboardcompanyserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Noticeboardcompany
        fields = '__all__'

class Noticeboardbranchserializer(serializers.ModelSerializer):
    class Meta:
      model = models.Noticeboardbranch
      fields = '__all__'

class Noticeboarddepartmentserializer(serializers.ModelSerializer):
    class Meta:
      model = models.Noticeboarddepartment
      fields = '__all__'
    
class Noticeboardemployeeserializer(serializers.ModelSerializer):
    class Meta:
      model = models.Noticeboardemployee
      fields = '__all__'