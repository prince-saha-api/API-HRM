from rest_framework import serializers
from officialoffday import models

class Offdayserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offday
        fields = '__all__'