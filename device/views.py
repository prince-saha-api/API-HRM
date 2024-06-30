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
    deviceserializers = SRLZER_DEVI.Deviceserializer(devices, many=True)
    return Response({'status': 'success', 'message': '', 'data': deviceserializers.data}, status=status.HTTP_200_OK)

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
def getdevicegroups(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'title', 'convert': None, 'replace':'title__icontains'},
                    {'name': 'device', 'convert': None, 'replace':'device'},
                    {'name': 'is_active', 'convert': 'bool', 'replace':'is_active'},
                ]
    devicegroups = MODELS_DEVI.Devicegroup.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: devicegroups = devicegroups.order_by(column_accessor)
    devicegroupserializers = SRLZER_DEVI.Devicegroupserializer(devicegroups, many=True)
    return Response({'status': 'success', 'message': '', 'data': devicegroupserializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adddevicegroup(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['title']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields = ['title']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_DEVI.Devicegroup, PSRLZER_DEVI.Devicegroupserializer, request.data, unique_fields=unique_fields, extra_fields=extra_fields, required_fields=required_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatedevicegroup(request, devicegroupid=None):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_DEVI.Devicegroup,
        PSRLZER_DEVI.Devicegroupserializer,
        devicegroupid,
        request.data,
        extra_fields=extra_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletedevicegroup(request, devicegroupid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_USER.Groupofdevicegroup, 'fields': [{'field': 'devicegroup', 'relation': 'manytomanyfield', 'records': MODELS_DEVI.Devicegroup.objects.filter(id=devicegroupid).first().groupofdevicegroup_set.all()}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_DEVI.Devicegroup,
        devicegroupid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)