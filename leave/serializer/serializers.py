from rest_framework import serializers
from leave import models

class Leavepolicyserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leavepolicy
        fields = '__all__'
    
class Leavesummaryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leavesummary
        fields = '__all__'

class Leavepolicyassignserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leavepolicyassign
        fields = '__all__'

class Leaverequestserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leaverequest
        fields = '__all__'