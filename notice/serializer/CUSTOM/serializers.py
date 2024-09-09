from rest_framework import serializers
from notice import models

class Noticeboardserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Noticeboard
        fields = ['id', 'title', 'description', 'attachment', 'publish_date', 'expiry_date', 'created_by', 'updated_by']