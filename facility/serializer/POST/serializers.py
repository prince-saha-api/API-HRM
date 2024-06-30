from rest_framework import serializers
from facility import models

class Facilityserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Facility
        fields = '__all__'