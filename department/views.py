from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from department import models as MODELS_DEPA
from department.serializer import serializers as SRLZER_DEPA
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getdepartments(request):
    departments = MODELS_DEPA.Department.objects.all()
    departmentserializers = SRLZER_DEPA.Departmentserializer(departments, many=True)
    return Response(departmentserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def adddepartment(request):
    departmentserializers = SRLZER_DEPA.Departmentserializer(data=request.data, many=False)
    if departmentserializers.is_valid():
        departmentserializers.save()
        return Response({'status': 'success', 'message': '', 'data': departmentserializers.data}, status=status.HTTP_201_CREATED)
    else: return Response({'status': 'error', 'message': '', 'data': departmentserializers.errors}, status=status.HTTP_400_BAD_REQUEST)
