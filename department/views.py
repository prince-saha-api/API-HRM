from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from department import models as MODELS_DEPA
from department.serializer import serializers as SRLZER_DEPA
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getdepartments(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
                        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
                        {'name': 'location', 'convert': None, 'replace':'location__icontains'},
                        {'name': 'email', 'convert': None, 'replace':'email__icontains'},
                        {'name': 'phone', 'convert': None, 'replace':'phone__icontains'},
                        {'name': 'manager', 'convert': None, 'replace':'manager'},
                        {'name': 'user', 'convert': None, 'replace':'user'},
                        {'name': 'company', 'convert': None, 'replace':'company'},
                        {'name': 'is_active', 'convert': 'bool', 'replace':'is_active'},
                    ]
    departments = MODELS_DEPA.Department.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: departments = departments.order_by(column_accessor)

    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    departments = departments[(page-1)*page_size:page*page_size]

    departmentserializers = SRLZER_DEPA.Departmentserializer(departments, many=True)
    return Response({'data': {
        'count': MODELS_DEPA.Department.objects.all().count(),
        'page': page,
        'page_size': page_size,
        'result': departmentserializers.data
    }, 'message': '', 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adddepartment(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['email','phone']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_DEPA.Department, SRLZER_DEPA.Departmentserializer, request.data, unique_fields=unique_fields, extra_fields=extra_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatedepartment(request, departmentid=None):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    allowed_fields = ['name', 'description', 'location', 'email', 'phone', 'manager', 'user', 'company', 'is_active']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(MODELS_DEPA.Department, SRLZER_DEPA.Departmentserializer, departmentid, request.data, allowed_fields=allowed_fields, extra_fields=extra_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)