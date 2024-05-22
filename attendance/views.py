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
from user.models import User


# ----------------------------------------------------------
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addmanualattendence(request):
    requestmanualattendanceserializer = SRLZER_ATTE.Requestmanualattendanceserializer(data=request.data, many=False)
    if requestmanualattendanceserializer.is_valid():
        requestmanualattendanceserializer.save()
        return Response({'status': 'success', 'message': '', 'data': requestmanualattendanceserializer.data}, status=status.HTTP_201_CREATED)
    else: return Response({'status': 'error', 'message': '', 'data': requestmanualattendanceserializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------


# ----------------------------------------------------------
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addattendancefromlogsalldevices(request, minutes):

    devices = Device.objects.filter(is_active=True)
    start , end = ghelp().getStarttimeEndtime(minutes)

    usernames = [cuser.username for cuser in User.objects.all()]
    # usernames = ['rashed', 'shakil', 'tamim_pm', 'NAYEEM']

    
    logs = {}
    for device in devices: dhelp().getAllLogs(device, start, end, 100, usernames, logs)

    # Saving To Logs
    for username in logs.keys():
        for date in logs[username].keys():
            for inout_time in logs[username][date]:
                employee=User.objects.get(username=username)
                try: MODELS_ATTE.Devicelogs.objects.create(date=date, in_time=inout_time, employee=employee)
                except: pass

    for username in logs.keys():
        for date in logs[username].keys():

            employee = User.objects.get(username=username)
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

# ----------------------------------------------------------


# ----------------------------------------------------------
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addremoteattendance(request, userid, date):
    user = User.objects.filter(id=userid)
    if user.exists():
        user = user.first()
        remotelogs = MODELS_ATTE.Remotelogs.objects.filter(date=date, employee=user).order_by('time')
        if remotelogs.count()>0:
            inlog = remotelogs.first()
            outlog = remotelogs.last()

            MODELS_ATTE.Requestremoteattendance(
                date=date,
                in_time=inlog.time,
                out_time=outlog.time,
                in_out_times=[remotelog.time for remotelog in remotelogs],
                status=STATUS[0][1],
                requested_by=user
            ).save()
            return Response({'status': 'success', 'message': '', 'data': []}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'message': 'no remote logs are available', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'user doesn\'t exist!', 'data': []}, status=status.HTTP_404_NOT_FOUND)

# ----------------------------------------------------------