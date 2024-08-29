from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from contribution import models as MODELS_CONT
from leave import models as MODELS_LEAV
from department import models as MODELS_DEPA
from hrm_settings import models as MODELS_SETT
from user import models as MODELS_USER
from branch import models as MODELS_BRAN
from device import models as MODELS_DEVI
from jobrecord import models as MODELS_JOBR
from jobrecord.serializer.POST import serializers as PSRLZER_JOBR
from user.serializer.CUSTOM import serializers as CSRLZER_USER
from user.serializer import serializers as SRLZER_USER
from user.serializer.POST import serializers as PSRLZER_USER
from contribution.serializer.POST import serializers as PSRLZER_CONT
from hrm_settings.serializer.POST import serializers as PSRLZER_SETT
from leave.serializer.POST import serializers as PSRLZER_LEAV
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from helps.common.generic import Generichelps as ghelp
from helps.device.a_device import A_device as DEVICE
from helps.choice import common as CHOICE
from drf_nested_forms.utils import NestedForm
from requests.auth import HTTPDigestAuth
import requests
import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getresponsibilitys(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'}
    ]
    responsibilitys = MODELS_USER.Responsibility.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: responsibilitys = responsibilitys.order_by(column_accessor)

    total_count = responsibilitys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: responsibilitys = responsibilitys[(page-1)*page_size:page*page_size]

    responsibilityserializers = SRLZER_USER.Responsibilityserializer(responsibilitys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': responsibilityserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addresponsibility(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['title']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields = ['title']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Responsibility, 
        Serializer=PSRLZER_USER.Responsibilityserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        extra_fields=extra_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getrequiredskills(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'}
    ]
    requiredskills = MODELS_USER.Requiredskill.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: requiredskills = requiredskills.order_by(column_accessor)

    total_count = requiredskills.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: requiredskills = requiredskills[(page-1)*page_size:page*page_size]

    requiredskillserializers = SRLZER_USER.Requiredskillserializer(requiredskills, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': requiredskillserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addrequiredskill(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['title']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields= ['title']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Requiredskill, 
        Serializer=PSRLZER_USER.Requiredskillserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        extra_fields=extra_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getdsignations(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'grade', 'convert': None, 'replace':'grade'}
    ]
    dsignations = MODELS_USER.Designation.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: dsignations = dsignations.order_by(column_accessor)

    total_count = dsignations.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: dsignations = dsignations[(page-1)*page_size:page*page_size]

    designationserializers = SRLZER_USER.Designationserializer(dsignations, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': designationserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def adddsignation(request):
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
def updatedesignation(request, designationid=None):
    allowed_fields = ['name', 'grade']
    unique_fields=['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Designation,
        Serializer=PSRLZER_USER.Designationserializer,
        id=designationid,
        data=request.data,
        unique_fields=unique_fields,
        allowed_fields=allowed_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletedesignation(request, designationid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.User, 'fields': [{'field': 'designation', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Designation,
        id=designationid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getgrades(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'}
    ]
    
    grades = MODELS_USER.Grade.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: grades = grades.order_by(column_accessor)

    total_count = grades.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: grades = grades[(page-1)*page_size:page*page_size]

    gradeserializers = SRLZER_USER.Gradeserializer(grades, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': gradeserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addgrade(request):
    # userid = request.user.id
    unique_fields = ['name']
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Grade, 
        Serializer=PSRLZER_USER.Gradeserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updategrade(request, gradeid=None):
    # userid = request.user.id
    unique_fields=['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Grade,
        Serializer=PSRLZER_USER.Gradeserializer,
        id=gradeid,
        data=request.data,
        unique_fields=unique_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletegrade(request, gradeid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_LEAV.Holiday, 'fields': [{'field': 'employee_grade', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_USER.Designation, 'fields': [{'field': 'grade', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_USER.User, 'fields': [{'field': 'grade', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Grade,
        id=gradeid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getshifts(request):

    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'in_time', 'convert': None, 'replace':'in_time'},
        {'name': 'out_time', 'convert': None, 'replace':'out_time'},
        {'name': 'late_tolerance_time', 'convert': None, 'replace':'late_tolerance_time'}
    ]

    shifts = MODELS_USER.Shift.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: shifts = shifts.order_by(column_accessor)

    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    shifts = shifts[(page-1)*page_size:page*page_size]

    shiftserializers = SRLZER_USER.Shiftserializer(shifts, many=True)
    return Response({'data': {
        'count': MODELS_USER.Shift.objects.all().count(),
        'page': page,
        'page_size': page_size,
        'result': shiftserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addshift(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields = ['name', 'in_time', 'out_time']
    unique_fields=['name']
    fields_regex = [
        {'field': 'in_time', 'type': 'time'},
        {'field': 'out_time', 'type': 'time'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Shift,
        Serializer=PSRLZER_USER.Shiftserializer,
        data=request.data,
        unique_fields=unique_fields,
        extra_fields=extra_fields,
        required_fields=required_fields,
        fields_regex=fields_regex
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateshift(request, shiftid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    fields_regex = [
        {'field': 'in_time', 'type': 'time'},
        {'field': 'out_time', 'type': 'time'},
    ]
    unique_fields=['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Shift, 
        Serializer=PSRLZER_USER.Shiftserializer, 
        id=shiftid, 
        data=request.data,
        unique_fields=unique_fields,
        extra_fields=extra_fields, 
        fields_regex=fields_regex
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteshift(request, shiftid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.User, 'fields': [{'field': 'shift', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_USER.Shiftchangelog, 'fields': [{'field': 'previouseshift', 'relation': 'foreignkey', 'records': []}, {'field': 'newshift', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_USER.Shiftchangerequest, 'fields': [{'field': 'reqshiftid', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Shift,
        id=shiftid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def assignshift(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    userlist = request.data.get('user')
    classOBJpackage = {'User': MODELS_USER.User, 'Shift': MODELS_USER.Shift}
    shiftid = request.data.get('shift')
    response = ghelp().assignShiftToBulkUser(classOBJpackage, userlist, shiftid)
    
    if response['flag']:
        response_successflag = 'success'
        response_status = status.HTTP_202_ACCEPTED
    response_message.extend(response['message'])
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getshiftchangerequest(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'reqshiftid', 'convert': None, 'replace':'reqshiftid'},
        {'name': 'fromdate', 'convert': None, 'replace':'fromdate'},
        {'name': 'todate', 'convert': None, 'replace':'todate'},
        {'name': 'reqnote', 'convert': None, 'replace':'reqnote__icontains'},
        {'name': 'status', 'convert': None, 'replace':'status__icontains'},
        {'name': 'adminnote', 'convert': None, 'replace':'adminnote__icontains'}
    ]
    shiftchangerequests = MODELS_USER.Shiftchangerequest.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: shiftchangerequests = shiftchangerequests.order_by(column_accessor)

    total_count = shiftchangerequests.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: shiftchangerequests = shiftchangerequests[(page-1)*page_size:page*page_size]

    shiftchangerequestserializers = SRLZER_USER.Shiftchangerequestserializer(shiftchangerequests, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': shiftchangerequestserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addshiftchangerequest(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'user': userid, 'updated_by': userid})
    extra_fields.update({'status': CHOICE.STATUS[0][1]})
    allowed_fields = ['reqshiftid', 'fromdate', 'todate',  'reqnote']
    choice_fields = [
        {'name': 'status', 'type': 'single-string', 'values': [item[1] for item in CHOICE.STATUS]}
    ]
    required_fields = ['user', 'reqshiftid', 'fromdate', 'todate']
    fields_regex = [
        {'field': 'fromdate', 'type': 'date'},
        {'field': 'todate', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Shiftchangerequest, 
        Serializer=PSRLZER_USER.Shiftchangerequestserializer, 
        data=request.data, 
        allowed_fields=allowed_fields, 
        extra_fields=extra_fields, 
        choice_fields=choice_fields, 
        required_fields=required_fields,
        fields_regex=fields_regex
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def updateshiftchangerequest(request, shiftchangerequestid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    allowed_fields = ['reqshiftid', 'fromdate', 'todate', 'reqnote']
    freez_update = [{'status': [CHOICE.STATUS[1][1], CHOICE.STATUS[2][1]]}]
    fields_regex = [
        {'field': 'fromdate', 'type': 'date'},
        {'field': 'todate', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Shiftchangerequest, 
        Serializer=PSRLZER_USER.Shiftchangerequestserializer, 
        id=shiftchangerequestid, 
        data=request.data, 
        allowed_fields=allowed_fields, 
        freez_update=freez_update, 
        extra_fields=extra_fields, 
        fields_regex=fields_regex
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def approveshiftchangerequest(request, shiftchangerequestid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'decision_by': userid})
    extra_fields.update({'status': CHOICE.STATUS[1][1]})
    allowed_fields = ['adminnote']
    # freez_update = [{'status': [CHOICE.STATUS[1][1], CHOICE.STATUS[2][1]]}]
    continue_update = [{'status': [CHOICE.STATUS[0][1]]}]
    fields_regex = [
        {'field': 'fromdate', 'type': 'date'},
        {'field': 'todate', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Shiftchangerequest, 
        Serializer=PSRLZER_USER.Shiftchangerequestserializer, 
        id=shiftchangerequestid, 
        data=request.data, 
        allowed_fields=allowed_fields, 
        continue_update=continue_update, 
        extra_fields=extra_fields, 
        fields_regex=fields_regex
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def rejectshiftchangerequest(request, shiftchangerequestid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'decision_by': userid})
    extra_fields.update({'status': CHOICE.STATUS[2][1]})
    allowed_fields = ['adminnote']
    # freez_update = [{'status': [CHOICE.STATUS[1][1], CHOICE.STATUS[2][1]]}]
    continue_update = [{'status': [CHOICE.STATUS[0][1]]}]
    fields_regex = [
        {'field': 'fromdate', 'type': 'date'},
        {'field': 'todate', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Shiftchangerequest, 
        Serializer=PSRLZER_USER.Shiftchangerequestserializer, 
        id=shiftchangerequestid, 
        data=request.data, 
        allowed_fields=allowed_fields, 
        continue_update=continue_update, 
        extra_fields=extra_fields, 
        fields_regex=fields_regex
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteshiftchangerequest(request, shiftchangerequestid=None):
    # freez_delete = [{'status': [CHOICE.STATUS[1][1], CHOICE.STATUS[2][1]]}]
    continue_delete = [{'status': [CHOICE.STATUS[0][1]]}]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Shiftchangerequest,
        id=shiftchangerequestid,
        continue_delete=continue_delete)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getshiftchangelog(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'decision_by', 'convert': None, 'replace':'decision_by'},
        {'name': 'previouseshift', 'convert': None, 'replace':'previouseshift'},
        {'name': 'newshift', 'convert': None, 'replace':'newshift'},
        {'name': 'date', 'convert': None, 'replace':'date'},
        {'name': 'reason', 'convert': None, 'replace':'reason__icontains'}
    ]
    shiftchangelogs = MODELS_USER.Shiftchangelog.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: shiftchangelogs = shiftchangelogs.order_by(column_accessor)

    total_count = shiftchangelogs.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: shiftchangelogs = shiftchangelogs[(page-1)*page_size:page*page_size]

    shiftchangelogserializers = SRLZER_USER.Shiftchangelogserializer(shiftchangelogs, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': shiftchangelogserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getreligions(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'}
    ]
    religions = MODELS_USER.Religion.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: religions = religions.order_by(column_accessor)

    total_count = religions.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: religions = religions[(page-1)*page_size:page*page_size]

    religionserializers = SRLZER_USER.Religionserializer(religions, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': religionserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addreligion(request):
    # details = {
    #     'data': {
    #                 "name":"Emon Molla",
    #                 "age":40,
    #                 "address":{
    #                     "district":"Madaripur",
    #                     "village":"Itkhola Bazitput",
    #                     "next": {
    #                         "dummy": "dummy details",
    #                         "policy": "hour",
    #                         "abc": {
    #                             "def": "def"
    #                         }
    #                     }
    #                 }
    #             },
    #     'order': ['address', 'next', 'abc'],
    #     'info': {
    #         'address': {
    #             'model': 'Random',
    #             'serializer': 'Random',
    #             'allow_fields': [],
    #             'required_fields': [],
    #             'unique_fields': []
    #         },
    #         'next': {
    #             'model': 'Random',
    #             'serializer': 'Random',
    #             'allow_fields': [],
    #             'required_fields': [],
    #             'unique_fields': []
    #         },
    #         'abc': {
    #             'model': 'Random',
    #             'serializer': 'Random',
    #             'allow_fields': [],
    #             'required_fields': [],
    #             'unique_fields': []
    #         }
    #     }
    # }

    # ghelp().nestedObjectPrepare(details)
    # # print(details)
    # input()



    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    unique_fields = ['name']
    required_fields = ['name']
    
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Religion, 
        Serializer=PSRLZER_USER.Religionserializer, 
        data=request.data, 
        extra_fields=extra_fields, 
        unique_fields=unique_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatereligion(request, religionid=None):
    unique_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Religion,
        Serializer=PSRLZER_USER.Religionserializer,
        id=religionid,
        data=request.data,
        unique_fields=unique_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletereligion(request, religionid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.User, 'fields': [{'field': 'religion', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Religion,
        id=religionid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getpermissions(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'}
    ]
    permissions = MODELS_USER.Permission.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: permissions = permissions.order_by(column_accessor)

    total_count = permissions.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: permissions = permissions[(page-1)*page_size:page*page_size]

    permissionserializers = SRLZER_USER.Permissionserializer(permissions, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': permissionserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addpermission(request):
    unique_fields = ['name']
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Permission, 
        Serializer=PSRLZER_USER.Permissionserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatepermission(request, permissionid=None):
    unique_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Permission,
        Serializer=PSRLZER_USER.Permissionserializer,
        id=permissionid,
        data=request.data,
        unique_fields=unique_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletepermission(request, permissionid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.Rolepermission, 'fields': [{'field': 'permission', 'relation': 'manytomanyfield', 'records': MODELS_USER.Permission.objects.filter(id=permissionid).first().rolepermission_set.all()}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Permission,
        id=permissionid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getrolepermissions(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'}
    ]
    rolepermissions = MODELS_USER.Rolepermission.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: rolepermissions = rolepermissions.order_by(column_accessor)

    total_count = rolepermissions.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: rolepermissions = rolepermissions[(page-1)*page_size:page*page_size]

    rolepermissionserializers = SRLZER_USER.Rolepermissionserializer(rolepermissions, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': rolepermissionserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addrolepermission(request):
    unique_fields = ['name']
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Rolepermission, 
        Serializer=PSRLZER_USER.Rolepermissionserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updaterolepermission(request, rolepermissionid=None):
    unique_fields=['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Rolepermission, 
        Serializer=PSRLZER_USER.Rolepermissionserializer, 
        id=rolepermissionid, 
        data=request.data,
        unique_fields=unique_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleterolepermission(request, rolepermissionid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.User, 'fields': [{'field': 'role_permission', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Rolepermission,
        id=rolepermissionid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getethnicgroups(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'}
    ]
    ethnicgroups = MODELS_USER.Ethnicgroup.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: ethnicgroups = ethnicgroups.order_by(column_accessor)

    total_count = ethnicgroups.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: ethnicgroups = ethnicgroups[(page-1)*page_size:page*page_size]

    ethnicgroupserializers = SRLZER_USER.Ethnicgroupserializer(ethnicgroups, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': ethnicgroupserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addethnicgroup(request):
    unique_fields = ['name']
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Ethnicgroup, 
        Serializer=PSRLZER_USER.Ethnicgroupserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getemployee(request):

    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'first_name', 'convert': None, 'replace':'first_name__icontains'},
        {'name': 'last_name', 'convert': None, 'replace':'last_name__icontains'},
        {'name': 'designation', 'convert': None, 'replace':'designation'},
        {'name': 'dob', 'convert': None, 'replace':'dob'},
        {'name': 'blood_group', 'convert': None, 'replace':'blood_group__icontains'},
        {'name': 'fathers_name', 'convert': None, 'replace':'fathers_name__icontains'},
        {'name': 'mothers_name', 'convert': None, 'replace':'mothers_name__icontains'},
        {'name': 'marital_status', 'convert': None, 'replace':'marital_status__icontains'},
        {'name': 'gender', 'convert': None, 'replace':'gender__icontains'},
        {'name': 'spouse_name', 'convert': None, 'replace':'spouse_name__icontains'},
        {'name': 'religion', 'convert': None, 'replace':'religion'},
        {'name': 'nationality', 'convert': None, 'replace':'nationality__icontains'},
        {'name': 'personal_email', 'convert': None, 'replace':'personal_email__icontains'},
        {'name': 'personal_phone', 'convert': None, 'replace':'personal_phone__icontains'},
        {'name': 'nid_passport_no', 'convert': None, 'replace':'nid_passport_no__icontains'},
        {'name': 'official_id', 'convert': None, 'replace':'official_id__icontains'},
        {'name': 'official_email', 'convert': None, 'replace':'official_email__icontains'},
        {'name': 'official_phone', 'convert': None, 'replace':'official_phone__icontains'},
        {'name': 'employee_type', 'convert': None, 'replace':'employee_type__icontains'},
        
        # {'name': 'department', 'convert': None, 'replace':'departmenttwo__id'},
        # {'name': 'company', 'convert': None, 'replace':'branch_company__department_branch'},
        # {'name': 'branch', 'convert': None, 'replace':'department_branch'},

        {'name': 'gross_salary_from', 'convert': None, 'replace':'gross_salary__gte'},
        {'name': 'gross_salary_to', 'convert': None, 'replace':'gross_salary__lte'},
        {'name': 'payment_in', 'convert': None, 'replace':'payment_in__icontains'},
        {'name': 'supervisor', 'convert': None, 'replace':'supervisor'},
        {'name': 'expense_approver', 'convert': None, 'replace':'expense_approver'},
        {'name': 'leave_approver', 'convert': None, 'replace':'leave_approver'},
        {'name': 'shift_request_approver', 'convert': None, 'replace':'shift_request_approver'},
        {'name': 'grade', 'convert': None, 'replace':'grade'},
        {'name': 'shift', 'convert': None, 'replace':'shift'},
        {'name': 'joining_date_from', 'convert': None, 'replace':'joining_date__gte'},
        {'name': 'joining_date_to', 'convert': None, 'replace':'joining_date__lte'},
        {'name': 'allow_overtime', 'convert': 'bool', 'replace':'allow_overtime'},
        {'name': 'allow_remote_checkin', 'convert': 'bool', 'replace':'allow_remote_checkin'},
        {'name': 'job_status', 'convert': None, 'replace':'job_status__icontains'},
        {'name': 'official_note', 'convert': None, 'replace':'official_note__icontains'},
        {'name': 'rfid', 'convert': None, 'replace':'rfid__icontains'}
    ]
    users = None
    flag_company_branch_department = False
    companyid = request.GET.get('company')
    if companyid:
        flag_company_branch_department = True
        branchs = MODELS_BRAN.Branch.objects.filter(company=companyid)
        departments = MODELS_DEPA.Department.objects.filter(branch__in=[each.id for each in branchs])
        users = MODELS_USER.User.objects.filter(departmenttwo__in=[each.id for each in departments]).distinct('id').order_by('id')
    branchid = request.GET.get('branch')
    if branchid:
        if not flag_company_branch_department:
            flag_company_branch_department = True
            departments = MODELS_DEPA.Department.objects.filter(branch=branchid)
            users = MODELS_USER.User.objects.filter(departmenttwo__in=[each.id for each in departments]).distinct('id').order_by('id')
    departmentid = request.GET.get('department')
    if departmentid:
        if not flag_company_branch_department:
            users = MODELS_USER.User.objects.filter(department=departmentid).distinct('id').order_by('id')

    kwargs = ghelp().KWARGS(request, filter_fields)
    kwargs.update({'is_active': True})
    
    users = MODELS_USER.User.objects.all() if users == None else users
    users = users.filter(**kwargs)
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: users = users.order_by(column_accessor)
    
    total_count = users.count()

    page = request.GET.get('page')
    page_size = request.GET.get('page_size')
    if page_size and page:
        page = int(page) if page else 1
        page_size = int(page_size) if page_size else 10
        users = users[(page-1)*page_size:page*page_size]

    userserializers = SRLZER_USER.Userserializer(users, many=True)
    chars = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']]
    for userserializer in userserializers.data:
        if userserializer['hr_password']:
            splitpassword = [int(each)-78 for each in userserializer['hr_password'].split('-')]
            password = ''
            for value in splitpassword:
                ran_number = random.randint(0, 25)
                ch = chars[ran_number%2][ran_number]
                password += ch+chr(value)+str(ord(ch))
            userserializer['hr_password'] = password

    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': userserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addemployee(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST
    
    requestdata = dict(request.data)
    requestdata.update({'abcdef[abcdef]': ['abcdef']})
    options = {'allow_blank': True, 'allow_empty': False}
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)

    
    personalDetails = form.data.get('personalDetails')
    officialDetails = form.data.get('officialDetails')
    emergencyContact = form.data.get('emergencyContact')
    academicRecord = form.data.get('academicRecord')
    previousExperience = form.data.get('previousExperience')
    salaryAndLeaves = form.data.get('salaryAndLeaves')

    personalDetails = ghelp().prepareData(personalDetails, 'personal')
    officialDetails = ghelp().prepareData(officialDetails, 'office')
    emergencyContact = ghelp().prepareData(emergencyContact, 'emergencycontact')
    academicRecord = ghelp().prepareData(academicRecord, 'academicrecord')
    previousExperience = ghelp().prepareData(previousExperience, 'previousexperience')
    ghelp().preparesalaryAndLeaves(salaryAndLeaves)

    # uploadDocuments = form.data.get('uploadDocuments')

    
    fields_tobe_checked = [
        {
            'data': officialDetails,
            'to_be_apply': ['choice_fields', 'fields_regex'],
            'required_fields': ['official_id', 'ethnic_group', 'joining_date', 'company', 'branch', 'department', 'designation', 'employee_type'],
            'fields_regex': [{'field': 'official_id', 'type': 'employeeid'}, {'field': 'joining_date', 'type': 'date'}],
            'choice_fields': [{'name': 'employee_type', 'type': 'single-string', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]}]
        },
        {
            'data': salaryAndLeaves,
            'to_be_apply': ['fields_regex'],
            'required_fields': ['gross_salary'],
            'fields_regex': []
        }
    ]
    response_message.extend(ghelp().checkrequiredfiels(fields_tobe_checked))
    if not response_message:
        
        classOBJpackage = {
            'Generalsettings': MODELS_SETT.Generalsettings,
            'Leavepolicy': MODELS_LEAV.Leavepolicy,
            'Leavepolicyassign': MODELS_LEAV.Leavepolicyassign,
            'Leavesummary': MODELS_LEAV.Leavesummary,
            'User': MODELS_USER.User,
            'Address': MODELS_CONT.Address,
            'Designation': MODELS_USER.Designation,
            'Shift': MODELS_USER.Shift,
            'Grade': MODELS_USER.Grade,
            'Bankaccount': MODELS_CONT.Bankaccount,
            'Bankaccounttype': MODELS_CONT.Bankaccounttype,
            'Religion': MODELS_USER.Religion,
        }
        serializerOBJpackage = {
            'Generalsettings': PSRLZER_SETT.Generalsettingsserializer,
            'Leavepolicy': PSRLZER_LEAV.Leavepolicyserializer,
            'Leavepolicyassign': PSRLZER_LEAV.Leavepolicyassignserializer,
            'Leavesummary': PSRLZER_LEAV.Leavesummaryserializer,
            'User': PSRLZER_USER.Userserializer,
            'Address': PSRLZER_CONT.Addressserializer,
            'Designation': PSRLZER_USER.Designationserializer,
            'Shift': PSRLZER_USER.Shiftserializer,
            'Grade': PSRLZER_USER.Gradeserializer,
            'Bankaccount': PSRLZER_CONT.Bankaccountserializer,
            'Bankaccounttype': PSRLZER_CONT.Bankaccounttypeserializer,
            'Religion': PSRLZER_USER.Religionserializer,
        }
        
        documents=int(len([key for key in requestdata.keys() if 'uploadDocuments' in key])/2)
        documentsindex = []
        photo = None
        for index in range(documents):
            title = request.data.get(f'uploadDocuments[{index}][title]')
            if title:
                title = title.lower()
                if title == 'photo': photo = request.FILES.get(f'uploadDocuments[{index}][attachment]')
                else: documentsindex.append(index)
        
        # If failed to create user then delete instance
        createdInstance = []
        created_by = MODELS_USER.User.objects.get(id=request.user.id)
        response = ghelp().createuser(classOBJpackage, serializerOBJpackage, createdInstance, personalDetails, officialDetails, salaryAndLeaves, photo, created_by)
        if not response['flag']:
            for each in createdInstance:
                if each: each.delete()
        response_message.extend(response['message'])
        
        if response['flag']:
            userinstance = response['userinstance']

            # name = userinstance.get_full_name()
            # cardno = userinstance.uniqueid
            # userid = userinstance.official_id
            # password = ''
            
            # reg_date = userinstance.joining_date
            # valid_date = reg_date + timedelta(days=3650)
            # reg_date = f'{reg_date}'.replace('-', '')
            # valid_date = f'{valid_date}'.replace('-', '')

            # image_paths = [userinstance.photo.path]

            # if 'group_of_device' in officialDetails:
            #     group_list = officialDetails['group_of_device']
            #     if group_list:
            #         devicegroups = MODELS_DEVI.Devicegroup.objects.filter(group__in=group_list)
            #         done_device = []
            #         for devicegroup in devicegroups:
            #             if devicegroup.device.id not in done_device:
            #                 ip = devicegroup.device.deviceip
            #                 uname = devicegroup.device.username
            #                 pword = devicegroup.device.password
            #                 DEVICE().createUserAndTrainImage(ip, name, cardno, userid, image_paths, password, reg_date,  valid_date, uname, pword)
            #                 done_device.append(devicegroup.device.id)
                            
            # Add Role-Permissions
            rolepermission_officialDetails = officialDetails.get('role_permission')
            if isinstance(rolepermission_officialDetails, list):
                if rolepermission_officialDetails:
                    for rolepermissionid in rolepermission_officialDetails:
                        rolepermission = ghelp().getobject(MODELS_USER.Rolepermission, {'id': rolepermissionid})
                        if rolepermission: userinstance.role_permission.add(rolepermission)
                        else: response_message.append(f'rolepermission{rolepermissionid} doesn\'t exist!')


            # ইউজার ক্রিয়েটের পরে।
            ethnicgroup_officialDetails = officialDetails.get('ethnic_group')
            if isinstance(ethnicgroup_officialDetails, list):
                if ethnicgroup_officialDetails:
                    for ethnicgroupid in ethnicgroup_officialDetails:
                        ethnicgroup = ghelp().getobject(MODELS_USER.Ethnicgroup, {'id': ethnicgroupid})
                        if ethnicgroup: ethnicgroup.user.add(userinstance)
                        else: response_message.append(f'ethnic_group{ethnicgroupid} doesn\'t exist!')
            
            if salaryAndLeaves:
                userlist=[userinstance.id]
                manipulate_info = {'created_by': request.user.id, 'updated_by': request.user.id}
                leavepolicy_response = ghelp().assignBulkUserToBulkLeavepolicy(classOBJpackage, salaryAndLeaves.get('leavepolicy'), userlist, manipulate_info)
                if leavepolicy_response['backend_message']:
                    response_message.append('inform backend, data is missing in backend!')
                response_message.extend(leavepolicy_response['message'])
            
            if officialDetails:
                if salaryAndLeaves:
                    employeejobhistorydata = {
                        'user': userinstance.id,
                        'effective_from': officialDetails['joining_date'],
                        'salary': salaryAndLeaves['gross_salary'],
                        'company': officialDetails['company'],
                        'branch': officialDetails['branch'],
                        'department': officialDetails['department'],
                        'designation': officialDetails['designation'],
                        'employee_type': officialDetails['employee_type'],
                        'status_adjustment': [CHOICE.STATUS_ADJUSTMENT[0][1]],
                        'job_status': CHOICE.JOB_STATUS[0][1],
                        'appraisal_by': request.user.id
                    }
                    required_fields = ['user', 'effective_from', 'salary', 'company', 'branch', 'department', 'designation', 'employee_type']
                    _, responsemessage, responsesuccessflag, _ = ghelp().addtocolass(
                        classOBJ=MODELS_JOBR.Employeejobhistory,
                        Serializer=PSRLZER_JOBR.Employeejobhistoryserializer,
                        data=employeejobhistorydata,
                        required_fields=required_fields
                    )
                    if responsesuccessflag == 'error':
                        response_message.extend([f'{each}, therefore couldn\'t add Employeejobhistory!' for each in responsemessage])

            user_records = {
                'emergencycontact_details': {
                    'outer_details': {
                        'userid': userinstance.id,
                        'classOBJ': MODELS_USER.Employeecontact,
                        'Serializer': PSRLZER_USER.Employeecontactserializer,
                        'data': emergencyContact,
                        'allowed_fields': ['name', 'user', 'age', 'phone_no', 'email', 'address', 'relation'],
                        'required_fields': ['name', 'user'],
                        'unique_fields': ['phone_no'],
                        'fields_regex': [
                            {'field': 'phone_no', 'type': 'phonenumber'},
                            {'field': 'email', 'type': 'email'}
                        ]
                    },
                    'inner_details': {
                        'classOBJ': MODELS_CONT.Address,
                        'Serializer': PSRLZER_CONT.Addressserializer,
                        'key': 'address',
                        'allowed_fields': ['alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude'],
                        'required_fields': ['address', 'city', 'state_division', 'country']
                    }
                },
                'academicrecord_details': {
                    'outer_details': {
                        'userid': userinstance.id,
                        'classOBJ': MODELS_USER.Employeeacademichistory,
                        'Serializer': PSRLZER_USER.Employeeacademichistoryserializer,
                        'data': academicRecord,
                        'allowed_fields': ['user', 'board_institute_name', 'certification', 'level', 'score_grade', 'year_of_passing'],
                        'required_fields': ['user', 'board_institute_name', 'certification', 'level', 'score_grade', 'year_of_passing']
                    }
                },
                'previousexperience_details': {
                    'outer_details': {
                        'userid': userinstance.id,
                        'classOBJ': MODELS_USER.Employeeexperiencehistory,
                        'Serializer': PSRLZER_USER.Employeeexperiencehistoryserializer,
                        'data': previousExperience,
                        'allowed_fields': ['user', 'company_name', 'designation', 'address', 'from_date', 'to_date'],
                        'required_fields': ['user', 'company_name', 'designation', 'address', 'from_date', 'to_date'],
                        'fields_regex': [{'field': 'from_date', 'type': 'date'}, {'field': 'to_date', 'type': 'date'}]
                    }
                }
            }
            for key in  user_records.keys():
                user_record_response = ghelp().addUserRecord(information=user_records[key])
                if user_record_response['backend_message']:
                    response_message.append('inform backend, data is missing in backend!')
                response_message.extend(user_record_response['message'])

            # upload documents
            for index in documentsindex:
                title=request.data.get(f'uploadDocuments[{index}][title]')
                attachment = request.FILES.get(f'uploadDocuments[{index}][attachment]')
                if bool(title) and bool(attachment):
                    employeedocsinstance=MODELS_USER.Employeedocs()
                    employeedocsinstance.user=userinstance
                    employeedocsinstance.title=title
                    employeedocsinstance.attachment=attachment
                    employeedocsinstance.save()
                else: response_message.append('either title or document or both are missing!')
            
            department_officialDetails = ghelp().getobject(MODELS_DEPA.Department, {'id': officialDetails.get('department')})
            if department_officialDetails: department_officialDetails.user.add(userinstance)

            response_data = SRLZER_USER.Userserializer(userinstance, many=False).data
            response_successflag = 'success'
            response_status = status.HTTP_201_CREATED
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getprofiledetails(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    user=MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        userserializer = CSRLZER_USER.Userserializer(user.first(), many=False)
        response_data=userserializer.data
        response_successflag='success'
        response_status = status.HTTP_200_OK
    else: response_message.append('user doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateprofilepic(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    photo = request.FILES.get('photo')
    if photo:
        photo_response = ghelp().validateprofilepic(photo)
        if not photo_response['flag']: response_message.extend(photo_response['message'])

        if not response_message:

            profilepicobj = {'photo': photo}
            static_fields = ['photo']

            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                classOBJ=MODELS_USER.User,
                Serializer=PSRLZER_USER.Userserializer,
                id=userid,
                data=profilepicobj,
                static_fields=static_fields
            )
            response_data = responsedata.data if responsesuccessflag == 'success' else {}
            response_message.extend(responsemessage)
            response_successflag = responsesuccessflag
            response_status = responsestatus
    else: response_message.append('photo doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateprofile(request, userid=None):
    requestdata = request.data.copy()

    department = None
    if 'department' in requestdata:
        department = requestdata['department']
        if isinstance(department, str):
            if department.isnumeric(): department = int(department)
    if isinstance(department, int):
        user = MODELS_USER.User.objects.filter(id=userid).first()
        for departmentOBJ in user.departmenttwo.all(): departmentOBJ.user.remove(user)
        department = MODELS_DEPA.Department.objects.filter(id=department)
        if department.exists(): department.first().user.add(user)

        del requestdata['department']
    allowed_fields = ['first_name', 'last_name', 'personal_phone', 'personal_email', 'dob', 'gender', 'blood_group', 'marital_status', 'spouse_name', 'supervisor']
    unique_fields = ['personal_phone', 'personal_email']
    choice_fields = [
        {'name': 'gender', 'type': 'single-string', 'values': [item[1] for item in CHOICE.GENDER]},
        {'name': 'blood_group', 'type': 'single-string', 'values': [item[1] for item in CHOICE.BLOOD_GROUP]},
        {'name': 'marital_status', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MARITAL_STATUS]}
    ]
    fields_regex = [
        {'field': 'personal_phone', 'type': 'phonenumber'},
        {'field': 'personal_email', 'type': 'email'},
        {'field': 'dob', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.User,
        Serializer=PSRLZER_USER.Userserializer,
        id=userid,
        data=requestdata,
        allowed_fields=allowed_fields,
        unique_fields=unique_fields,
        choice_fields=choice_fields,
        fields_regex=fields_regex
    )
    if response_successflag == 'success':
        
        # employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(user=userid).order_by('id')
        # last_employeejobhistory = employeejobhistory.last()
        # while last_employeejobhistory:
        #     if last_employeejobhistory.designation:
        #         if response_data.instance.designation.id != last_employeejobhistory.designation.id:
        #             MODELS_JOBR.Employeejobhistory.objects.filter(id=last_employeejobhistory.id).update(designation=response_data.instance.designation)
        #         break
        #     else: last_employeejobhistory = last_employeejobhistory.previous_id

        # if response_data.instance.joining_date != employeejobhistory.first().effective_from:
        #     MODELS_JOBR.Employeejobhistory.objects.filter(id=employeejobhistory.first().id).update(effective_from=response_data.instance.joining_date)

        response_data = CSRLZER_USER.Userserializer(MODELS_USER.User.objects.get(id=userid), many=False).data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatepersonaldetails(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    present_address_flag = False
    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        requestdata = request.data.copy()

        if_any_opperation_occurred = False
        same_as_present_address = requestdata.get('permanentAddressSameAsPresent', False)
        if same_as_present_address:
            # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস সেইম করে দিতে হবে।
            if user.first().present_address:
                # ইউজারের প্রেজেন্ট এড্রেস আগে থেকেই আছে।
                if user.first().permanent_address:
                    # ইউজারের পার্মানেন্ট এড্রেস আগে থেকেই আছে।
                    if user.first().present_address.id == user.first().permanent_address.id:
                        # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস সেইম।
                        # শুধুমাত্র প্রেজেন্ট এড্রেসকে আপডেট করে দিলেই হবে।
                        present_address = requestdata.get('present_address', {})
                        if present_address:
                            # ডেটা নিয়ে প্রেজেন্ট এড্রেসকে আপডেট করে দিলেই হবে।
                            # রিকোয়েস্টেড অব্জেক্ট থেকে প্রেজেন্ট এড্রেস কী ডিলিট করে দিতে হবে।
                            # রিকোয়েস্টেড অব্জেক্ট থেকে পার্মানেন্ট এড্রেস কী ডিলিট করে দিতে হবে।
                            allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                classOBJ=MODELS_CONT.Address,
                                Serializer=PSRLZER_CONT.Addressserializer,
                                id=user.first().present_address.id,
                                data=present_address,
                                allowed_fields=allowed_fields
                            )
                            if 'present_address' in requestdata: del requestdata['present_address']
                            if 'permanent_address' in requestdata: del requestdata['permanent_address']
                        else:
                            # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেসকে নাল করে দিতে হবে।
                            requestdata.update({'present_address': None, 'permanent_address': None})
                        if_any_opperation_occurred = True
                    else:
                        # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস সেইম না।
                        # পার্মানেন্ট এড্রেস ডিলিট করতে হবে।
                        # প্রেজেন্ট এড্রেসকে আপডেট করে সেই আইডি পার্মানেন্ট এড্রেসে এসাইন করতে হবে।।
                        
                        user.first().permanent_address.delete()
                        present_address = requestdata.get('present_address', {})
                        if present_address:
                            # প্রেজেন্ট এড্রেসকে আপডেট করে দিতে হবে।
                            # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেসকে সেইম করে দিতে হবে।
                            # রিকোয়েস্টেড অব্জেক্ট থেকে প্রেজেন্ট এড্রেস কী ডিলিট করে দিতে হবে।
                            # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে প্রেজেন্ট এড্রেসের আইডি দিতে হবে।
                            allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                classOBJ=MODELS_CONT.Address,
                                Serializer=PSRLZER_CONT.Addressserializer,
                                id=user.first().present_address.id,
                                data=present_address,
                                allowed_fields=allowed_fields
                            )
                            if 'present_address' in requestdata: del requestdata['present_address']
                            requestdata.update({'permanent_address': user.first().present_address.id})
                        else:
                            # প্রেজেন্ট এড্রেস ডিলিট করতে হবে।
                            # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেসকে নাল করে দিতে হবে।
                            # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                            # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                            user.first().present_address.delete()
                            requestdata.update({'present_address': None, 'permanent_address': None})
                        if_any_opperation_occurred = True
                else:
                    # ইউজারের পার্মানেন্ট এড্রেস নাই।
                    present_address = requestdata.get('present_address', {})
                    if present_address:
                        # প্রেজেন্ট এড্রেসকে আপডেট করে দিতে হবে।
                        # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস দুটোকেই আপডেট করে দিতে হবে।
                        # রিকোয়েস্টেড অব্জেক্ট থেকে প্রেজেন্ট এড্রেস কী ডিলিট করে দিতে হবে।
                        # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে প্রেজেন্ট এড্রেসের আইডি দিতে হবে।

                        allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                            classOBJ=MODELS_CONT.Address,
                            Serializer=PSRLZER_CONT.Addressserializer,
                            id=user.first().present_address.id,
                            data=present_address,
                            allowed_fields=allowed_fields
                        )
                        if 'present_address' in requestdata: del requestdata['present_address']
                        requestdata.update({'permanent_address': user.first().present_address.id}) 
                    else:
                        # প্রেজেন্ট এড্রেসকে ডিলিট হবে।
                        # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস দুটোকেই নান করতে হবে।

                        # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                        # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                        user.first().present_address.delete()
                        requestdata.update({'present_address': None, 'permanent_address': None})
                    if_any_opperation_occurred = True
            else:
                # ইউজারের প্রেজেন্ট এড্রেস নাই।
                # ইউজারের পার্মানেন্ট এড্রেস চেক করতে হবে থাকলে ডিলিট করে দিতে হবে।
                
                permanent_address = user.first().permanent_address
                if permanent_address: permanent_address.delete()

                present_address = requestdata.get('present_address', {})
                if present_address:
                    # প্রেজেন্ট এড্রেস ক্রিয়েট করতে হবে।
                    # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস দুটোকেই সেইম করে দিতে হবে।

                    # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে প্রেজেন্ট এড্রেসের আইডি দিতে হবে।
                    # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে প্রেজেন্ট এড্রেসের আইডি দিতে হবে।
                    
                    allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                    required_fields = ['address', 'city', 'state_division', 'country']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_CONT.Address,
                        Serializer=PSRLZER_CONT.Addressserializer,
                        data=present_address,
                        allowed_fields=allowed_fields,
                        required_fields=required_fields
                    )
                    if responsesuccessflag == 'success': requestdata.update({'present_address': responsedata.instance.id, 'permanent_address': responsedata.instance.id})
                else:
                    # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস দুটোকেই নান করে দিতে হবে।
                    # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                    # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                    requestdata.update({'present_address': None, 'permanent_address': None})
                if_any_opperation_occurred = True
        else:
            # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস সেইম হতে পারবে না।
            if user.first().present_address:
                # ইউজারের প্রেজেন্ট এড্রেস আছে।
                if user.first().permanent_address:
                    # ইউজারের প্রেজেন্ট এড্রেস আছে।
                    # ইউজারের পার্মানেন্ট এড্রেস আছে।
                    if user.first().present_address.id == user.first().permanent_address.id:
                        # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস সেইম।
                        # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস সেইম হতে পারবে না.
                        # প্রেজেন্ট এড্রেসকে আপডেট করতে হবে।
                        # পার্মানেন্ট এড্রেস ক্রিয়েট করতে হবে।
                        # রিকোয়েস্টেড অব্জেক্টে থেকে প্রেজেন্ট এড্রেসের ফিল্ড মুছে ফেলতে হবে।
                        # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে পার্মানেন্ট এড্রেসের আইডি দিতে হবে।
                        present_address = requestdata.get('present_address', {})
                        if present_address:
                            # প্রেজেন্ট এড্রেসকে আপডেট করে দিতে হবে।
                            allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                classOBJ=MODELS_CONT.Address,
                                Serializer=PSRLZER_CONT.Addressserializer,
                                id=user.first().present_address.id,
                                data=present_address,
                                allowed_fields=allowed_fields
                            )
                            if 'present_address' in requestdata: del requestdata['present_address']
                        else:
                            # আগের প্রেজেন্ট এড্রেসকে ডিলিট করতে হবে।
                            # প্রেজেন্ট এড্রেসকে নাল করে দিতে হবে।
                            present_address = user.first().present_address
                            present_address.delete()
                            requestdata.update({'present_address': None})
                            
                        permanent_address = requestdata.get('permanent_address', {})
                        if permanent_address:
                            # ডাটা নিয়ে পার্মানেন্ট এড্রেসকে ক্রিয়েট করতে হবে।

                            allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                            required_fields = ['address', 'city', 'state_division', 'country']
                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                classOBJ=MODELS_CONT.Address,
                                Serializer=PSRLZER_CONT.Addressserializer,
                                data=present_address,
                                allowed_fields=allowed_fields,
                                required_fields=required_fields
                            )
                            if responsesuccessflag == 'success': requestdata.update({'permanent_address': responsedata.instance.id})
                        else:
                            # পার্মানেন্ট এড্রেসকে নাল করে দিতে হবে।
                            requestdata.update({'permanent_address': None})
                        if_any_opperation_occurred = True
                    else:
                        # প্রেজেন্ট এড্রেস এবং পার্মানেন্ট এড্রেস সেইম না।
                        present_address = requestdata.get('present_address', {})
                        if present_address:
                            # প্রেজেন্ট এড্রেসকে আপডেট করতে হবে।
                            # রিকোয়েস্টেড অব্জেক্টে থেকে প্রেজেন্ট এড্রেসের ফিল্ড মুছে ফেলতে হবে।
                            allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                classOBJ=MODELS_CONT.Address,
                                Serializer=PSRLZER_CONT.Addressserializer,
                                id=user.first().present_address.id,
                                data=present_address,
                                allowed_fields=allowed_fields
                            )
                            if 'present_address' in requestdata: del requestdata['present_address']
                        else:
                            # প্রেজেন্ট এড্রেসকে নাল করে দিতে হবে।
                            # প্রেজেন্ট এড্রেসকে ডিলিট করতে হবে।
                            # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                            present_address = user.first().present_address
                            present_address.delete()
                            requestdata.update({'present_address': None})
                            
                        permanent_address = requestdata.get('permanent_address', {})
                        if permanent_address:
                            # পার্মানেন্ট এড্রেসকে আপডেট করতে হবে।
                            # রিকোয়েস্টেড অব্জেক্টে থেকে পার্মানেন্ট এড্রেসের ফিল্ড মুছে ফেলতে হবে।
                            allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                classOBJ=MODELS_CONT.Address,
                                Serializer=PSRLZER_CONT.Addressserializer,
                                id=user.first().permanent_address.id,
                                data=permanent_address,
                                allowed_fields=allowed_fields
                            )
                            if 'permanent_address' in requestdata: del requestdata['permanent_address']
                        else:
                            # পার্মানেন্ট এড্রেসকে নাল করে দিতে হবে।
                            # পার্মানেন্ট এড্রেসকে ডিলিট করতে হবে।
                            # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                            permanent_address = user.first().permanent_address
                            permanent_address.delete()
                            requestdata.update({'permanent_address': None})
                        if_any_opperation_occurred = True
                else:
                    # ইউজারের প্রেজেন্ট এড্রেস আছে।
                    # ইউজারের পার্মানেন্ট এড্রেস নাই।
                    present_address = requestdata.get('present_address', {})
                    if present_address:
                        # প্রেজেন্ট এড্রেসকে আপডেট করতে হবে।
                        # রিকোয়েস্টেড অব্জেক্ট থেকে প্রেজেন্ট এড্রেসের ফিল্ড মুছে ফেলতে হবে।
                        allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                            classOBJ=MODELS_CONT.Address,
                            Serializer=PSRLZER_CONT.Addressserializer,
                            id=user.first().present_address.id,
                            data=present_address,
                            allowed_fields=allowed_fields
                        )
                        if 'present_address' in requestdata: del requestdata['present_address']
                    else:
                        # প্রেজেন্ট এড্রেসকে নাল করতে হবে।
                        # প্রেজেন্ট এড্রেসকে ডিলিট করতে হবে।
                        # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে নান দিতে হবে।
                        present_address = user.first().present_address
                        present_address.delete()
                        requestdata.update({'present_address': None})
                    
                    permanent_address = requestdata.get('permanent_address', {})
                    if permanent_address:
                        # পার্মানেন্ট এড্রেসকে ক্রিয়েট করতে হবে।
                        allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                        required_fields = ['address', 'city', 'state_division', 'country']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_CONT.Address,
                            Serializer=PSRLZER_CONT.Addressserializer,
                            data=permanent_address,
                            allowed_fields=allowed_fields,
                            required_fields=required_fields
                        )
                        if responsesuccessflag == 'success': requestdata.update({'permanent_address': responsedata.instance.id})
                    if_any_opperation_occurred = True
            else:
                # ইউজারের প্রেজেন্ট এড্রেস নাই।
                if user.first().permanent_address:
                    # ইউজারের প্রেজেন্ট এড্রেস নাই।
                    # ইউজারের পার্মানেন্ট এড্রেস আছে।
                    present_address = requestdata.get('present_address', {})
                    if present_address:
                        # প্রেজেন্ট এড্রেসকে ক্রিয়েট করতে হবে।
                        # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে প্রেজেন্ট এড্রেসের আইডি দিতে হবে।

                        allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                        required_fields = ['address', 'city', 'state_division', 'country']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_CONT.Address,
                            Serializer=PSRLZER_CONT.Addressserializer,
                            data=present_address,
                            allowed_fields=allowed_fields,
                            required_fields=required_fields
                        )
                        if responsesuccessflag == 'success': requestdata.update({'present_address': responsedata.instance.id})
                        
                    permanent_address = requestdata.get('permanent_address', {})
                    if permanent_address:
                        # পার্মানেন্ট এড্রেসকে আপডেট করতে হবে।
                        allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                            classOBJ=MODELS_CONT.Address,
                            Serializer=PSRLZER_CONT.Addressserializer,
                            id=user.first().permanent_address.id,
                            data=permanent_address,
                            allowed_fields=allowed_fields
                        )
                        if 'permanent_address' in requestdata: del requestdata['permanent_address']
                    else:
                        # পার্মানেন্ট এড্রেসকে নাল করতে হবে।
                        # পার্মানেন্ট এড্রেসকে ডিলিট করতে হবে।
                        permanent_address = user.first().permanent_address
                        permanent_address.delete()
                        requestdata.update({'permanent_address': None})
                    if_any_opperation_occurred = True
                else:
                    # ইউজারের প্রেজেন্ট এড্রেস নাই।
                    # ইউজারের পার্মানেন্ট এড্রেস নাই।
                    # প্রেজেন্ট এড্রেস ক্রিয়েট করতে হবে।
                    # পার্মানেন্ট এড্রেস ক্রিয়েট করতে হবে।
                    # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে প্রেজেন্ট এড্রেসের আইডি দিতে হবে।
                    # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে পার্মানেন্ট এড্রেসের আইডি দিতে হবে।
                    
                    present_address = requestdata.get('present_address', {})
                    if present_address:
                        # প্রেজেন্ট এড্রেসকে ক্রিয়েট করতে হবে।
                        # রিকোয়েস্টেড অব্জেক্টে প্রেজেন্ট এড্রেসের ফিল্ডে প্রেজেন্ট এড্রেসের আইডি দিতে হবে।

                        allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                        required_fields = ['address', 'city', 'state_division', 'country']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_CONT.Address,
                            Serializer=PSRLZER_CONT.Addressserializer,
                            data=present_address,
                            allowed_fields=allowed_fields,
                            required_fields=required_fields
                        )
                        if responsesuccessflag == 'success':
                            requestdata.update({'present_address': responsedata.instance.id})
                            if_any_opperation_occurred = True
                        
                    permanent_address = requestdata.get('permanent_address', {})
                    if permanent_address:
                        # পার্মানেন্ট এড্রেসকে ক্রিয়েট করতে হবে।
                        # রিকোয়েস্টেড অব্জেক্টে পার্মানেন্ট এড্রেসের ফিল্ডে পার্মানেন্ট এড্রেসের আইডি দিতে হবে।

                        allowed_fields=['name', 'alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                        required_fields = ['address', 'city', 'state_division', 'country']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_CONT.Address,
                            Serializer=PSRLZER_CONT.Addressserializer,
                            data=permanent_address,
                            allowed_fields=allowed_fields,
                            required_fields=required_fields
                        )
                        if responsesuccessflag == 'success':
                            requestdata.update({'permanent_address': responsedata.instance.id})
                            if_any_opperation_occurred = True
        
        if requestdata:
            allowed_fields = ['fathers_name', 'mothers_name', 'nationality', 'religion', 'nid_passport_no', 'tin_no', 'present_address', 'permanent_address']
            unique_fields = ['nid_passport_no', 'tin_no']
            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                classOBJ=MODELS_USER.User,
                Serializer=PSRLZER_USER.Userserializer,
                id=userid,
                data=requestdata,
                allowed_fields=allowed_fields,
                unique_fields=unique_fields
            )
            if responsesuccessflag == 'success':
                response_data = CSRLZER_USER.Userserializer(MODELS_USER.User.objects.get(id=userid), many=False).data
            elif responsesuccessflag == 'error':
                response_message.extend(responsemessage)
            response_successflag = responsesuccessflag
            response_status = responsestatus
        else:
            if if_any_opperation_occurred:
                response_successflag = 'success'
                response_status = status.HTTP_200_OK

    else: response_message.append('user doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateofficialdetails(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        requestdata = request.data

        # app_name = 'user'
        # model = 'ethnicgroup'
        # models_field_name = 'user'

        # first_table = f'{app_name}_{model}'
        # second_table = f'{app_name}_{model}_{models_field_name}'
        # second_table_select = f'{model}_id'
        # second_table_where = f'{user}_id'
        # sql = '''
        # SELECT *
        # FROM user_ethnicgroup
        # WHERE id IN (
        #     (
        #         SELECT ethnicgroup_id
        #         FROM user_ethnicgroup_user
        #         WHERE user_id=11
        #     )
        # );
        # '''

        
        
        # 'ethnic_group'
        if 'ethnic_group' in requestdata:
            new_ethnicgroupids = requestdata['ethnic_group']
            if isinstance(new_ethnicgroupids, list):
                add_ethnicgroups = []
                remove_ethnicgroups = []

                previous_ethnicgroups = {f'{each.id}': each for each in user.first().ethnicgroup_user.all()}
                new_ethnicgroupids = [str(ethnicgroupid) for ethnicgroupid in new_ethnicgroupids]
                for new_ethnicgroupid in new_ethnicgroupids:
                    if new_ethnicgroupid not in previous_ethnicgroups:
                        ethnicgroup = MODELS_USER.Ethnicgroup.objects.filter(id=new_ethnicgroupid)
                        if ethnicgroup.exists(): add_ethnicgroups.append(ethnicgroup.first())
                for id in previous_ethnicgroups.keys():
                    if id not in new_ethnicgroupids:
                        ethnicgroup = MODELS_USER.Ethnicgroup.objects.filter(id=id)
                        if ethnicgroup.exists(): remove_ethnicgroups.append(ethnicgroup.first())
                for remove_ethnicgroup in remove_ethnicgroups: remove_ethnicgroup.user.remove(user.first())
                for add_ethnicgroup in add_ethnicgroups: add_ethnicgroup.user.add(user.first())
            else: response_message.append('please provide ethnic_group as list!')

        allowed_fields = ['official_email', 'official_phone', 'shift', 'grade', 'role_permission', 'official_note', 'expense_approver', 'leave_approver', 'shift_request_approver']
        unique_fields = ['official_email', 'official_phone']
        choice_fields = [
            {'name': 'employee_type', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]}
        ]
        fields_regex = [
            {'field': 'official_email', 'type': 'email'},
            {'field': 'official_phone', 'type': 'phonenumber'},
            {'field': 'joining_date', 'type': 'date'}
        ]
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
            classOBJ=MODELS_USER.User,
            Serializer=PSRLZER_USER.Userserializer,
            id=userid,
            data=requestdata,
            allowed_fields=allowed_fields,
            unique_fields=unique_fields,
            choice_fields=choice_fields,
            fields_regex=fields_regex
        )
        if responsesuccessflag == 'success':
            userserializer = CSRLZER_USER.Userserializer(MODELS_USER.User.objects.get(id=userid), many=False)

            # employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(user=user.first().id).order_by('id')

            # if userserializer.instance.joining_date != employeejobhistory.first().effective_from:
            #     MODELS_JOBR.Employeejobhistory.objects.filter(id=employeejobhistory.first().id).update(effective_from=userserializer.instance.joining_date)
            
            # employeejobhistory = employeejobhistory.last()
            # # 'company'
            # if 'company' in requestdata:
            #     companyid = requestdata['company']
            #     company = MODELS_COMP.Company.objects.filter(id=companyid)
            #     if company.exists():
            #         company = company.first()
            #         if employeejobhistory.department:

            #             while employeejobhistory:
            #                 if employeejobhistory.company:
            #                     if company.id != employeejobhistory.company.id:
            #                         employeejobhistory.department.user.remove(user.first())
            #                         MODELS_JOBR.Employeejobhistory.objects.filter(id=employeejobhistory.id).update(company=company, branch=None, department=None)
            #                     break
            #                 else: employeejobhistory = employeejobhistory.previous_id
            # # 'branch'
            # if 'branch' in requestdata:
            #     branchid = requestdata['branch']
            #     branch = MODELS_BRAN.Branch.objects.filter(id=branchid)
            #     if branch.exists():
            #         branch = branch.first()
            #         if employeejobhistory.department:
            #             while employeejobhistory:
            #                 if employeejobhistory.branch:
            #                     if branch.id != employeejobhistory.branch.id:
            #                         employeejobhistory.department.user.remove(user.first())
            #                         MODELS_JOBR.Employeejobhistory.objects.filter(id=employeejobhistory.id).update(branch=branch, department=None)
            #                     break
            #                 else: employeejobhistory = employeejobhistory.previous_id
            response_data = userserializer.data
        
        response_message.extend(responsemessage)
        response_successflag = responsesuccessflag
        response_status = responsestatus
    else: response_message.append('user doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatesalaryleaves(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        requestdata = request.data.copy()

        if 'bankaccount' in requestdata:
            if user.first().bank_account:
                bankaccount = requestdata['bankaccount']

                if user.first().bank_account.address:
                    if 'address' in bankaccount:
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                            classOBJ=MODELS_CONT.Address,
                            Serializer=PSRLZER_CONT.Addressserializer,
                            id=user.first().bank_account.address.id,
                            data=bankaccount['address']
                        )
                        if responsesuccessflag == 'error':
                            response_message.extend([f'bank account address\'s {each}' for each in responsemessage])
                            del bankaccount['address']
                        elif responsesuccessflag == 'success': del bankaccount['address']
                else:
                    if 'id' in bankaccount['address']: del bankaccount['address']['id']
                    required_fields = ['address', 'city', 'state_division', 'country']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_CONT.Address,
                        Serializer=PSRLZER_CONT.Addressserializer,
                        data=bankaccount['address'],
                        required_fields=required_fields
                    )
                    if responsesuccessflag == 'success': bankaccount.update({'address': responsedata.data['id']})
                    elif responsesuccessflag == 'error':
                        response_message.extend(responsemessage)
                        del bankaccount['address']

                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                    classOBJ=MODELS_CONT.Bankaccount,
                    Serializer=PSRLZER_CONT.Bankaccountserializer,
                    id=user.first().bank_account.id,
                    data=bankaccount
                )
                if responsesuccessflag == 'success': bankaccount.update({'bankaccount': responsedata.data['id']})
                elif responsesuccessflag == 'error':
                    del bankaccount['bankaccount']
                    response_message.extend([f'Bank Account\'s {each}' for each in responsemessage])
            else:
                classOBJpackage = {'Address': MODELS_CONT.Address, 'Bankaccount': MODELS_CONT.Bankaccount}
                serializerOBJpackage = {'Address': PSRLZER_CONT.Addressserializer, 'Bankaccount': PSRLZER_CONT.Bankaccountserializer}

                addbankaccountdetails=ghelp().addbankaccount(classOBJpackage, serializerOBJpackage, requestdata['bankaccount'])
                if addbankaccountdetails['flag']: requestdata.update({'bankaccount': addbankaccountdetails['instance'].id})
                else:
                    response_message.extend(addbankaccountdetails['message'])
                    del requestdata['bankaccount']
        
        # leavepolicy
        if 'leavepolicy' in requestdata:
            new_leavepolicyids = requestdata['leavepolicy']
            if isinstance(new_leavepolicyids, list):
                fiscalyear_response = ghelp().findFiscalyear(MODELS_SETT.Generalsettings)
                if fiscalyear_response['fiscalyear']:
                    add_leavepolicys = []
                    remove_leavepolicys = []

                    previous_leavepolicys = {f'{each.id}': each for each in MODELS_LEAV.Leavepolicyassign.objects.filter(user=user.first().id)}
                    new_leavepolicyids = [str(leavepolicyid) for leavepolicyid in new_leavepolicyids]
                    for new_leavepolicyid in new_leavepolicyids:
                        if new_leavepolicyid not in previous_leavepolicys:
                            leavepolicy = MODELS_LEAV.Leavepolicy.objects.filter(id=new_leavepolicyid)
                            if leavepolicy.exists(): add_leavepolicys.append(leavepolicy.first())
                    for id in previous_leavepolicys.keys():
                        if id not in new_leavepolicyids:
                            leavepolicy = MODELS_LEAV.Leavepolicy.objects.filter(id=id)
                            if leavepolicy.exists(): remove_leavepolicys.append(leavepolicy.first())

                    for remove_leavepolicy in remove_leavepolicys:
                        leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user.first(), leavepolicy=remove_leavepolicy)
                        if leavesummary.exists():
                            if leavesummary.first().total_consumed == 0:
                                leaverequests = MODELS_LEAV.Leaverequest.objects.filter(user=user.first(), leavepolicy=remove_leavepolicy)
                                if leaverequests.exists(): leaverequests.delete()
                                leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user.first(), leavepolicy=remove_leavepolicy)
                                if leavepolicyassign.exists(): leavepolicyassign.delete()
                                leavesummary.delete()
                            else:
                                response_message.append(f'couldn\'t remove {remove_leavepolicy.name} leavepolicy({remove_leavepolicy.id}), because you have already consumed!')
                        else:
                            leaverequests = MODELS_LEAV.Leaverequest.objects.filter(user=user.first(), leavepolicy=remove_leavepolicy)
                            if leaverequests.exists(): leaverequests.delete()
                            leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user.first(), leavepolicy=remove_leavepolicy)
                            if leavepolicyassign.exists(): leavepolicyassign.delete()
                    
                    for add_leavepolicy in add_leavepolicys:
                        # create leavepolicyassign 
                        leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user.first(), leavepolicy=add_leavepolicy)
                        if not leavepolicyassign.exists():
                            MODELS_LEAV.Leavepolicyassign.objects.create(user=user.first(), leavepolicy=add_leavepolicy)
                        
                        leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user.first(), leavepolicy=add_leavepolicy)
                        if not leavesummary.exists():
                            MODELS_LEAV.Leavesummary.objects.create(
                                user=user.first(),
                                leavepolicy=add_leavepolicy,
                                fiscal_year=fiscalyear_response['fiscalyear'],
                                total_allocation=add_leavepolicy.allocation_days,
                                total_consumed=0,
                                total_left=add_leavepolicy.allocation_days
                            )

                else: response_message.extend(fiscalyear_response['message'])
            else: response_message.append('please provide leavepolicy as list!')
            del requestdata['leavepolicy']

        allowed_fields = ['payment_in', 'bankaccount']
        choice_fields = [{'name': 'payment_in', 'type': 'single-string', 'values': [item[1] for item in CHOICE.PAYMENT_IN]}]
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
            classOBJ=MODELS_USER.User,
            Serializer=PSRLZER_USER.Userserializer,
            id=userid,
            data=requestdata,
            allowed_fields=allowed_fields,
            choice_fields=choice_fields
        )
        if responsesuccessflag == 'success':
            response_data = CSRLZER_USER.Userserializer(MODELS_USER.User.objects.get(id=userid), many=False).data
            response_successflag=responsesuccessflag
            response_status=responsestatus
        elif responsesuccessflag == 'error':
            response_successflag=responsesuccessflag
            response_message.extend(responsemessage)
            response_status=responsestatus
    else: response_message.append('user doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateemergencycontact(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        requestdata = request.data.copy()
        successfully_deleted = 0
        successfully_updated = 0
        successfully_addeded = 0

        if 'delete' in requestdata:
            deleteemergencycontacts = requestdata['delete']
            if isinstance(deleteemergencycontacts, list):
                for index, deleteemergencycontactid in enumerate(deleteemergencycontacts):
                    employeecontact = MODELS_USER.Employeecontact.objects.filter(id=deleteemergencycontactid)
                    if employeecontact.exists():
                        if employeecontact.first().user.id == userid:
                            employeecontact.delete()
                            successfully_deleted += 1
                        else: response_message.append(f'{user.first().get_full_name()}({userid}) has no Employeecontact having {deleteemergencycontactid} id(index {index})!')
                    else: response_message.append(f'couldn\'t found any employeecontact with this id {deleteemergencycontactid}!')
            else: response_message.append('delete must be array(list)!')

        if 'update' in requestdata:
            updateemergencycontacts = requestdata['update']
            if isinstance(updateemergencycontacts, list):
                for index, updateemergencycontact in enumerate(updateemergencycontacts):
                    if 'id' in updateemergencycontact:
                        updateemergencycontactid = updateemergencycontact['id']
                        del updateemergencycontact['id']
                        employeecontact = MODELS_USER.Employeecontact.objects.filter(id=updateemergencycontactid)
                        if employeecontact.exists():
                            if userid == employeecontact.first().user.id:
                                allowed_fields=['name', 'user', 'age', 'phone_no', 'email', 'address', 'relation']
                                fields_regex = [{'field': 'phone_no', 'type': 'phonenumber'}, {'field': 'email', 'type': 'email'}]
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                    classOBJ=MODELS_USER.Employeecontact,
                                    Serializer=PSRLZER_USER.Employeecontactserializer,
                                    id=updateemergencycontactid,
                                    data=updateemergencycontact,
                                    allowed_fields=allowed_fields,
                                    fields_regex=fields_regex
                                )
                                if responsesuccessflag == 'error':
                                    response_message.extend([f'{index}\'th update({updateemergencycontactid}) - {message}' for message in responsemessage])
                                elif responsesuccessflag == 'success': successfully_updated += 1
                            else: response_message.append(f'{user.first().get_full_name()}({userid}) has no Employeecontact having {updateemergencycontactid} id(index {index})!')
                        else: response_message.append(f'{index}\'th emergencycontact doesn\'t exist!')
                    else: response_message.append(f'please provide emergencycontact\'s id to update, check {index}\'th data!')
            else: response_message.append('update must be array(list)!')
        
        if 'add' in requestdata:
            addemergencycontacts = requestdata['add']
            if isinstance(addemergencycontacts, list):
                for index, addemergencycontact in enumerate(addemergencycontacts):
                    if 'user' not in addemergencycontact: addemergencycontact.update({'user': userid})

                    allowed_fields=['name', 'user', 'age', 'phone_no', 'email', 'address', 'relation']
                    required_fields = ['name', 'user']
                    fields_regex = [{'field': 'phone_no', 'type': 'phonenumber'}, {'field': 'email', 'type': 'email'}]
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_USER.Employeecontact, 
                        Serializer=PSRLZER_USER.Employeecontactserializer, 
                        data=updateemergencycontact,
                        allowed_fields=allowed_fields,
                        required_fields=required_fields,
                        fields_regex=fields_regex
                    )
                    if responsesuccessflag == 'error':
                        response_message.extend([f'{index}\'th add - {message}' for message in responsemessage])
                    elif responsesuccessflag == 'success': successfully_addeded += 1
            else: response_message.append('add must be array(list)!')
    
    if successfully_deleted + successfully_updated + successfully_addeded > 0:
        response_successflag = 'success'
        response_status = status.HTTP_200_OK
        response_data = CSRLZER_USER.Userserializer(MODELS_USER.User.objects.get(id=userid), many=False).data

    else: response_message.append('user doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateeducation(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        requestdata = request.data.copy()
        successfully_deleted = 0
        successfully_updated = 0
        successfully_addeded = 0

        if 'delete' in requestdata:
            deleteeducations = requestdata['delete']
            if isinstance(deleteeducations, list):
                for index, deleteeducationid in enumerate(deleteeducations):
                    employeeacademichistory = MODELS_USER.Employeeacademichistory.objects.filter(id=deleteeducationid)
                    if employeeacademichistory.exists():
                        if employeeacademichistory.first().user.id == userid:
                            employeeacademichistory.delete()
                            successfully_deleted += 1
                        else: response_message.append(f'{user.first().get_full_name()}({userid}) has no Employeeacademichistory having {deleteeducationid} id(index {index})!')
                    else: response_message.append(f'couldn\'t found any employeeacademichistory with this id {deleteeducationid}!')
            else: response_message.append('delete must be array(list)!')

        if 'update' in requestdata:
            updateeducations = requestdata['update']
            if isinstance(updateeducations, list):
                for index, updateeducation in enumerate(updateeducations):
                    if 'id' in updateeducation:
                        updateeducationid = updateeducation['id']
                        del updateeducation['id']
                        employeeacademichistory = MODELS_USER.Employeeacademichistory.objects.filter(id=updateeducationid)
                        if employeeacademichistory.exists():
                            if userid == employeeacademichistory.first().user.id:
                                allowed_fields=['user', 'board_institute_name', 'certification', 'level', 'score_grade', 'year_of_passing']
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                    classOBJ=MODELS_USER.Employeeacademichistory,
                                    Serializer=PSRLZER_USER.Employeeacademichistoryserializer,
                                    id=updateeducationid,
                                    data=updateeducation,
                                    allowed_fields=allowed_fields
                                )
                                if responsesuccessflag == 'error':
                                    response_message.extend([f'{index}\'th update({updateeducationid}) - {message}' for message in responsemessage])
                                elif responsesuccessflag == 'success': successfully_updated += 1
                            else: response_message.append(f'{user.first().get_full_name()}({userid}) has no Employeeacademichistory having {updateeducationid} id(index {index})!')
                        else: response_message.append(f'{index}\'th employeeacademichistory doesn\'t exist!')
                    else: response_message.append(f'please provide employeeacademichistory\'s id to update, check {index}\'th data!')
            else: response_message.append('update must be array(list)!')
        
        if 'add' in requestdata:
            addeducations = requestdata['add']
            if isinstance(addeducations, list):
                for index, addeducation in enumerate(addeducations):
                    if 'user' not in addeducation: addeducation.update({'user': userid})

                    allowed_fields=['user', 'board_institute_name', 'certification', 'level', 'score_grade', 'year_of_passing']
                    required_fields = ['user', 'board_institute_name', 'certification', 'level', 'score_grade', 'year_of_passing']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_USER.Employeeacademichistory, 
                        Serializer=PSRLZER_USER.Employeeacademichistoryserializer, 
                        data=addeducation,
                        allowed_fields=allowed_fields,
                        required_fields=required_fields
                    )
                    if responsesuccessflag == 'error':
                        response_message.extend([f'{index}\'th add - {message}' for message in responsemessage])
                    elif responsesuccessflag == 'success': successfully_addeded += 1
            else: response_message.append('add must be array(list)!')
    
    if successfully_deleted + successfully_updated + successfully_addeded > 0:
        response_successflag = 'success'
        response_status = status.HTTP_200_OK
        response_data = CSRLZER_USER.Userserializer(MODELS_USER.User.objects.get(id=userid), many=False).data

    else: response_message.append('user doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateexperience(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        requestdata = request.data.copy()
        successfully_deleted = 0
        successfully_updated = 0
        successfully_addeded = 0

        if 'delete' in requestdata:
            deleteexperiences = requestdata['delete']
            if isinstance(deleteexperiences, list):
                for index, deleteexperienceid in enumerate(deleteexperiences):
                    employeeexperiencehistory = MODELS_USER.Employeeexperiencehistory.objects.filter(id=deleteexperienceid)
                    if employeeexperiencehistory.exists():
                        if employeeexperiencehistory.first().user.id == userid:
                            employeeexperiencehistory.delete()
                            successfully_deleted += 1
                        else: response_message.append(f'{user.first().get_full_name()}({userid}) has no Employeeexperiencehistory having {deleteexperienceid} id(index {index})!')
                    else: response_message.append(f'couldn\'t found any deleteexperience with this id {deleteexperienceid}!')
            else: response_message.append('delete must be array(list)!')

        if 'update' in requestdata:
            updateexperiences = requestdata['update']
            if isinstance(updateexperiences, list):
                for index, updateexperience in enumerate(updateexperiences):
                    if 'id' in updateexperience:
                        updateexperienceid = updateexperience['id']
                        del updateexperience['id']
                        employeeexperiencehistory = MODELS_USER.Employeeexperiencehistory.objects.filter(id=updateexperienceid)
                        if employeeexperiencehistory.exists():
                            if userid == employeeexperiencehistory.first().user.id:
                                allowed_fields=['user', 'company_name', 'designation', 'address', 'from_date', 'to_date']
                                fields_regex = [{'field': 'from_date', 'type': 'date'}, {'field': 'to_date', 'type': 'date'}]
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                    classOBJ=MODELS_USER.Employeeexperiencehistory,
                                    Serializer=PSRLZER_USER.Employeeexperiencehistoryserializer,
                                    id=updateexperienceid,
                                    data=updateexperience,
                                    allowed_fields=allowed_fields,
                                    fields_regex=fields_regex
                                )
                                if responsesuccessflag == 'error':
                                    response_message.extend([f'{index}\'th update({updateexperienceid}) - {message}' for message in responsemessage])
                                elif responsesuccessflag == 'success': successfully_updated += 1
                            else: response_message.append(f'{user.first().get_full_name()}({userid}) has no Employeeexperiencehistory having {updateexperienceid} id(index {index})!')
                        else: response_message.append(f'{index}\'th employeeexperiencehistory doesn\'t exist!')
                    else: response_message.append(f'please provide employeeexperiencehistory\'s id to update, check {index}\'th data!')
            else: response_message.append('update must be array(list)!')
        
        if 'add' in requestdata:
            addexperiences = requestdata['add']
            if isinstance(addexperiences, list):
                for index, addexperience in enumerate(addexperiences):
                    if 'user' not in addexperience: addexperience.update({'user': userid})

                    allowed_fields=['user', 'company_name', 'designation', 'address', 'from_date', 'to_date']
                    fields_regex = [{'field': 'from_date', 'type': 'date'}, {'field': 'to_date', 'type': 'date'}]
                    required_fields = ['user', 'company_name', 'designation', 'from_date', 'to_date']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_USER.Employeeexperiencehistory, 
                        Serializer=PSRLZER_USER.Employeeexperiencehistoryserializer, 
                        data=addexperience,
                        allowed_fields=allowed_fields,
                        required_fields=required_fields,
                        fields_regex=fields_regex
                    )
                    if responsesuccessflag == 'error':
                        response_message.extend([f'{index}\'th add - {message}' for message in responsemessage])
                    elif responsesuccessflag == 'success': successfully_addeded += 1
            else: response_message.append('add must be array(list)!')
    
    if successfully_deleted + successfully_updated + successfully_addeded > 0:
        response_successflag = 'success'
        response_status = status.HTTP_200_OK
        response_data = CSRLZER_USER.Userserializer(MODELS_USER.User.objects.get(id=userid), many=False).data

    else: response_message.append('user doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatedocuments(request, userid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    user = MODELS_USER.User.objects.filter(id=userid)

    if user.exists():

        requestdata = dict(request.data)
        requestdata.update({'abcdef[abcdef]': ['abcdef']})
        options = {'allow_blank': True, 'allow_empty': False}
        
        form = NestedForm(requestdata, **options)
        form.is_nested(raise_exception=True)

        requestdata = form.data
        if 'documents' in requestdata:
            requestdata = requestdata['documents']
            requestdata = ghelp().prepareData(requestdata, 'userdocument')
            
            for document in requestdata:
                if 'id' in document:
                    documentid=document['id']
                    del document['id']
                    employeedocs=MODELS_USER.Employeedocs.objects.filter(id=documentid)
                    if employeedocs.first().user.id==userid:

                        static_fields = []
                        if 'attachment' in document:
                            if 'InMemoryUploadedFile' in str(type(document['attachment'])): static_fields.append('attachment')
                            else: del document['attachment']

                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                            classOBJ=MODELS_USER.Employeedocs,
                            Serializer=PSRLZER_USER.Employeedocsserializer,
                            id=documentid,
                            data=document,
                            static_fields=static_fields
                        )
                        if responsesuccessflag == 'error':
                            response_message.extend([f'update({documentid}) {message}' for message in responsemessage])
                        elif responsesuccessflag == 'success':
                            response_successflag = 'success'
                            response_status = status.HTTP_200_OK
                    else: response_message.append(f'This User({userid}) has no Employeedocs having {documentid} id!')
                else:
                    if 'user' not in document: document.update({'user': userid})
                    required_fields = ['title', 'user']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_USER.Employeedocs, 
                        Serializer=PSRLZER_USER.Employeedocsserializer, 
                        data=document,
                        required_fields=required_fields
                    )
                    if responsesuccessflag == 'error':
                        response_message.extend([f'add {message}' for message in responsemessage])
                    elif responsesuccessflag == 'success':
                        response_successflag = 'success'
                        response_status = status.HTTP_200_OK
            response_data = CSRLZER_USER.Userserializer(MODELS_USER.User.objects.get(id=userid), many=False).data
        else: response_message.append('no documents provided!')
    else: response_message.append('user doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getnote(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'title', 'convert': None, 'replace':'reason__ititle'},
        {'name': 'description', 'convert': None, 'replace':'reason__idescription'},
        {'name': 'priority', 'convert': None, 'replace':'reason__ipriority'},
        {'name': 'reminder', 'convert': None, 'replace':'reminder'},
        {'name': 'status', 'convert': None, 'replace':'status'}
    ]
    notes = MODELS_USER.Note.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: notes = notes.order_by(column_accessor)

    total_count = notes.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: notes = notes[(page-1)*page_size:page*page_size]

    noteserializers = SRLZER_USER.Noteserializer(notes, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': noteserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addnote(request):
    extra_fields = {'created_by': request.user.id, 'updated_by': request.user.id}
    choice_fields = [
        {'name': 'priority', 'type': 'single-string', 'values': [item[1] for item in CHOICE.PRIORITY]}
    ]
    fields_regex = [
        {'field': 'reminder', 'type': 'date'}
    ]
    required_fields = ['user','title', 'priority']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Note, 
        Serializer=SRLZER_USER.Noteserializer, 
        data=request.data, 
        unique_fields=[], 
        extra_fields=extra_fields, 
        choice_fields=choice_fields, 
        required_fields=required_fields,
        fields_regex=fields_regex
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatenote(request, noteid=None):
    fields_regex = [
        {'field': 'reminder', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Note, 
        Serializer=SRLZER_USER.Noteserializer, 
        id=noteid, 
        data=request.data,
        fields_regex=fields_regex
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletenote(request, noteid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Note,
        id=noteid,
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def assignusergroup(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    userlist = request.data.get('user')
    
    classOBJpackage = {
        'Devicegroup': MODELS_DEVI.Devicegroup,
        'Group': MODELS_DEVI.Group,
        'Userdevicegroup': MODELS_USER.Userdevicegroup,
        'User': MODELS_USER.User
    }
    grouplist = request.data.get('group')
    group_response = ghelp().assignBulkUserToBulkGroup(classOBJpackage, grouplist, userlist)
    
    if group_response['backend_message']:
        response_message.append('inform backend, data is missing in backend!')
    
    if group_response['flag']:
        response_message.extend(group_response['message'])
        response_successflag = 'success'
        response_status = status.HTTP_202_ACCEPTED
    else: response_message.extend(group_response['message'])
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)