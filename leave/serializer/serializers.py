from rest_framework import serializers
from user.serializer import serializers as SRLZER_USER
from leave import models

class Leavepolicyserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leavepolicy
        fields = '__all__'
    
class Leavesummaryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leavesummary
        fields = '__all__'

class Leavepolicyassignserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leavepolicyassign
        fields = '__all__'

class Leaverequestserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leaverequest
        fields = '__all__'

class Leaveallocationrequestserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leaveallocationrequest
        fields = '__all__'

class Holidayserializer(serializers.ModelSerializer):
    employee_grade = SRLZER_USER.Gradeserializer(many=False)
    class Meta:
        model = models.Holiday
        fields = '__all__'