from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user import models
from user.serializer import serializers as SRLZER_U
from rest_framework.response import Response
from rest_framework import status
# from helps.common.generic import Generichelps as ghelp
# from django.core.paginator import Paginator


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getemployee(request):
    users = models.User.objects.all()
    userserializers = SRLZER_U.Userserializer(users, many=True)
    return Response(userserializers.data, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
# def getPermission(request, id):
#     if Permission.objects.filter(id=id).exists():
#         permission = Permission.objects.get(id=id)
#         permissionserializer=PermissionSerializer(permission, many=False)
#         return Response(permissionserializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'not found!'}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Active Permissions', 'all'])
# def getActivePermissions(request):
#     permissions = Permission.objects.filter(active=True)
#     permissionserializer=PermissionSerializer(permissions, many=True)
#     return Response(permissionserializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Active Permissions', 'all'])
# def getInactivePermissions(request):
#     permissions = Permission.objects.filter(active=False)
#     permissionserializer=PermissionSerializer(permissions, many=True)
#     return Response(permissionserializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Loggedin User Permissions', 'all'])
# def getLoggedinUserPermissions(request):
#     permissions = []
#     if request.user.username:
#         if User.objects.filter(username=request.user.username).exists():
#            ghelp().getPermissionsList(User=User, username=request.user.username, permissions=permissions, all=True)
#     return Response({'permissions': permissions}, status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Loggedin User Active Permissions', 'all'])
# def getLoggedinUserActivePermissions(request):
#     permissions = []
#     if request.user.username:
#         if User.objects.filter(username=request.user.username).exists():
#             ghelp().getPermissionsList(User=User, username=request.user.username, permissions=permissions, active=True)
#     return Response({'permissions': permissions}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Loggedin User Inactive Permissions', 'all'])
# def getLoggedinUserInactivePermissions(request):
#     permissions = []
#     if request.user.username:
#         if User.objects.filter(username=request.user.username).exists():
#             ghelp().getPermissionsList(User=User, username=request.user.username, permissions=permissions, inactive=True)
#     return Response({'permissions': permissions}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Add Permission', 'all'])
# def addPermission(request):
#     permissionserializer=PermissionSerializer(data=request.data)
#     if permissionserializer.is_valid(raise_exception=True):
#         permissionserializer.save()
#         return Response(permissionserializer.data, status=status.HTTP_201_CREATED)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Update Permission', 'all'])
# def updatePermission(request, id):
#     if Permission.objects.filter(id=id).exists():
#         permission = Permission.objects.get(id=id)
#         permissionserializer=PermissionSerializer(permission, data=request.data, partial=True)
#         if permissionserializer.is_valid(raise_exception=True):
#             permissionserializer.save()
#             return Response(permissionserializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'validation failed!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#     else:
#         return Response({'message': 'not found!'}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Update Permission', 'all'])
# def getUsersInfo(request):
#     customusers = CustomUser.objects.all()
#     customUserserializer = CustomUserSerializer(customusers, many=True)
#     return Response(customUserserializer.data, status=status.HTTP_200_OK)