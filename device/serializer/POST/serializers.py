from rest_framework import serializers
from device import models

class Deviceserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = '__all__'

class Groupserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = '__all__'

class Devicegroupserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Devicegroup
        fields = '__all__'