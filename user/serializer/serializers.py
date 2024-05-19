from rest_framework import serializers
from user import models

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
