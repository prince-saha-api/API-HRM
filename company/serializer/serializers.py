from rest_framework import serializers
from company import models

class Companyserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'
