from contribution.serializer import serializers as SRLZER_CONT
from branch.serializer import serializers as SRLZER_BRAN
from rest_framework import serializers
from department import models

class Departmentserializer(serializers.ModelSerializer):
    address = SRLZER_CONT.Addressserializer(many=False)
    branch = SRLZER_BRAN.Branchserializer(many=False)
    class Meta:
        model = models.Department
        fields = ['id', 'name', 'description', 'email', 'phone', 'fax', 'address', 'user', 'branch']