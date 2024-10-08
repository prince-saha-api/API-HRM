from rest_framework import serializers
from contribution import models

class Addressserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = '__all__'

class Bankaccounttypeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bankaccounttype
        fields = '__all__'

class Bankaccountserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bankaccount
        fields = '__all__'
