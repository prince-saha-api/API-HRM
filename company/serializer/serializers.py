from rest_framework import serializers
from company import models
from contribution.serializer import serializers as SRLZER_CONT
        
class Basicinformationserializer(serializers.ModelSerializer):
    address = SRLZER_CONT.Addressserializer(many=False)
    class Meta:
        model = models.Basicinformation
        exclude = ('is_active', 'code', 'created_at', 'updated_at')

class Companyserializer(serializers.ModelSerializer):
    basic_information = Basicinformationserializer(many=False)
    class Meta:
        model = models.Company
        fields = ['id', 'basic_information']