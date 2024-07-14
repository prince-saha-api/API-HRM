from rest_framework import serializers
from company import models
        
class Basicinformationserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Basicinformation
        fields = '__all__'

class Companyserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'

