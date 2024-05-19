from rest_framework import serializers
from user import models

class Permissionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'