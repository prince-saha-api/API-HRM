from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from contribution import models as MODELS_CONT
from leave import models as MODELS_LEAV
from department import models as MODELS_DEPA
from hrm_settings import models as MODELS_SETT
from user import models as MODELS_USER
from jobrecord import models as MODELS_JOBR
from user.serializer import serializers as SRLZER_USER
from user.serializer.POST import serializers as PSRLZER_USER
from contribution.serializer.POST import serializers as PSRLZER_CONT
from rest_framework.response import Response
from rest_framework import status
from helps.common.generic import Generichelps as ghelp
from helps.choice import common as CHOICE
# from django.core.paginator import Paginator
from drf_nested_forms.utils import NestedForm
import random


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getjobhistorys(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'effective_from', 'convert': None, 'replace':'effective_from'},
        {'name': 'increment_on', 'convert': None, 'replace':'increment_on__icontains'},
        {'name': 'prev_salary', 'convert': None, 'replace':'prev_salary'},
        {'name': 'new_salary', 'convert': None, 'replace':'new_salary'},
        {'name': 'increment_amount', 'convert': None, 'replace':'increment_amount'},
        {'name': 'percentage', 'convert': None, 'replace':'percentage'},
        {'name': 'prev_company', 'convert': None, 'replace':'prev_company'},
        {'name': 'prev_branch', 'convert': None, 'replace':'prev_branch'},
        {'name': 'prev_department', 'convert': None, 'replace':'prev_department'},
        {'name': 'prev_designation', 'convert': None, 'replace':'prev_designation'},
        {'name': 'prev_employee_type', 'convert': None, 'replace':'prev_employee_type'},
        {'name': 'from_date', 'convert': None, 'replace':'from_date'},
        {'name': 'to_date', 'convert': None, 'replace':'to_date'},
        {'name': 'status_adjustment', 'convert': None, 'replace':'status_adjustment__icontains'},
        {'name': 'appraisal_by', 'convert': None, 'replace':'appraisal_by'},
        {'name': 'comment', 'convert': None, 'replace':'comment__icontains'}
    ]
    employeejobhistorys = MODELS_JOBR.Employeejobhistory.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: employeejobhistorys = employeejobhistorys.order_by(column_accessor)

    total_count = employeejobhistorys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: employeejobhistorys = employeejobhistorys[(page-1)*page_size:page*page_size]

    designationserializers = SRLZER_USER.Designationserializer(employeejobhistorys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': designationserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addjobhistory(request):
    # userid = request.user.id
    unique_fields = ['name']
    required_fields= ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Designation, 
        Serializer=PSRLZER_USER.Designationserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatejobhistory(request, jobhistoryid=None):
    allowed_fields = ['name', 'grade']
    unique_fields=['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Designation,
        Serializer=PSRLZER_USER.Designationserializer,
        id=jobhistoryid,
        data=request.data,
        unique_fields=unique_fields,
        allowed_fields=allowed_fields
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletejobhistory(request, jobhistoryid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.User, 'fields': [{'field': 'designation', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Designation,
        id=jobhistoryid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)