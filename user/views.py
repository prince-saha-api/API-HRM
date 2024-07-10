from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from contribution import models as MODELS_CONT
from leave import models as MODELS_LEAV
from department import models as MODELS_DEPA
from hrm_settings import models as MODELS_SETT
from user import models as MODELS_USER
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
import os

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
def addresponsibility(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['title']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields = ['title']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Responsibility, 
        PSRLZER_USER.Responsibilityserializer, 
        request.data, 
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
def addrequiredskill(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['title']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields= ['title']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Requiredskill, 
        PSRLZER_USER.Requiredskillserializer, 
        request.data, 
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
def adddsignation(request):
    # userid = request.user.id
    unique_fields = ['name']
    required_fields= ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Designation, 
        PSRLZER_USER.Designationserializer, 
        request.data, 
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
        MODELS_USER.Designation,
        PSRLZER_USER.Designationserializer,
        designationid,
        request.data,
        unique_fields=unique_fields,
        allowed_fields=allowed_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletedesignation(request, designationid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.User, 'fields': [{'field': 'designation', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_USER.Designation,
        designationid,
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
def addgrade(request):
    # userid = request.user.id
    unique_fields = ['name']
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Grade, 
        PSRLZER_USER.Gradeserializer, 
        request.data, 
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
        MODELS_USER.Grade,
        PSRLZER_USER.Gradeserializer,
        gradeid,
        request.data,
        unique_fields=unique_fields
        )
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
        MODELS_USER.Grade,
        gradeid,
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
        MODELS_USER.Shift, 
        PSRLZER_USER.Shiftserializer, 
        request.data, 
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
        MODELS_USER.Shift, 
        PSRLZER_USER.Shiftserializer, 
        shiftid, 
        request.data,
        unique_fields=unique_fields,
        extra_fields=extra_fields, 
        fields_regex=fields_regex
        )
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
        MODELS_USER.Shift,
        shiftid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
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
def addshiftchangerequest(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'user': userid, 'updated_by': userid})
    extra_fields.update({'status': CHOICE.STATUS[0][1]})
    allowed_fields = ['reqshiftid', 'fromdate', 'todate',  'reqnote']
    choice_fields = [
        {'name': 'status', 'values': [item[1] for item in CHOICE.STATUS]}
    ]
    required_fields = ['user', 'reqshiftid', 'fromdate', 'todate']
    fields_regex = [
        {'field': 'fromdate', 'type': 'date'},
        {'field': 'todate', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Shiftchangerequest, 
        PSRLZER_USER.Shiftchangerequestserializer, 
        request.data, 
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
        MODELS_USER.Shiftchangerequest, 
        PSRLZER_USER.Shiftchangerequestserializer, 
        shiftchangerequestid, 
        request.data, 
        allowed_fields=allowed_fields, 
        freez_update=freez_update, 
        extra_fields=extra_fields, 
        fields_regex=fields_regex
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
        MODELS_USER.Shiftchangerequest, 
        PSRLZER_USER.Shiftchangerequestserializer, 
        shiftchangerequestid, 
        request.data, 
        allowed_fields=allowed_fields, 
        continue_update=continue_update, 
        extra_fields=extra_fields, 
        fields_regex=fields_regex
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
        MODELS_USER.Shiftchangerequest, 
        PSRLZER_USER.Shiftchangerequestserializer, 
        shiftchangerequestid, 
        request.data, 
        allowed_fields=allowed_fields, 
        continue_update=continue_update, 
        extra_fields=extra_fields, 
        fields_regex=fields_regex
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteshiftchangerequest(request, shiftchangerequestid=None):
    # freez_delete = [{'status': [CHOICE.STATUS[1][1], CHOICE.STATUS[2][1]]}]
    continue_delete = [{'status': [CHOICE.STATUS[0][1]]}]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_USER.Shiftchangerequest,
        shiftchangerequestid,
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
def addreligion(request):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    unique_fields = ['name']
    required_fields = ['name']
    
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Religion, 
        PSRLZER_USER.Religionserializer, 
        request.data, 
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
        MODELS_USER.Religion,
        PSRLZER_USER.Religionserializer,
        religionid,
        request.data,
        unique_fields=unique_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletereligion(request, religionid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.User, 'fields': [{'field': 'religion', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_USER.Religion,
        religionid,
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
# @permission_classes([IsAuthenticated])
def addpermission(request):
    unique_fields = ['name']
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Permission, 
        PSRLZER_USER.Permissionserializer, 
        request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields
        )
    if response_data: response_data = response_data.data
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
def addrolepermission(request):
    unique_fields = ['name']
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Rolepermission, 
        PSRLZER_USER.Rolepermissionserializer, 
        request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields
        )
    if response_data: response_data = response_data.data
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
def addethnicgroup(request):
    unique_fields = ['name']
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_USER.Ethnicgroup, 
        PSRLZER_USER.Ethnicgroupserializer, 
        request.data, 
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
                        {'name': 'gross_salary', 'convert': None, 'replace':'gross_salary'},
                        {'name': 'payment_in', 'convert': None, 'replace':'payment_in__icontains'},
                        {'name': 'supervisor', 'convert': None, 'replace':'supervisor'},
                        {'name': 'expense_approver', 'convert': None, 'replace':'expense_approver'},
                        {'name': 'leave_approver', 'convert': None, 'replace':'leave_approver'},
                        {'name': 'shift_request_approver', 'convert': None, 'replace':'shift_request_approver'},
                        {'name': 'grade', 'convert': None, 'replace':'grade'},
                        {'name': 'shift', 'convert': None, 'replace':'shift'},
                        {'name': 'joining_date', 'convert': None, 'replace':'joining_date'},
                        {'name': 'allow_overtime', 'convert': 'bool', 'replace':'allow_overtime'},
                        {'name': 'allow_remote_checkin', 'convert': 'bool', 'replace':'allow_remote_checkin'},
                        {'name': 'job_status', 'convert': None, 'replace':'job_status__icontains'},
                        {'name': 'official_note', 'convert': None, 'replace':'official_note__icontains'},
                        {'name': 'rfid', 'convert': None, 'replace':'rfid__icontains'},
                        {'name': 'created_by', 'convert': None, 'replace':'created_by'},
                        {'name': 'updated_by', 'convert': None, 'replace':'updated_by'},
                    ]
    users = MODELS_USER.User.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: users = users.order_by(column_accessor)
    
    total_count = users.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: users = users[(page-1)*page_size:page*page_size]

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
    generalsettings = MODELS_SETT.Generalsettings.objects.all().order_by('id')
    if generalsettings.exists():
        created_by = MODELS_USER.User.objects.get(id=request.user.id) if request.user.id != None else None
        requestdata = dict(request.data)
        # requestdata = ghelp().requestdata()
        options = {
            'allow_blank': True,
            'allow_empty': False
        }
        
        form = NestedForm(requestdata, **options)
        form.is_nested(raise_exception=True)


        personalDetails = form.data.get('personalDetails')
        personalDetails = ghelp().prepareData(personalDetails, 'personal')

        officialDetails = form.data.get('officialDetails')
        officialDetails = ghelp().prepareData(officialDetails, 'office')
        if 'official_id' not in officialDetails: return Response({'data': {}, 'message': ['official_id is required!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        if 'ethnic_group' not in officialDetails: return Response({'data': {}, 'message': ['ethnic_group is required!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        salaryAndLeaves = form.data.get('salaryAndLeaves')
        ghelp().preparesalaryAndLeaves(salaryAndLeaves)

        emergencyContact = form.data.get('emergencyContact')
        emergencyContact = ghelp().prepareData(emergencyContact, 'emergencycontact')
        academicRecord = form.data.get('academicRecord')
        academicRecord = ghelp().prepareData(academicRecord, 'academicrecord')
        previousExperience = form.data.get('previousExperience')
        previousExperience = ghelp().prepareData(previousExperience, 'previousexperience')

        # uploadDocuments = form.data.get('uploadDocuments')

        # লিভ-পলিসি যুক্ত করলে এথনিক-গ্রুপও দিতে হবে
        leavepolicy_salaryAndLeaves = salaryAndLeaves.get('leavepolicy')
        if leavepolicy_salaryAndLeaves:
            if not ghelp().ifallrecordsexistornot(MODELS_USER.Ethnicgroup, officialDetails.get('ethnic_group')):
                return Response({'data': {}, 'message': ['please add valid Ethnicgroup!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        if ghelp().ifallrecordsexistornot(MODELS_LEAV.Leavepolicy, salaryAndLeaves.get('leavepolicy')):

            fiscal_year = generalsettings.first().fiscalyear
            official_id = officialDetails.get('official_id')
            if official_id:
                classOBJpackage = {
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
                required_fields = ['username', 'password', 'first_name', 'last_name', 'gender', 'personal_phone', 'official_id']
                usermodelsuniquefields = ['personal_phone', 'nid_passport_no', 'tin_no', 'official_id', 'official_phone', 'rfid']
                response = ghelp().createuser(classOBJpackage, serializerOBJpackage, createdInstance, personalDetails, officialDetails, salaryAndLeaves, photo, usermodelsuniquefields, required_fields, created_by)

                if not response['flag']:
                    for each in createdInstance:
                        if each: each.delete()
                    return Response({'data': {}, 'message': response['message'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                userinstance = response['userinstance'] 

                role_permission_officialDetails = officialDetails.get('role_permission')
                if role_permission_officialDetails:
                    for id in role_permission_officialDetails:
                        object = ghelp().getobject(MODELS_USER.Rolepermission, {'id': id})
                        if object: userinstance.role_permission.add(object)


                # ইউজার ক্রিয়েটের পরে।
                ethnic_group_officialDetails = officialDetails.get('ethnic_group')
                if ethnic_group_officialDetails:
                    for id in ethnic_group_officialDetails:
                        object = ghelp().getobject(MODELS_USER.Ethnicgroup, {'id': id})
                        if object:
                            if object.name != 'all': object.user.add(userinstance)

                leavepolicy_salaryAndLeaves = salaryAndLeaves.get('leavepolicy')
                if isinstance(leavepolicy_salaryAndLeaves, list):
                    if leavepolicy_salaryAndLeaves:
                        for id in leavepolicy_salaryAndLeaves:
                            leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': id})
                            if leavepolicy:
                                # if userinstance in leavepolicy.applicable_for.user.all() or leavepolicy.applicable_for.name == 'all':
                                if not MODELS_LEAV.Leavepolicyassign.objects.filter(user=userinstance, leavepolicy=leavepolicy).exists():
                                    MODELS_LEAV.Leavepolicyassign.objects.create(user=userinstance, leavepolicy=leavepolicy)
                                    if not MODELS_LEAV.Leavesummary.objects.filter(user=userinstance, leavepolicy=leavepolicy).exists():
                                        MODELS_LEAV.Leavesummary.objects.create(
                                            user=userinstance,
                                            leavepolicy=leavepolicy,
                                            fiscal_year=fiscal_year,
                                            total_allocation=leavepolicy.allocation_days,
                                            total_consumed=0,
                                            total_left=leavepolicy.allocation_days
                                        )
                emergencycontact = ghelp().addemergencycontact(MODELS_USER.Employeecontact, PSRLZER_USER.Employeecontactserializer, MODELS_CONT.Address, PSRLZER_CONT.Addressserializer, userinstance, emergencyContact)
                academicrecord = ghelp().addacademicrecord(MODELS_USER.Employeeacademichistory, PSRLZER_USER.Employeeacademichistoryserializer, userinstance, academicRecord)
                previousexperience = ghelp().addpreviousexperience(MODELS_USER.Employeeexperiencehistory, PSRLZER_USER.Employeeexperiencehistoryserializer, userinstance, previousExperience)

                faileddetails = []
                faileddetails.extend(emergencycontact['failed'])
                faileddetails.extend(academicrecord['failed'])
                faileddetails.extend(previousexperience['failed'])

                # message
                emergencycontact['message']
                academicrecord['message']
                previousexperience['message']

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



                department_officialDetails = ghelp().getobject(MODELS_DEPA.Department, {'id': officialDetails.get('department')})
                if department_officialDetails: department_officialDetails.user.add(userinstance)
                # company_officialDetails = ghelp().getobject(MODELS_COM.Company, {'id': officialDetails.get('company')})
                # branch_officialDetails = ghelp().getobject(MODELS_BR.Branch, {'id': officialDetails.get('branch')})
                # department_officialDetails = ghelp().getobject('''MODELS_BR.Branch''', {'id': officialDetails.get('department')})
                    
                return Response({'data': SRLZER_USER.Userserializer(userinstance, many=False).data, 'message': [], 'status': 'success'}, status=status.HTTP_201_CREATED)
            else: return Response({'data': {}, 'message': ['employee id is missing!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'data': {}, 'message': ['please add valid Leavepolicy!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': ['please add general settings first!!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateprofilepic(request, userid=None):
    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        photo = request.FILES.get('photo')
        if photo:
            userserializer = PSRLZER_USER.Userserializer(instance=user.first(), data=request.data, partial=True)
            if userserializer.is_valid():
                try:
                    ghelp().removeFile(user.first(), 'photo')
                    userserializer.save()
                    return Response({'data': {}, 'message': ['successfully uploaded the photo!'], 'status': 'success'}, status=status.HTTP_200_OK)
                except: return Response({'data': {}, 'message': ['couldn\'t upload photo!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'data': {}, 'message': ['photo doesn\'t exist!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': ['user doesn\'t exist!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateprofile(request, userid=None):
    requesteddata = request.data.copy()

    department = None
    if 'department' in requesteddata:
        department = requesteddata['department']
        if department:
            if isinstance(department, str):
                if department.isnumeric(): department = int(department)
    if isinstance(department, int):
        user = MODELS_USER.User.objects.filter(id=userid).first()
        for departmentOBJ in user.departmenttwo.all():
            departmentOBJ.user.remove(user)
        department = MODELS_DEPA.Department.objects.filter(id=department)
        if department.exists(): department.first().user.add(user)

        del requesteddata['department']

    if 'official_id' in requesteddata:
        official_id = requesteddata['official_id']
        if official_id:
            requesteddata.update({'username': official_id})

    allowed_fields = ['username', 'first_name', 'last_name', 'designation', 'official_id', 'joining_date', 'personal_phone', 'personal_email', 'dob', 'gender', 'blood_group', 'marital_status', 'spouse_name', 'supervisor']
    unique_fields = ['official_id', 'personal_phone', 'personal_email']
    choice_fields = [
        {'name': 'gender', 'values': [item[1] for item in CHOICE.GENDER]},
        {'name': 'blood_group', 'values': [item[1] for item in CHOICE.BLOOD_GROUP]},
        {'name': 'marital_status', 'values': [item[1] for item in CHOICE.MARITAL_STATUS]}
    ]
    fields_regex = [
        {'field': 'official_id', 'type': 'employeeid'},
        {'field': 'personal_phone', 'type': 'phonenumber'},
        {'field': 'personal_email', 'type': 'email'},
        {'field': 'dob', 'type': 'date'}
    ]

    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_USER.User,
        PSRLZER_USER.Userserializer,
        userid,
        requesteddata,
        allowed_fields=allowed_fields,
        unique_fields=unique_fields,
        choice_fields=choice_fields,
        fields_regex=fields_regex
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatepersonaldetails(request, userid=None):

    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        requesteddata = request.data.copy()

        if 'present_address' in requesteddata:
            presentaddressid = user.first().present_address.id
            presentaddress = requesteddata['present_address']
            response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                MODELS_CONT.Address,
                PSRLZER_CONT.Addressserializer,
                presentaddressid,
                presentaddress
            )
            del requesteddata['present_address']

        if 'permanent_address' in requesteddata:
            permanentaddressid = user.first().permanent_address
            permanentaddress = requesteddata['permanent_address']
            response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                MODELS_CONT.Address,
                PSRLZER_CONT.Addressserializer,
                permanentaddressid,
                permanentaddress
            )
            del requesteddata['permanent_address']

        allowed_fields = ['fathers_name', 'mothers_name', 'spouse_name', 'nationality', 'religion', 'nid_passport_no', 'tin_no']
        unique_fields = ['nid_passport_no', 'tin_no']
        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
            MODELS_USER.User,
            PSRLZER_USER.Userserializer,
            userid,
            requesteddata,
            allowed_fields=allowed_fields,
            unique_fields=unique_fields
        )
        if response_successflag == 'success':
            return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
        elif response_successflag == 'error':
            return Response({'data': {}, 'message': ['something went wrong!'], 'status':'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': ['user doesn\'t exist!'], 'status':'error'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def updateofficialdetails(request, userid=None):

#     user = MODELS_USER.User.objects.filter(id=userid)
#     if user.exists():
#         requesteddata = request.data.copy()
        
#         if 'company' in requesteddata:
#             company = requesteddata['company']

#         # company
#         # branch

#         # official_phone
#         # employee_type
#         # shift
#         # grade
#         # role_permission
#         # joining_date
#         # expense_approver
#         # leave_approver
#         # shift_request_approver
#     else: return Response({'data': {}, 'message': ['user doesn\'t exist!'], 'status':'error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatesalaryleaves(request, userid=None):

    user = MODELS_USER.User.objects.filter(id=userid)
    if user.exists():
        requesteddata = request.data.copy()

        if 'bankaccount' in requesteddata:
            bankaccount = requesteddata['bankaccount']
            bankaccountid = user.first().bank_account.id

            response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                MODELS_CONT.Bankaccount,
                PSRLZER_CONT.Bankaccountserializer,
                bankaccountid,
                bankaccount
            )

            if 'address' in bankaccount:
                address = bankaccount['address']
                addressid = user.first().bank_account.address.id
                response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                    MODELS_CONT.Address,
                    PSRLZER_CONT.Addressserializer,
                    addressid,
                    address
                )
            del requesteddata['bankaccount']

        # leavepolicy
        couldnotremoveleavepolicy = []
        if 'leavepolicy' in requesteddata:
            leavepolicy = requesteddata['leavepolicy']
            if isinstance(leavepolicy, list):
                if leavepolicy:
                    fiscalyear = MODELS_SETT.Generalsettings.objects.all().order_by('id').last().fiscalyear
                    keepleavepolicy = []
                    for id in leavepolicy:
                        leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': id})
                        if leavepolicy:
                            leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user.first(), leavepolicy=leavepolicy)
                            if not leavesummary.exists():
                                leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user.first(), leavepolicy=leavepolicy)
                                if leavepolicyassign.exists():
                                    MODELS_LEAV.Leavesummary.objects.create(
                                        user=user.first(),
                                        leavepolicy=leavepolicy,
                                        fiscal_year=fiscalyear,
                                        total_allocation=leavepolicy.allocation_days,
                                        total_consumed=0,
                                        total_left=leavepolicy.allocation_days
                                    )
                                else:
                                    MODELS_LEAV.Leavepolicyassign.objects.create(
                                        user=user.first(),
                                        leavepolicy=leavepolicy
                                    )
                                    MODELS_LEAV.Leavesummary.objects.create(
                                        user=user.first(),
                                        leavepolicy=leavepolicy,
                                        fiscal_year=fiscalyear,
                                        total_allocation=leavepolicy.allocation_days,
                                        total_consumed=0,
                                        total_left=leavepolicy.allocation_days
                                    )
                                keepleavepolicy.append(leavepolicy)
                    leavepolicyassigns = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user.first())
                    for leavepolicyassign in leavepolicyassigns:
                        if leavepolicyassign.leavepolicy not in keepleavepolicy:
                            leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user.first(), leavepolicy=leavepolicyassign.leavepolicy)
                            if leavesummary.exists():
                                if leavesummary.first().total_consumed:
                                    couldnotremoveleavepolicy.append(leavepolicyassign.leavepolicy)
                                else:
                                    leavesummary.delete()
                                    leavepolicyassign.delete()
                            else: leavepolicyassign.delete()
            del requesteddata['leavepolicy']
        # earningpolicy
        # deductionpolicy
        
        allowed_fields = ['payment_in', 'gross_salary']
        choice_fields = [
            {'name': 'payment_in', 'values': [item[1] for item in CHOICE.PAYMENT_IN]}
        ]
        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
            MODELS_USER.User,
            PSRLZER_USER.Userserializer,
            userid,
            requesteddata,
            allowed_fields=allowed_fields,
            choice_fields=choice_fields
        )
        if response_successflag == 'success':
            return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
        elif response_successflag == 'error':
            return Response({'data': {}, 'message': ['something went wrong!'], 'status':'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': ['user doesn\'t exist!'], 'status':'error'}, status=status.HTTP_400_BAD_REQUEST)