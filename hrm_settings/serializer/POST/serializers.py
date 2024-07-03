from rest_framework import serializers
from hrm_settings import models

class Weekdaysserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Weekdays
        fields = '__all__'

class Weeklyholidayserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Weeklyholiday
        fields = '__all__'

class Generalsettingsserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Generalsettings
        fields = '__all__'