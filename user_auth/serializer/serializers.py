from rest_framework import serializers
from user import models
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    
class Registerserializer(serializers.ModelSerializer):
    super_user = serializers.BooleanField(default=False)
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'is_staff', 'super_user']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data.get('super_user', False):
            user = models.User.objects.create_superuser(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'], is_active=True, is_staff=True)
        else:
            user = models.User.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        # user.set_password(validated_data['password'])
        # user.save()
        return user


class Loginserializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, trim_whitespace=False, write_only=True)
    # token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    
class Changepasswordserializer(serializers.Serializer):
    model = models.User
    
    '''
    serializer for password change endpoint
    '''
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class Changeusertypeserializer(serializers.Serializer):
    model = models.User
    '''
    serializer for password change endpoint
    '''

    user_id = serializers.IntegerField(min_value=1, required=False)
    username = serializers.CharField(max_length=150, required=False)
    super_user = serializers.BooleanField(required=True)

    def validate(self, data):
        if not (bool(data.get("user_id")) or bool(data.get("username"))):
            raise serializers.ValidationError("Both user_id and username can't be blank at a time!")
        return data