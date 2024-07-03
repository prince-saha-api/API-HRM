from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from device import models as MODELS_DEVI
from user import models as MODELS_USER
from device.serializer import serializers as SRLZER_DEVI
from device.serializer.POST import serializers as PSRLZER_DEVI
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getdevices(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'title', 'convert': None, 'replace':'title__icontains'},
                    {'name': 'username', 'convert': None, 'replace':'username'},
                    {'name': 'password', 'convert': None, 'replace':'password'},
                    {'name': 'location', 'convert': None, 'replace':'location'},
                    {'name': 'macaddress', 'convert': None, 'replace':'macaddress'},
                    {'name': 'deviceip', 'convert': None, 'replace':'deviceip'},
                    {'name': 'is_active', 'convert': 'bool', 'replace':'is_active'},
                ]
    
    devices = MODELS_DEVI.Device.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: devices = devices.order_by(column_accessor)
    
    total_count = devices.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: devices = devices[(page-1)*page_size:page*page_size]

    deviceserializers = SRLZER_DEVI.Deviceserializer(devices, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': deviceserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adddevice(request):
    # userid = request.user.id
    unique_fields = ['title']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields = ['title', 'deviceip']
    fields_regex = [
        {'field': 'username', 'type': 'username'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_DEVI.Device, 
        PSRLZER_DEVI.Deviceserializer, 
        request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields,
        fields_regex=fields_regex
        )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatedevice(request, deviceid=None):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_DEVI.Device,
        PSRLZER_DEVI.Deviceserializer,
        deviceid,
        request.data,
        extra_fields=extra_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletedevice(request, deviceid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_DEVI.Devicegroup, 'fields': [{'field': 'device', 'relation': 'manytomanyfield', 'records': MODELS_DEVI.Device.objects.filter(id=deviceid).first().devicegroup_set.all()}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_DEVI.Device,
        deviceid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getgroups(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'title', 'convert': None, 'replace':'title__icontains'},
                    {'name': 'description', 'convert': None, 'replace':'description__icontains'}
                ]
    
    devicegroups = MODELS_DEVI.Devicegroup.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: devicegroups = devicegroups.order_by(column_accessor)
    
    total_count = devicegroups.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: devicegroups = devicegroups[(page-1)*page_size:page*page_size]

    devicegroupserializers = SRLZER_DEVI.Devicegroupserializer(devicegroups, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': devicegroupserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addgroup(request):
    allowed_fields = ['title', 'description']
    unique_fields = ['title']
    required_fields = ['title']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_DEVI.Devicegroup, 
        PSRLZER_DEVI.Devicegroupserializer, 
        request.data,
        allowed_fields=allowed_fields,
        unique_fields=unique_fields, 
        required_fields=required_fields
        )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updategroup(request, groupid=None):
    allowed_fields = ['title', 'description']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_DEVI.Devicegroup,
        PSRLZER_DEVI.Devicegroupserializer,
        groupid,
        request.data,
        allowed_fields=allowed_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletegroup(request, groupid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.Groupofdevicegroup, 'fields': [{'field': 'devicegroup', 'relation': 'manytomanyfield', 'records': MODELS_DEVI.Devicegroup.objects.filter(id=groupid).first().groupofdevicegroup_set.all()}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_DEVI.Devicegroup,
        groupid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getdevicegroup(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'title', 'convert': None, 'replace':'title__icontains'},
                    {'name': 'description', 'convert': None, 'replace':'description__icontains'}
                ]
    
    devicegroups = MODELS_DEVI.Devicegroup.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: devicegroups = devicegroups.order_by(column_accessor)


    preparedevicegroups = []
    for devicegroup in devicegroups:
        if devicegroup:
            preparedevicegroup = {
                "group_title": devicegroup.title if devicegroup.title else None,
                "group_description": devicegroup.description if devicegroup.description else None,
                "device_title": None,
                "device_deviceip": None
            }
            for device in devicegroup.device.all():
                preparedevicegroup['device_title'] = device.title if device.title else None
                preparedevicegroup['device_deviceip'] = device.deviceip if device.deviceip else None
                preparedevicegroups.append(preparedevicegroup)

    after_filter = []
    device_title = request.GET.get('device_title')
    if device_title:
        for preparedevicegroup in preparedevicegroups:
            if preparedevicegroup['device_title']:
                split_text = device_title.lower()
                text = preparedevicegroup['device_title'].lower()
                if len(text.split(split_text))>1:
                    after_filter.append(preparedevicegroup)
        preparedevicegroups = after_filter

    after_filter = []
    device_deviceip = request.GET.get('device_deviceip')
    if device_deviceip:
        for preparedevicegroup in preparedevicegroups:
            if preparedevicegroup['device_deviceip']:
                split_text = device_deviceip
                text = preparedevicegroup['device_deviceip']
                if len(text.split(split_text))>1:
                    after_filter.append(preparedevicegroup)
        preparedevicegroups = after_filter

    
    total_count = len(preparedevicegroups)
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: preparedevicegroups = preparedevicegroups[(page-1)*page_size:page*page_size]

    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': preparedevicegroups
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adddevicegroup(request):
    response_data = {}
    response_message = []
    response_successflag = 'success'
    response_status = status.HTTP_201_CREATED

    deviceid = request.data.get('deviceid')
    if deviceid:
        if not isinstance(deviceid, int):
            response_successflag = 'error'
            response_status = status.HTTP_400_BAD_REQUEST
            response_message.append('deviceid should be int!')
    else:
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        response_message.append('deviceid is required!')

    groupid = request.data.get('groupid')
    if groupid:
        if not isinstance(groupid, int):
            response_successflag = 'error'
            response_status = status.HTTP_400_BAD_REQUEST
            response_message.append('groupid should be int!')
    else:
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        response_message.append('groupid is required!')

    if not response_message:
        devicegroup = MODELS_DEVI.Devicegroup.objects.filter(id=groupid)
        if devicegroup.exists():
            devicegroup = devicegroup.first()
            device = MODELS_DEVI.Device.objects.filter(id=deviceid)
            if device.exists():
                device = device.first()
                devicegroup.device.add(device)
            else:
                response_successflag = 'error'
                response_status = status.HTTP_400_BAD_REQUEST
                response_message.append('deviceid doesn\'t exist!')
        else:
            response_successflag = 'error'
            response_status = status.HTTP_400_BAD_REQUEST
            response_message.append('groupid doesn\'t exist!')

    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def updatedevicegroup(request, devicegroupid=None):
#     allowed_fields = ['title', 'description']
#     response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
#         MODELS_DEVI.Devicegroup,
#         PSRLZER_DEVI.Devicegroupserializer,
#         groupid,
#         request.data,
#         allowed_fields=allowed_fields
#         )
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)