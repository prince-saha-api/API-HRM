from rest_framework import serializers
from branch import models

class Operatinghourserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operatinghour
        fields = '__all__'

class Branchserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = '__all__'

