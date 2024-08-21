from contribution.serializer import serializers as SRLZER_CONT
from company.serializer import serializers as SRLZER_COMP
from branch.serializer import serializers as SRLZER_BRAN
from rest_framework import serializers
from department import models

class Departmentserializer(serializers.ModelSerializer):
    address = SRLZER_CONT.Addressserializer(many=False)
    branch = SRLZER_BRAN.Branchserializer(many=False)
    class Meta:
        model = models.Department
        fields = '__all__'