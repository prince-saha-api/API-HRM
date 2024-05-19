from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from customuser.models import *
# from django.contrib.auth.models import User
# from customuser.serializer.serializers import *
# from rest_framework.response import Response
# from rest_framework import status
# from helps.common.generic import Generichelps as ghelp
# from django.core.paginator import Paginator

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def getPermissions(request):
#     page = request.GET.get('page')
#     limit = request.GET.get('limit')
#     if page == None and limit == None:
#         permissions = Permission.objects.all()
#         permissionserializer=PermissionSerializer(permissions, many=True)
#         return Response(permissionserializer.data, status=status.HTTP_200_OK)
#     else:
#         allpermissions = Permission.objects.all().order_by('id')
#         limit = int(limit) if limit is not None else 10
#         page = int(page) if page is not None else 1

#         paginator = Paginator(allpermissions, limit)
#         permissions = paginator.get_page(page)

#         pages = paginator.num_pages

#         permissionserializer=PermissionSerializer(permissions, many=True)
#         return Response({
#             'item_count': paginator.count,
#             'per_page_limit': limit,
#             'num_pages': pages,
#             'next': f'http://127.0.0.1:8000/api/customuser/get-permissions?page={page+1}&limit={limit}' if permissions.has_next() else 'N/A',
#             'previous': f'http://127.0.0.1:8000/api/customuser/get-permissions?page={page-1}&limit={limit}' if permissions.has_previous() else 'N/A',
#             'result': permissionserializer.data}, status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Single Permission Details', 'all'])
# def filterPermissions(request):
#     extra_conditions = {'name': 'icontains'}
#     permissions = ghelp().filterClass(Permission, request, extra_conditions)
#     permissionserializer=PermissionSerializer(permissions, many=True)
#     return Response(permissionserializer.data, status=status.HTTP_200_OK)


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