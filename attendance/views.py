from django.shortcuts import render
from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from helps.choice.common import ATTENDANCE_FROM, STATUS
from rest_framework.permissions import IsAuthenticated
from helps.common.generic import Generichelps as ghelp
from helps.accesscontroldevice.a_devicehelp import Decicehelps as dhelp
from attendance import models as MODELS_ATTE
from attendance.serializer import serializers as SRLZER_ATTE
from device.models import Device
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
    requestmanualattendances = MODELS_ATTE.Requestmanualattendance.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: requestmanualattendances = requestmanualattendances.order_by(column_accessor)
    requestmanualattendanceserializers = SRLZER_ATTE.Requestmanualattendanceserializer(requestmanualattendances, many=True)
    return Response({'status': 'success', 'message': '', 'data': requestmanualattendanceserializers.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addmanualattendence(request):
    date = request.data.get('date')
    if date == None: return Response({'status': 'error', 'message': 'date is required!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
    
    request.data.update({'requested_by': request.user.id})
    requestmanualattendance = MODELS_ATTE.Requestmanualattendance.objects.filter(date=date, requested_by=request.user.id)
    
    if not requestmanualattendance.exists():
        requestmanualattendanceserializers = SRLZER_ATTE.Requestmanualattendanceserializer(data=request.data, many=False)
        if requestmanualattendanceserializers.is_valid():
            requestmanualattendanceserializers.save()
            return Response({'status': 'success', 'message': '', 'data': requestmanualattendanceserializers.data}, status=status.HTTP_201_CREATED)
        else: return Response({'status': 'error', 'message': '', 'data': requestmanualattendanceserializers.errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'already exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def getloggedinusersmanualattendence(request):
    userid = request.user.id
    filter_fields = [
                        {'name': 'date', 'convert': None, 'replace':'date'},
                        {'name': 'in_time', 'convert': None, 'replace':'in_time'},
                        {'name': 'out_time', 'convert': None, 'replace':'out_time'},
                        {'name': 'status', 'convert': None, 'replace':'status__icontains'},
                        {'name': 'decisioned_by', 'convert': None, 'replace':'decisioned_by'}
                    ]
    kwargs = ghelp().KWARGS(request, filter_fields)
    kwargs.update({'requested_by': userid})
    requestmanualattendances = MODELS_ATTE.Requestmanualattendance.objects.filter(**kwargs)
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: requestmanualattendances = requestmanualattendances.order_by(column_accessor)
    requestmanualattendanceserializer = SRLZER_ATTE.Requestmanualattendanceserializer(requestmanualattendances, many=True)
    return Response({'status': 'success', 'message': '', 'data': requestmanualattendanceserializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def updatemanualattendence(request, manualattendenceid):
    requestmanualattendance = MODELS_ATTE.Requestmanualattendance.objects.filter(id=manualattendenceid)
    if requestmanualattendance.exists():
        data = {}
        date = request.data.get('date')
        if date != None: data.update({'date': date})

        in_time = request.data.get('in_time')
        if in_time != None: data.update({'in_time': in_time})
        out_time = request.data.get('out_time')
        if out_time != None: data.update({'out_time': out_time})

        requestmanualattendanceserializer = SRLZER_ATTE.Requestmanualattendanceserializer(instance=requestmanualattendance.first(), data=data, partial=True)
        if requestmanualattendanceserializer.is_valid(raise_exception=True):
            try: 
                requestmanualattendanceserializer.save()
                return Response({'status': 'success', 'message': '', 'data': requestmanualattendanceserializer.data}, status=status.HTTP_200_OK)
            except: return Response({'status': 'error', 'message': 'already exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': requestmanualattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def approvemanualattendence(request, manualattendenceid):
    requestmanualattendance = MODELS_ATTE.Requestmanualattendance.objects.filter(id=manualattendenceid)
    if requestmanualattendance.exists():
        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestmanualattendance.first().date, employee=requestmanualattendance.first().requested_by.id)
        if requestmanualattendance.first().status != STATUS[2][1]:
            if requestmanualattendance.first().status != STATUS[1][1]:
                if not attendance.exists():
                    data = {'status': STATUS[1][1], 'decisioned_by': request.user.id}
                    requestmanualattendanceserializer = SRLZER_ATTE.Requestmanualattendanceserializer(instance=requestmanualattendance.first(), data=data, partial=True)
                    if requestmanualattendanceserializer.is_valid(raise_exception=True):
                        requestmanualattendanceserializer.save()
                        MODELS_ATTE.Attendance(
                            date=requestmanualattendance.first().date,
                            in_time=requestmanualattendance.first().in_time,
                            out_time=requestmanualattendance.first().out_time,
                            employee=MODELS_USER.User.objects.get(id=requestmanualattendance.first().requested_by.id),
                            attendance_from=ATTENDANCE_FROM[1][1]
                        ).save()
                        return Response({'status': 'success', 'message': '', 'data': requestmanualattendanceserializer.data}, status=status.HTTP_200_OK)
                    else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': requestmanualattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = {'status': STATUS[1][1], 'decisioned_by': request.user.id}
                    requestmanualattendanceserializer = SRLZER_ATTE.Requestmanualattendanceserializer(instance=requestmanualattendance.first(), data=data, partial=True)
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
                        attendance_from=ATTENDANCE_FROM[1][1]
                    ).save()
                return Response({'status': 'error', 'message': 'already approved!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if attendance.exists(): attendance.delete()
            return Response({'status': 'error', 'message': 'it\'s rejected!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def rejectmanualattendence(request, manualattendenceid):
    requestmanualattendance = MODELS_ATTE.Requestmanualattendance.objects.filter(id=manualattendenceid)
    if requestmanualattendance.exists():

        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestmanualattendance.first().date, employee=requestmanualattendance.first().requested_by.id)
        if attendance.exists():
            attendance.delete()

        data = {'status': STATUS[2][1], 'decisioned_by': request.user.id}
        if request.data.get('reject_reason'): data.update({'reject_reason': request.data.get('reject_reason')})
        requestmanualattendanceserializer = SRLZER_ATTE.Requestmanualattendanceserializer(instance=requestmanualattendance.first(), data=data, partial=True)
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
    remotelogsserializers = SRLZER_ATTE.Remotelogsserializer(remotelogs, many=True)
    return Response({'status': 'success', 'message': '', 'data': remotelogsserializers.data}, status=status.HTTP_200_OK)

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
        remotelogsserializer = SRLZER_ATTE.Remotelogsserializer(data=request.data, many=False)
        if remotelogsserializer.is_valid():
            remotelogsserializer.save()
            return Response({'status': 'success', 'message': '', 'data': remotelogsserializer.data}, status=status.HTTP_201_CREATED)
        else: return Response({'status': 'error', 'message': '', 'data': remotelogsserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'already exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def updateremotelog(request, remotelogid):
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

        remotelogsserializer = SRLZER_ATTE.Remotelogsserializer(instance=remotelogs.first(), data=data, partial=True)
        if remotelogsserializer.is_valid(raise_exception=True):
            try:
                remotelogsserializer.save()
                return Response({'status': 'success', 'message': '', 'data': remotelogsserializer.data}, status=status.HTTP_200_OK)
            except: return Response({'status': 'error', 'message': 'can\'t update, already exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': remotelogsserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
    requestremoteattendanceserializers = SRLZER_ATTE.Requestremoteattendanceserializer(requestremoteattendances, many=True)
    return Response({'status': 'success', 'message': '', 'data': requestremoteattendanceserializers.data}, status=status.HTTP_200_OK)

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
            requestremoteattendanceinstance.status=STATUS[0][1]
            requestremoteattendanceinstance.requested_by=MODELS_USER.User.objects.get(id=request.user.id)
            requestremoteattendanceinstance.save()
            requestremoteattendanceserializer = SRLZER_ATTE.Requestremoteattendanceserializer(requestremoteattendanceinstance, many=False)
            return Response({'status': 'success', 'message': '', 'data': requestremoteattendanceserializer.data}, status=status.HTTP_201_CREATED)
        else: return Response({'status': 'error', 'message': 'no remote logs are available', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'already exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def getloggedinusersremoteattendence(request):
    userid = request.user.id
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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def approveremoteattendence(request, remoteattendenceid):
    requestremoteattendance = MODELS_ATTE.Requestremoteattendance.objects.filter(id=remoteattendenceid)
    if requestremoteattendance.exists():
        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestremoteattendance.first().date, employee=requestremoteattendance.first().requested_by.id)
        if requestremoteattendance.first().status != STATUS[2][1]:
            if requestremoteattendance.first().status != STATUS[1][1]:
                if not attendance.exists():
                    data = {'status': STATUS[1][1], 'decisioned_by': request.user.id}
                    requestremoteattendanceserializer = SRLZER_ATTE.Requestremoteattendanceserializer(instance=requestremoteattendance.first(), data=data, partial=True)
                    if requestremoteattendanceserializer.is_valid(raise_exception=True):
                        requestremoteattendanceserializer.save()
                        MODELS_ATTE.Attendance(
                            date=requestremoteattendance.first().date,
                            in_time=requestremoteattendance.first().in_time,
                            out_time=requestremoteattendance.first().out_time,
                            employee=MODELS_USER.User.objects.get(id=requestremoteattendance.first().requested_by.id),
                            attendance_from=ATTENDANCE_FROM[2][1]
                        ).save()
                        return Response({'status': 'success', 'message': '', 'data': requestremoteattendanceserializer.data}, status=status.HTTP_200_OK)
                    else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': requestremoteattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = {'status': STATUS[1][1], 'decisioned_by': request.user.id}
                    requestremoteattendanceserializer = SRLZER_ATTE.Requestremoteattendanceserializer(instance=requestremoteattendance.first(), data=data, partial=True)
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
                        attendance_from=ATTENDANCE_FROM[2][1]
                    ).save()
                return Response({'status': 'error', 'message': 'already approved!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if attendance.exists(): attendance.delete()
            return Response({'status': 'error', 'message': 'it\'s rejected!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def rejectremoteattendence(request, remoteattendenceid):
    requestremoteattendance = MODELS_ATTE.Requestremoteattendance.objects.filter(id=remoteattendenceid)
    if requestremoteattendance.exists():

        attendance = MODELS_ATTE.Attendance.objects.filter(date=requestremoteattendance.first().date, employee=requestremoteattendance.first().requested_by.id)
        if attendance.exists():
            attendance.delete()

        data = {'status': STATUS[2][1], 'decisioned_by': request.user.id}
        if request.data.get('reject_reason'): data.update({'reject_reason': request.data.get('reject_reason')})
        requestremoteattendanceserializer = SRLZER_ATTE.Requestremoteattendanceserializer(instance=requestremoteattendance.first(), data=data, partial=True)
        if requestremoteattendanceserializer.is_valid(raise_exception=True):
            requestremoteattendanceserializer.save()
            return Response({'status': 'success', 'message': '', 'data': requestremoteattendanceserializer.data}, status=status.HTTP_200_OK)
        else: return Response({'status': 'error', 'message': 'something went wrong!', 'data': requestremoteattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'doesn\'t exist!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addattendancefromlogsalldevices(request, minutes):

    devices = Device.objects.filter(is_active=True)
    start , end = ghelp().getStarttimeEndtime(minutes)

    usernames = [cuser.username for cuser in MODELS_USER.User.objects.all()]
    # usernames = ['rashed', 'shakil', 'tamim_pm', 'NAYEEM']

    
    logs = {}
    for device in devices: dhelp().getAllLogs(device, start, end, 100, usernames, logs)

    # Saving To Logs
    for username in logs.keys():
        for date in logs[username].keys():
            for inout_time in logs[username][date]:
                employee=MODELS_USER.User.objects.get(username=username)
                try: MODELS_ATTE.Devicelogs.objects.create(date=date, in_time=inout_time, employee=employee)
                except: pass

    for username in logs.keys():
        for date in logs[username].keys():

            employee = MODELS_USER.User.objects.get(username=username)
            assending_logs = MODELS_ATTE.Devicelogs.objects.filter(date=date, employee=employee).order_by('in_time')
            if assending_logs.count()>=1:
                intime = assending_logs.first().in_time
                outtime = assending_logs.last().in_time

                attendance = MODELS_ATTE.Attendance.objects.filter(date=date, employee=employee)
                if attendance.exists():

                    attendance.update(
                        in_time=intime,
                        out_time=outtime,
                        in_out_times=[assending_log.in_time for assending_log in assending_logs]
                    )
                else:
                    MODELS_ATTE.Attendance.objects.create(
                        date=date,
                        in_time=intime,
                        out_time=outtime,
                        in_out_times=[assending_log.in_time for assending_log in assending_logs],
                        employee=employee,
                        attendance_from=ATTENDANCE_FROM[0][1]
                    )

    return Response({'status': 'success', 'message': '', 'data': logs}, status=status.HTTP_200_OK)