from rest_framework import serializers
from company import models

class Companyserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'

class Basicinformationserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Basicinformation
        fields = '__all__'

class Companytypeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Companytype
        fields = '__all__'

