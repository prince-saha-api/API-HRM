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
