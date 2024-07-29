from django.contrib.auth import login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
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
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def resetPassword(request):
    userid = request.data.get('user')
    if userid == None: return Response({'data': {}, 'message': ['please provide an user\'s user id!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(id=userid)
    if user.exists():
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if new_password == None: return Response({'data': {}, 'message': ['new_password is required!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        if old_password:
            if not check_password(old_password, user.first().password):
                return Response({'data': {}, 'message': ['old_password doesn\'t match!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user.update(
                password=make_password(new_password),
                hr_password='-'.join([str(ord(each)+78) for each in new_password])
            )
            return Response({'data': {}, 'message': ['password changed successfully!'], 'status': 'success'}, status=status.HTTP_200_OK)
        except: return Response({'data': {}, 'message': ['couldn\'t change password!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': [f'user doesn\'t exist with this user id({userid})!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)