from django.contrib.auth import login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from user_auth.serializer import serializers as SRLZER_UA
from user.models import User
from rest_framework.decorators import api_view

class RegisterAPI(generics.GenericAPIView):
    serializer_class = SRLZER_UA.Registerserializer
    
    def post(self, request, *args, **kwargs):
        reponse = {
            'status': '',
            'message': '',
            'data': {}
            }
        STATUS = status.HTTP_400_BAD_REQUEST
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.save()

            reponse['status'] = 'success.'
            reponse['message'] = f'registered successfully({request.data["username"]}).'
            STATUS = status.HTTP_200_OK
        else:
            reponse['status'] = 'error.'
            reponse['message'] = 'couldn\'t register.'
        return Response(reponse, status=STATUS)
    
@api_view(['POST'])
def login_user(request):
    reponse = {
        'refresh': '',
        'access': '',
        'user': {}
        }
    STATUS = status.HTTP_400_BAD_REQUEST
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            authenticate_user = authenticate(request, username=username, password=password)
            if authenticate_user is not None:
                user = User.objects.get(username=username)
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                login(request, authenticate_user)
                reponse['access'] = str(access)
                reponse['refresh'] = str(refresh)
                reponse['user'] = SRLZER_UA.Userserializer(user, many=False).data
                STATUS = status.HTTP_200_OK
    return Response(reponse, status=STATUS)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        reponse = {
            'status': '',
            'message': '',
            'data': {}
            }
        try:
            refresh = request.data["refresh"]
            token = RefreshToken(refresh)
            token.blacklist()
            reponse['status'] = 'success.'
            reponse['message'] = 'successfully logged out.'
            return Response(reponse, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            reponse['status'] = 'error.'
            reponse['message'] = 'something went worng.'
            return Response(reponse, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
    
class ChangePasswordView(generics.UpdateAPIView):
    '''
    An endpoint for changing password.
    '''
    
    serializer_class = SRLZER_UA.Changepasswordserializer
    model = User
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong Password.']}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)