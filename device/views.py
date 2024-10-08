from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from device import models as MODELS_DEVI
from user import models as MODELS_USER
from device.serializer import serializers as SRLZER_DEVI
from device.serializer.POST import serializers as PSRLZER_DEVI
from helps.common.generic import Generichelps as ghelp
from helps.device.a_device import A_device as DEVICE
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
import os

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
        {'name': 'is_active', 'convert': 'bool', 'replace':'is_active'}
    ]
    kwargs = ghelp().KWARGS(request, filter_fields)
    devices = MODELS_DEVI.Device.objects.filter(**kwargs)
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
# @deco.get_permission(['get company info', 'all'])
def adddevice(request):
    allowed_fields = ['title', 'username', 'password', 'location', 'macaddress', 'deviceip', 'is_active']
    required_fields = ['title', 'deviceip']
    unique_fields = ['title']
    fields_regex = [{'field': 'username', 'type': 'username'}]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_DEVI.Device, 
        Serializer=PSRLZER_DEVI.Deviceserializer, 
        data=request.data,
        allowed_fields=allowed_fields,
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
    allowed_fields = ['title', 'username', 'password', 'location', 'macaddress', 'deviceip', 'is_active']
    unique_fields = ['title']
    fields_regex = [{'field': 'username', 'type': 'username'}]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_DEVI.Device,
        Serializer=PSRLZER_DEVI.Deviceserializer,
        id=deviceid,
        data=request.data,
        allowed_fields=allowed_fields,
        unique_fields=unique_fields,
        fields_regex=fields_regex
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletedevice(request, deviceid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_DEVI.Devicegroup, 'fields': [{'field': 'device', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_DEVI.Device,
        id=deviceid,
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
    
    groups = MODELS_DEVI.Group.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: groups = groups.order_by(column_accessor)
    
    total_count = groups.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: groups = groups[(page-1)*page_size:page*page_size]

    groupserializers = SRLZER_DEVI.Groupserializer(groups, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': groupserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addgroup(request):
    allowed_fields = ['title', 'description']
    unique_fields = ['title']
    required_fields = ['title']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_DEVI.Group, 
        Serializer=PSRLZER_DEVI.Groupserializer, 
        data=request.data,
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
    unique_fields = ['title']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_DEVI.Group,
        Serializer=PSRLZER_DEVI.Groupserializer,
        id=groupid,
        data=request.data,
        allowed_fields=allowed_fields,
        unique_fields=unique_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletegroup(request, groupid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_DEVI.Devicegroup, 'fields': [{'field': 'group', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_DEVI.Group,
        id=groupid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def getdevicegroup(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'},
        {'name': 'group', 'convert': None, 'replace':'group'},
        {'name': 'device', 'convert': None, 'replace':'device'}
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
# @deco.get_permission(['get company info', 'all'])
def adddevicegroup(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    groupid = request.data.get('group')
    deviceid = request.data.get('device')
    group = MODELS_DEVI.Group.objects.filter(id=groupid)
    if not group.exists(): response_message.append(f'group{groupid} doesn\'t exist!')

    device = MODELS_DEVI.Device.objects.filter(id=deviceid)
    if device.exists():
        if not device.first().is_active: response_message.append(f'device{deviceid} is not in active mood!')
    else: response_message.append(f'device{deviceid} doesn\'t exist!')

    if not response_message:
        user_info = ghelp().getUsersInfoToRegisterIntoDevice(MODELS_USER.User, MODELS_USER.Userdevicegroup, device.first(), groupid)
        response_message.extend(user_info['message'])
        allowed_fields = ['title', 'group', 'device']
        required_fields = ['group', 'device']
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
            classOBJ=MODELS_DEVI.Devicegroup, 
            Serializer=PSRLZER_DEVI.Devicegroupserializer, 
            data=request.data,
            allowed_fields=allowed_fields,
            required_fields=required_fields
        )
        if responsesuccessflag == 'success':
            if user_info['user_count']:
                response = ghelp().registerUserToDevice(user_info['data'])
                if response['flag']:
                    response_data = responsedata.data
                    response_successflag = responsesuccessflag
                    response_status = responsestatus
                else: responsedata.instance.delete()
                response_message.extend(response['message'])
            else:
                response_data = responsedata.data
                response_successflag = responsesuccessflag
                response_status = responsestatus
        elif responsesuccessflag == 'error': response_message.extend(responsemessage)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def updatedevicegroup(request, devicegroupid=None):
#     allowed_fields = ['title', 'group', 'device']
#     response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
#         classOBJ=MODELS_DEVI.Devicegroup,
#         Serializer=PSRLZER_DEVI.Devicegroupserializer,
#         id=devicegroupid,
#         data=request.data,
#         allowed_fields=allowed_fields
#     )
#     response_data = response_data.data if response_successflag == 'success' else {}
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletedevicegroup(request, devicegroupid=None):
    remove_info_from_device = ghelp().getInfoOfUserToRemoveFromDevice(MODELS_DEVI.Devicegroup, MODELS_USER.Userdevicegroup, devicegroupid)
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_DEVI.Devicegroup,
        id=devicegroupid
    )
    if response_successflag == 'success':
        for info in remove_info_from_device:
            response = DEVICE().deleteusr(info['ip'], info['userid'], info['uname'], info['pword'])
            if response['flag']:
                response_message.append(f'successfully removed {info["full_name"]}({info["userid"]}) user as connection between {info["device_name"]} device({info["ip"]}) to {info["group_name"]} group has been deleted!')
            else: response_message.extend([f'{each}, please delete it manually, it may occur internate problem, ip connection problem etc!' for each in response['message']])
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# # @deco.get_permission(['get company info', 'all'])
# def insertUserWithoutImage(request):

#     ip = '10.10.20.51'
#     name = 'DummyABC'
#     cardno = 147258369258456
#     userid = 'DummyID'
#     password = ''
#     reg_date = '20240827'
#     valid_date = '20300827'
#     uname = 'admin'
#     pword = 'admin1234'
#     response = DEVICE().insertusrwithoutimg(ip, name, cardno, userid, password, reg_date,  valid_date, uname, pword)
    
#     return Response({"response": response}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # @deco.get_permission(['get company info', 'all'])
# def existanceUser(request):

#     ip = '10.10.20.51'
#     userid = 'DummyID'
#     uname = 'admin'
#     pword = 'admin1234'
#     response = DEVICE().existanceofuser(ip, userid, uname, pword)
    
#     return Response({"response": response}, status=status.HTTP_200_OK)


# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # @deco.get_permission(['get company info', 'all'])
# def getRecordNumber(request):

#     ip = '10.10.20.51'
#     userid = 'DummyID'
#     uname = 'admin'
#     pword = 'admin1234'
#     response = DEVICE().get_record_number(ip, userid, uname, pword)
    
#     return Response({"response": response}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # @deco.get_permission(['get company info', 'all'])
# def isDeviceActive(request):

#     ip = '10.10.20.51'
#     response = DEVICE().is_device_active(ip)
    
#     return Response({"response": response}, status=status.HTTP_200_OK)