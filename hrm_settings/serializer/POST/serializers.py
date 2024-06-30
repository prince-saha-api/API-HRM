from rest_framework import serializers
from hrm_settings import models

class Fiscalyearserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fiscalyear
        fields = '__all__'