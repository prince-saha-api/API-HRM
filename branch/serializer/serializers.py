from rest_framework import serializers
from branch import models
from contribution.serializer import serializers as SRLZER_CONT
from company.serializer import serializers as SRLZER_COMP

class Operatinghourserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operatinghour
        fields = ['id', 'operating_hour_from', 'operating_hour_to']

class Branchserializer(serializers.ModelSerializer):
    company = SRLZER_COMP.Companyserializer(many=False)
    address = SRLZER_CONT.Addressserializer(many=False)
    class Meta:
        model = models.Branch
        exclude = ('is_active', 'code', 'created_at', 'updated_at')