from rest_framework import serializers
from contribution import models

class Addressserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['id', 'name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country']

class Bankaccounttypeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bankaccounttype
        fields = ['id', 'name']

class Bankaccountserializer(serializers.ModelSerializer):
    account_type=Bankaccounttypeserializer(many=False)
    address=Addressserializer(many=False)
    class Meta:
        model = models.Bankaccount
        exclude = ('is_active', 'code', 'created_at', 'updated_at')
