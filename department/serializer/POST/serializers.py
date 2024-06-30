from rest_framework import serializers
from department import models

class Departmentserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'
