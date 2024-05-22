from rest_framework import serializers
from user import models

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class Responsibilityserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Responsibility
        fields = '__all__'

class Requiredskillserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Requiredskill
        fields = '__all__'

class Designationserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Designation
        fields = '__all__'

class Gradeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = '__all__'

class Shiftserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shift
        fields = '__all__'

class Religionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Religion
        fields = '__all__'


