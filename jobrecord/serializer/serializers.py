from rest_framework import serializers
from jobrecord import models

class Employeejobhistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employeejobhistory
        fields = '__all__'