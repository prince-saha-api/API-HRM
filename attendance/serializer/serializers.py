from user.serializer import serializers as SRLZER_USER
from rest_framework import serializers
from attendance import models

class Attendanceserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attendance
        fields = '__all__'

class Requestmanualattendanceserializer(serializers.ModelSerializer):
    requested_by=SRLZER_USER.Userserializer(many=False)
    class Meta:
        model = models.Requestmanualattendance
        fields = '__all__'


class Remotelogsserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Remotelogs
        fields = '__all__'

class Requestremoteattendanceserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Requestremoteattendance
        fields = '__all__'