from django.shortcuts import render
from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from helps.choice import common as CHOICE
from rest_framework.permissions import IsAuthenticated
from helps.common.generic import Generichelps as ghelp
from helps.device.a_device import A_device as DEVICE
from attendance import models as MODELS_ATTE
from attendance.serializer.POST import serializers as PSRLZER_ATTE
from attendance.serializer import serializers as SRLZER_ATTE
from device import models as MODELS_DEVI
from rest_framework.response import Response
from rest_framework import status
from user import models as MODELS_USER

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def getmanualattendence(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'date', 'convert': None, 'replace':'date'},
        {'name': 'in_time', 'convert': None, 'replace':'in_time'},
        {'name': 'out_time', 'convert': None, 'replace':'out_time'},
        {'name': 'status', 'convert': None, 'replace':'status__icontains'},
        {'name': 'requested_by', 'convert': None, 'replace':'requested_by'},
        {'name': 'decisioned_by', 'convert': None, 'replace':'decisioned_by'}
    ]
    kwargs=ghelp().KWARGS(request, filter_fields)
    if 'requested_by' not in kwargs: kwargs.update({'requested_by': request.user.id})

    requestmanualattendances = MODELS_ATTE.Requestmanualattendance.objects.filter(**kwargs)
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: requestmanualattendances = requestmanualattendances.order_by(column_accessor)

    total_count = requestmanualattendances.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: requestmanualattendances = requestmanualattendances[(page-1)*page_size:page*page_size]

    requestmanualattendanceserializers = SRLZER_ATTE.Requestmanualattendanceserializer(requestmanualattendances, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': requestmanualattendanceserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addmanualattendence(request):
    requestdata = request.data.copy()
    date = requestdata.get('date')
    if date == None: return Response({'status': 'error', 'message': 'date is required!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
    if 'requested_by' not in requestdata:  requestdata.update({'requested_by': request.user.id})

    allowed_fields = ['date', 'in_time', 'out_time', 'admin_note', 'requested_by']
    required_fields = ['date', 'in_time', 'out_time']
    fields_regex = [{'field': 'date', 'type': 'date'}, {'field': 'in_time', 'type': 'time'}, {'field': 'out_time', 'type': 'time'}]
    
    extra_fields = {'status': CHOICE.STATUS[0][1]}
    if 'requested_by' not in requestdata: extra_fields.update({'requested_by': request.user.id})
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_ATTE.Requestmanualattendance,
        Serializer=PSRLZER_ATTE.Requestmanualattendanceserializer,
        data=requestdata,
        allowed_fields=allowed_fields,
        required_fields=required_fields,
        fields_regex=fields_regex,
        extra_fields=extra_fields
    )
    if response_successflag == 'success': response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def updatemanualattendence(request, manualattendenceid=None):
    # allowed_fields = ['date', 'in_time', 'out_time']
    fields_regex = [{'field': 'date', 'type': 'date'}, {'field': 'in_time', 'type': 'time'}, {'field': 'out_time', 'type': 'time'}]
    freez_update = [{'status': [CHOICE.STATUS[1][1], CHOICE.STATUS[2][1]]}]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_ATTE.Requestmanualattendance,
        Serializer=SRLZER_ATTE.Requestmanualattendanceserializer,
        id=manualattendenceid,
        data=request.data,
        # allowed_fields=allowed_fields,
        fields_regex=fields_regex,
        freez_update=freez_update
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def approvemanualattendence(request, manualattendenceid=None):
    freez_update = [{'status': [CHOICE.STATUS[1][1], CHOICE.STATUS[2][1]]}]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_ATTE.Requestmanualattendance,
        Serializer=SRLZER_ATTE.Requestmanualattendanceserializer,
        id=manualattendenceid,
        data={'status': CHOICE.STATUS[1][1]},
        freez_update=freez_update
    )
    if response_successflag == 'success':
        response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)





    requestmanualattendance = MODELS_ATTE.Requestmanualattendance.objects.filter(id=manualattendenceid)
    if requestmanualattendance.exists():
        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestmanualattendance.first().date, employee=requestmanualattendance.first().requested_by.id)
        if requestmanualattendance.first().status != CHOICE.STATUS[2][1]:
            if requestmanualattendance.first().status != CHOICE.STATUS[1][1]:
                if not attendance.exists():
                    data = {'status': CHOICE.STATUS[1][1], 'decisioned_by': request.user.id}
                    requestmanualattendanceserializer = PSRLZER_ATTE.Requestmanualattendanceserializer(instance=requestmanualattendance.first(), data=data, partial=True)
                    if requestmanualattendanceserializer.is_valid(raise_exception=True):
                        requestmanualattendanceserializer.save()
                        MODELS_ATTE.Attendance(
                            date=requestmanualattendance.first().date,
                            in_time=requestmanualattendance.first().in_time,
                            out_time=requestmanualattendance.first().out_time,
                            employee=MODELS_USER.User.objects.get(id=requestmanualattendance.first().requested_by.id),
                            attendance_from=CHOICE.ATTENDANCE_FROM[1][1]
                        ).save()
                        return Response({'status': 'success', 'message': '', 'data': requestmanualattendanceserializer.data}, status=status.HTTP_200_OK)
                    else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': requestmanualattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = {'status': CHOICE.STATUS[1][1], 'decisioned_by': request.user.id}
                    requestmanualattendanceserializer = PSRLZER_ATTE.Requestmanualattendanceserializer(instance=requestmanualattendance.first(), data=data, partial=True)
                    if requestmanualattendanceserializer.is_valid(raise_exception=True):
                        requestmanualattendanceserializer.save()
                    return Response({'status': 'error', 'message': 'already attendance exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not attendance.exists():
                    MODELS_ATTE.Attendance(
                        date=requestmanualattendance.first().date,
                        in_time=requestmanualattendance.first().in_time,
                        out_time=requestmanualattendance.first().out_time,
                        employee=MODELS_USER.User.objects.get(id=requestmanualattendance.first().requested_by.id),
                        attendance_from=CHOICE.ATTENDANCE_FROM[1][1]
                    ).save()
                return Response({'status': 'error', 'message': 'already approved!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if attendance.exists(): attendance.delete()
            return Response({'status': 'error', 'message': 'it\'s rejected!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def rejectmanualattendence(request, manualattendenceid=None):
    requestmanualattendance = MODELS_ATTE.Requestmanualattendance.objects.filter(id=manualattendenceid)
    if requestmanualattendance.exists():

        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestmanualattendance.first().date, employee=requestmanualattendance.first().requested_by.id)
        if attendance.exists():
            attendance.delete()

        data = {'status': CHOICE.STATUS[2][1], 'decisioned_by': request.user.id}
        if request.data.get('reject_reason'): data.update({'reject_reason': request.data.get('reject_reason')})
        requestmanualattendanceserializer = PSRLZER_ATTE.Requestmanualattendanceserializer(instance=requestmanualattendance.first(), data=data, partial=True)
        if requestmanualattendanceserializer.is_valid(raise_exception=True):
            requestmanualattendanceserializer.save()
            return Response({'status': 'success', 'message': '', 'data': requestmanualattendanceserializer.data}, status=status.HTTP_200_OK)
        else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': requestmanualattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def getremotelog(request):
    filter_fields = [
                        {'name': 'employee', 'convert': None, 'replace':'employee'},
                        {'name': 'date', 'convert': None, 'replace':'date'},
                        {'name': 'time', 'convert': None, 'replace':'time'},
                        {'name': 'latitude', 'convert': None, 'replace':'latitude'},
                        {'name': 'longitude', 'convert': None, 'replace':'longitude'},
                        {'name': 'device', 'convert': None, 'replace':'device__icontains'},
                        {'name': 'model', 'convert': None, 'replace':'model__icontains'}
                    ]
    remotelogs = MODELS_ATTE.Remotelogs.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: remotelogs = remotelogs.order_by(column_accessor)

    total_count = remotelogs.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: remotelogs = remotelogs[(page-1)*page_size:page*page_size]

    remotelogsserializers = SRLZER_ATTE.Remotelogsserializer(remotelogs, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': remotelogsserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addremotelog(request):
    date = request.data.get('date')
    if date == None: return Response({'status': 'error', 'message': 'date is required!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
    time = request.data.get('time')
    if time == None: return Response({'status': 'error', 'message': 'time is required!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
    
    request.data.update({'employee': request.user.id})
    remotelogs = MODELS_ATTE.Remotelogs.objects.filter(date=date, employee=request.user.id, time=time)
    
    if not remotelogs.exists():
        remotelogsserializer = PSRLZER_ATTE.Remotelogsserializer(data=request.data, many=False)
        if remotelogsserializer.is_valid():
            remotelogsserializer.save()
            return Response({'status': 'success', 'message': '', 'data': remotelogsserializer.data}, status=status.HTTP_201_CREATED)
        else: return Response({'status': 'error', 'message': '', 'data': remotelogsserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'already exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def updateremotelog(request, remotelogid=None):
    remotelogs = MODELS_ATTE.Remotelogs.objects.filter(id=remotelogid)
    if remotelogs.exists():
        data = {}
        date = request.data.get('date')
        if date != None: data.update({'date': date})

        time = request.data.get('time')
        if time != None: data.update({'time': time})

        latitude = request.data.get('latitude')
        if latitude != None: data.update({'latitude': latitude})

        longitude = request.data.get('longitude')
        if longitude != None: data.update({'longitude': longitude})

        device = request.data.get('device')
        if device != None: data.update({'device': device})

        model = request.data.get('model')
        if model != None: data.update({'model': model})

        remotelogsserializer = PSRLZER_ATTE.Remotelogsserializer(instance=remotelogs.first(), data=data, partial=True)
        if remotelogsserializer.is_valid(raise_exception=True):
            try:
                remotelogsserializer.save()
                return Response({'status': 'success', 'message': '', 'data': remotelogsserializer.data}, status=status.HTTP_200_OK)
            except: return Response({'status': 'error', 'message': 'can\'t update, already exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': remotelogsserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def deleteremotelog(request, remotelogid=None):
    remotelogs = MODELS_ATTE.Remotelogs.objects.filter(id=remotelogid)
    if remotelogs.exists():
        remotelogs.delete()
        return Response({'status': 'success', 'message': 'deleted!', 'data': {}}, status=status.HTTP_200_OK)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def getremoteattendance(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'date', 'convert': None, 'replace':'date'},
                        {'name': 'in_time', 'convert': None, 'replace':'in_time'},
                        {'name': 'out_time', 'convert': None, 'replace':'out_time'},
                        {'name': 'status', 'convert': None, 'replace':'status__icontains'},
                        {'name': 'requested_by', 'convert': None, 'replace':'requested_by'},
                        {'name': 'decisioned_by', 'convert': None, 'replace':'decisioned_by'}
                    ]
    requestremoteattendances = MODELS_ATTE.Requestremoteattendance.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: requestremoteattendances = requestremoteattendances.order_by(column_accessor)

    total_count = requestremoteattendances.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: requestremoteattendances = requestremoteattendances[(page-1)*page_size:page*page_size]

    requestremoteattendanceserializers = SRLZER_ATTE.Requestremoteattendanceserializer(requestremoteattendances, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': requestremoteattendanceserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addremoteattendance(request):
    date = request.data.get('date')
    if date == None: return Response({'status': 'error', 'message': 'date is required!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

    requestremoteattendance = MODELS_ATTE.Requestremoteattendance.objects.filter(date=date, requested_by=request.user.id)
    if not requestremoteattendance.exists():
        remotelogs = MODELS_ATTE.Remotelogs.objects.filter(date=date, employee=request.user.id).order_by('time')
        if remotelogs.count()>0:
            inlog = remotelogs.first()
            outlog = remotelogs.last()

            requestremoteattendanceinstance = MODELS_ATTE.Requestremoteattendance()
            requestremoteattendanceinstance.date=date
            requestremoteattendanceinstance.in_time=inlog.time
            requestremoteattendanceinstance.out_time=outlog.time
            requestremoteattendanceinstance.in_out_times=[remotelog.time for remotelog in remotelogs]
            requestremoteattendanceinstance.status=CHOICE.STATUS[0][1]
            requestremoteattendanceinstance.requested_by=MODELS_USER.User.objects.get(id=request.user.id)
            requestremoteattendanceinstance.save()
            requestremoteattendanceserializer = SRLZER_ATTE.Requestremoteattendanceserializer(requestremoteattendanceinstance, many=False)
            return Response({'status': 'success', 'message': '', 'data': requestremoteattendanceserializer.data}, status=status.HTTP_201_CREATED)
        else: return Response({'status': 'error', 'message': 'no remote logs are available', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'already exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def deleteremoteattendance(request, deleteattendenceid=None):
    requestremoteattendance = MODELS_ATTE.Requestremoteattendance.objects.filter(id=deleteattendenceid)
    if requestremoteattendance.exists():
        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestremoteattendance.first().date, employee=requestremoteattendance.first().requested_by.id)
        if attendance.exists(): attendance.delete()
        requestremoteattendance.delete()
        return Response({'status': 'success', 'message': 'deleted!', 'data': {}}, status=status.HTTP_200_OK)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def getloggedinusersremoteattendence(request):
    userid = request.user.id
    if userid:
        filter_fields = [
            {'name': 'date', 'convert': None, 'replace':'date'},
            {'name': 'in_time', 'convert': None, 'replace':'in_time'},
            {'name': 'out_time', 'convert': None, 'replace':'out_time'},
            {'name': 'status', 'convert': None, 'replace':'status__icontains'},
            {'name': 'decisioned_by', 'convert': None, 'replace':'decisioned_by'}
        ]
        kwargs = ghelp().KWARGS(request, filter_fields)
        kwargs.update({'requested_by': userid})
        requestremoteattendances = MODELS_ATTE.Requestremoteattendance.objects.filter(**kwargs)
        column_accessor = request.GET.get('column_accessor')
        if column_accessor: requestremoteattendances = requestremoteattendances.order_by(column_accessor)
        requestremoteattendanceserializers = SRLZER_ATTE.Requestremoteattendanceserializer(requestremoteattendances, many=True)
        return Response({'status': 'success', 'message': '', 'data': requestremoteattendanceserializers.data}, status=status.HTTP_200_OK)
    else: return Response({'status': 'error', 'message': 'not loggedin!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def approveremoteattendence(request, remoteattendenceid=None):
    requestremoteattendance = MODELS_ATTE.Requestremoteattendance.objects.filter(id=remoteattendenceid)
    if requestremoteattendance.exists():
        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestremoteattendance.first().date, employee=requestremoteattendance.first().requested_by.id)
        if requestremoteattendance.first().status != CHOICE.STATUS[2][1]:
            if requestremoteattendance.first().status != CHOICE.STATUS[1][1]:
                if not attendance.exists():
                    data = {'status': CHOICE.STATUS[1][1], 'decisioned_by': request.user.id}
                    requestremoteattendanceserializer = PSRLZER_ATTE.Requestremoteattendanceserializer(instance=requestremoteattendance.first(), data=data, partial=True)
                    if requestremoteattendanceserializer.is_valid(raise_exception=True):
                        requestremoteattendanceserializer.save()
                        MODELS_ATTE.Attendance(
                            date=requestremoteattendance.first().date,
                            in_time=requestremoteattendance.first().in_time,
                            out_time=requestremoteattendance.first().out_time,
                            employee=MODELS_USER.User.objects.get(id=requestremoteattendance.first().requested_by.id),
                            attendance_from=CHOICE.ATTENDANCE_FROM[2][1]
                        ).save()
                        return Response({'status': 'success', 'message': '', 'data': requestremoteattendanceserializer.data}, status=status.HTTP_200_OK)
                    else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': requestremoteattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = {'status': CHOICE.STATUS[1][1], 'decisioned_by': request.user.id}
                    requestremoteattendanceserializer = PSRLZER_ATTE.Requestremoteattendanceserializer(instance=requestremoteattendance.first(), data=data, partial=True)
                    if requestremoteattendanceserializer.is_valid(raise_exception=True):
                        requestremoteattendanceserializer.save()
                    return Response({'status': 'error', 'message': 'already attendance exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not attendance.exists():
                    MODELS_ATTE.Attendance(
                        date=requestremoteattendance.first().date,
                        in_time=requestremoteattendance.first().in_time,
                        out_time=requestremoteattendance.first().out_time,
                        employee=MODELS_USER.User.objects.get(id=requestremoteattendance.first().requested_by.id),
                        attendance_from=CHOICE.ATTENDANCE_FROM[2][1]
                    ).save()
                return Response({'status': 'error', 'message': 'already approved!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if attendance.exists(): attendance.delete()
            return Response({'status': 'error', 'message': 'it\'s rejected!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def rejectremoteattendence(request, remoteattendenceid=None):
    requestremoteattendance = MODELS_ATTE.Requestremoteattendance.objects.filter(id=remoteattendenceid)
    if requestremoteattendance.exists():

        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestremoteattendance.first().date, employee=requestremoteattendance.first().requested_by.id)
        if attendance.exists():
            attendance.delete()

        data = {'status': CHOICE.STATUS[2][1], 'decisioned_by': request.user.id}
        if request.data.get('reject_reason'): data.update({'reject_reason': request.data.get('reject_reason')})
        requestremoteattendanceserializer = PSRLZER_ATTE.Requestremoteattendanceserializer(instance=requestremoteattendance.first(), data=data, partial=True)
        if requestremoteattendanceserializer.is_valid(raise_exception=True):
            requestremoteattendanceserializer.save()
            return Response({'status': 'success', 'message': '', 'data': requestremoteattendanceserializer.data}, status=status.HTTP_200_OK)
        else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': requestremoteattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def attendancefromlogs(request, minutes=None):

    devices = [each for each in MODELS_DEVI.Device.objects.filter(is_active=True) if DEVICE().is_device_active(each.deviceip)]
    start, end = ghelp().getStarttimeEndtime(minutes)

    officialids = [each.official_id for each in MODELS_USER.User.objects.filter(is_active=True) if each.official_id]
    
    logs = {}
    for device in devices:
        DEVICE().getAllLogs(device, start, end, 100, officialids, logs)

    # Saving To Logs
    for officialid in logs.keys():
        for date in logs[officialid].keys():
            if logs[officialid][date]:
                
                for time in logs[officialid][date]:
                    employee=MODELS_USER.User.objects.get(official_id=officialid)
                    try: MODELS_ATTE.Devicelogs.objects.create(date=date, in_time=time, employee=employee)
                    except: pass

                attendance = MODELS_ATTE.Attendance.objects.filter(date=date, employee=employee)
                if attendance.exists():
                    pass
                    # attendance.update(
                    #     # in_time=logs[officialid][date][0],
                    #     out_time=logs[officialid][date][-1],
                    #     in_out_times=logs[officialid][date]
                    # )
                else:
                    MODELS_ATTE.Attendance.objects.create(
                        date=date,
                        in_time=logs[officialid][date][0],
                        out_time=logs[officialid][date][-1],
                        in_out_times=logs[officialid][date],
                        employee=employee,
                        attendance_from=CHOICE.ATTENDANCE_FROM[0][1]
                    )

    return Response({'status': 'success', 'message': '', 'data': logs}, status=status.HTTP_200_OK)