from rest_framework import serializers
from payroll import models

class Payrollearningserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payrollearning
        fields = '__all__'

class Payrolldeductionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payrolldeduction
        fields = '__all__'

class Payrolltaxserializer(serializers.ModelSerializer):
    class Meta:
      model = models.Payrolltax
      fields = '__all__'