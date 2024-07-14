from rest_framework import serializers
from company import models
from contribution.serializer import serializers as SRLZER_CONT
        
class Basicinformationserializer(serializers.ModelSerializer):
    address = SRLZER_CONT.Addressserializer(many=False)
    class Meta:
        model = models.Basicinformation
        fields = '__all__'

class Companyserializer(serializers.ModelSerializer):
    basic_information = Basicinformationserializer(many=False)
    class Meta:
        model = models.Company
        fields = '__all__'