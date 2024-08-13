from rest_framework import serializers
from user.serializer import serializers as SRLZER_USER
from leave.serializer import serializers as SRLZER_LEAV
from leave import models

class Leavepolicyserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leavepolicy
        fields = '__all__'
    
class Leavesummaryserializer(serializers.ModelSerializer):
    leavepolicy = SRLZER_LEAV.Leavepolicyserializer(many=False)
    class Meta:
        model = models.Leavesummary
        fields = '__all__'

class Leavepolicyassignserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leavepolicyassign
        fields = '__all__'

class Leaverequestserializer(serializers.ModelSerializer):
    user = SRLZER_USER.Userserializer(many=False)
    leavepolicy = SRLZER_LEAV.Leavepolicyserializer(many=False)
    class Meta:
        model = models.Leaverequest
        fields = '__all__'

class Holidayserializer(serializers.ModelSerializer):
    employee_grade = SRLZER_USER.Gradeserializer(many=False)
    class Meta:
        model = models.Holiday
        fields = '__all__'