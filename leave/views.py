from django.shortcuts import render
from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from user import models as MODELS_USER
from officialoffday.models import Offday
from leave import models as MODELS_LEAV
from leave.serializer import serializers as SRLZER_LEAV
from rest_framework.response import Response
from rest_framework import status
from hrm_settings import models as MODELS_SETT
from helps.common.generic import Generichelps as ghelp
from helps.choice.common import STATUS
import json

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getleavepolicys(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'user', 'convert': None, 'replace':'leavepolicyassign__user__id'},
                        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
                        {'name': 'allocation_days', 'convert': None, 'replace':'allocation_days'},
                        {'name': 'leave_type', 'convert': None, 'replace':'leave_type__icontains'},
                        {'name': 'applicable_for', 'convert': None, 'replace':'applicable_for'},
                        {'name': 'max_consecutive_days', 'convert': None, 'replace':'max_consecutive_days'},
                        {'name': 'require_attachment', 'convert': 'bool', 'replace':'require_attachment'},
                        {'name': 'is_optional', 'convert': 'bool', 'replace':'is_optional'},
                        {'name': 'is_calendar_day', 'convert': 'bool', 'replace':'is_calendar_day'}
                    ]
    leavepolicys = MODELS_LEAV.Leavepolicy.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: leavepolicys = leavepolicys.order_by(column_accessor)
    leavepolicyserializers = SRLZER_LEAV.Leavepolicyserializer(leavepolicys, many=True)
    return Response({'data': leavepolicyserializers.data, 'message': '', 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addleavepolicy(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid, 'created_by': userid})
    allowed_fields = ['__all__']
    unique_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_LEAV.Leavepolicy, SRLZER_LEAV.Leavepolicyserializer, request.data, allowed_fields=allowed_fields, unique_fields=unique_fields, extra_fields=extra_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def assignleavepolicy(request):
    check_mood = True

    fiscalyear = ghelp().getobject(MODELS_SETT.Fiscalyear, {'id': request.data.get('fiscalyear')})
    leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': request.data.get('leavepolicy')})
    user = ghelp().getobject(MODELS_USER.User, {'id': request.data.get('user')})
    if check_mood:
        if fiscalyear == None: return Response({'status': 'error', 'message': 'fiscalyear doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        if leavepolicy == None: return Response({'status': 'error', 'message': 'leavepolicy doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        if user == None: return Response({'status': 'error', 'message': 'user doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)


    if leavepolicy.applicable_for.name != 'all':
        if user not in leavepolicy.applicable_for.user.all():
            return Response({'status': 'error', 'message': 'This user can\'t have this leave!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    

    leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user, leavepolicy=leavepolicy)
    if not leavepolicyassign.exists():
        created_by = MODELS_USER.User.objects.get(id=request.user.id)
        leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.create(user=user, leavepolicy=leavepolicy, created_by=created_by, updated_by=created_by)
        leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
        if not leavesummary.exists():
            MODELS_LEAV.Leavesummary.objects.create(
                user=user,
                leavepolicy=leavepolicy,
                fiscal_year=fiscalyear,
                total_allocation=leavepolicy.allocation_days,
                total_consumed=0,
                total_left=leavepolicy.allocation_days
            )
            return Response({'status': 'success', 'message': '', 'data': []}, status=status.HTTP_200_OK)
        else: return Response({'status': 'error', 'message': 'this leavesummary is already exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'this leavepolicyassign is already exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getleavesummarys(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'user', 'convert': None, 'replace':'user'},
                        {'name': 'leavepolicy', 'convert': None, 'replace':'leavepolicy'},
                        {'name': 'total_allocation', 'convert': None, 'replace':'total_allocation'},
                        {'name': 'total_consumed', 'convert': None, 'replace':'total_consumed'},
                        {'name': 'total_left', 'convert': None, 'replace':'total_left'},
                        {'name': 'fiscal_year', 'convert': None, 'replace':'fiscal_year'}
                    ]
    leavesummarys = MODELS_LEAV.Leavesummary.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: leavesummarys = leavesummarys.order_by(column_accessor)
    leavesummaryserializers = SRLZER_LEAV.Leavesummaryserializer(leavesummarys, many=True)
    return Response(leavesummaryserializers.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getleaverequest(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'user', 'convert': None, 'replace':'user'},
                        {'name': 'leavepolicy', 'convert': None, 'replace':'leavepolicy'},
                        {'name': 'from_date', 'convert': None, 'replace':'from_date'},
                        {'name': 'to_date', 'convert': None, 'replace':'to_date'},
                        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
                        {'name': 'status', 'convert': None, 'replace':'status__icontains'},
                        {'name': 'rejection_reason', 'convert': None, 'replace':'rejection_reason__icontains'},
                        {'name': 'approved_by', 'convert': None, 'replace':'approved_by'}
                    ]
    leaverequests = MODELS_LEAV.Leaverequest.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: leaverequests = leaverequests.order_by(column_accessor)
    leaverequestserializers=SRLZER_LEAV.Leaverequestserializer(leaverequests, many=True)
    return Response({'status': 'success', 'message': '', 'data': leaverequestserializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def addleaverequest(request):
    check_mood = True
    user = MODELS_USER.User.objects.get(id=request.user.id)

    leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': request.data.get('leavepolicy')})
    if check_mood:
        if leavepolicy == None: return Response({'status': 'error', 'message': 'leavepolicy doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)


    from_date = request.data.get('from_date')
    try: from_date=ghelp().convert_STR_datetime_date(from_date)
    except: return Response({'status': 'error', 'message': 'from_date is not valid!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    to_date = request.data.get('to_date')
    try: to_date=ghelp().convert_STR_datetime_date(to_date)
    except: return Response({'status': 'error', 'message': 'to_date is not valid!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    description = request.data.get('description')
    attachment = request.FILES.get('attachment')

    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
    if leavesummary.exists():

        # Section to calculate date based on is_calendar_day
        daycount = (to_date - from_date).days + 1
        dates = []
        if leavepolicy.is_calendar_day:
            for day in range(daycount):
                
                filter_date = from_date + timedelta(day)
                if ghelp().is_date_in_range(filter_date, leavesummary.first().fiscal_year.from_date, leavesummary.first().fiscal_year.to_date):
                    dates.append(filter_date)
                else: return Response({'status': 'error', 'message': 'applied date is not in this fiscal year!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        else:
            for day in range(daycount):
                date = from_date + timedelta(day)
                offday = Offday.objects.filter(is_active=True, day=ghelp().convert_y_m_d_STR_day(date))
                if not offday.exists():
                    holiday = MODELS_LEAV.Holiday.objects.filter(date=date, employee_grade=user.grade)
                    if not holiday.exists():
                        filter_date = from_date + timedelta(day)
                        if ghelp().is_date_in_range(filter_date, leavesummary.first().fiscal_year.from_date, leavesummary.first().fiscal_year.to_date):
                            dates.append(filter_date)
                        else: return Response({'status': 'error', 'message': 'applied date is not in this fiscal year!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

        if leavepolicy.max_consecutive_days == 0 or len(dates)<=leavepolicy.max_consecutive_days:
            total_left = leavesummary.first().total_left
            if len(dates)<=total_left:

                if leavepolicy.require_attachment:
                    if not attachment: return Response({'status': 'error', 'message': 'attachment is required!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
                
                if len(dates)>0:
                    leaverequest=MODELS_LEAV.Leaverequest()
                    leaverequest.user=user
                    leaverequest.leavepolicy=leavepolicy
                    leaverequest.from_date=from_date
                    leaverequest.to_date=to_date
                    leaverequest.total_leave=len(dates)
                    leaverequest.valid_leave_dates=dates
                    if attachment: leaverequest.attachment=attachment
                    if description: leaverequest.description=description
                    leaverequest.status=STATUS[0][1]
                    leaverequest.save()
                    return Response({'status': 'success', 'message': dates, 'data': []}, status=status.HTTP_200_OK)
                
                else: return Response({'status': 'error', 'message': 'all the day\'s are holiday!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
            else: return Response({'status': 'error', 'message': f'you have left {total_left} leave - {leavepolicy.name}!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'status': 'error', 'message': f'max_consecutive_days {leavepolicy.max_consecutive_days} have been exceeded!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': f'you are not permitted to have {leavepolicy.name} leave!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def approveleaverequest(request, leaverequest=None):
    check_mood = True

    if leaverequest:
        leaverequest = ghelp().getobject(MODELS_LEAV.Leaverequest, {'id': leaverequest}, True)

        if check_mood:
            if leaverequest == None: return Response({'status': 'error', 'message': 'leaverequest doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

        leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
        if leavesummary.first().total_left >= len(leaverequest.first().valid_leave_dates):
            
            for date in leaverequest.first().valid_leave_dates:
                leaveallocation = MODELS_LEAV.Approvedleave.objects.filter(
                    leavepolicy=leaverequest.first().leavepolicy,
                    user=leaverequest.first().user,
                    date=date
                )
                if leaveallocation.exists(): return Response({'status': 'error', 'message': 'already exist in leaveallocation!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

            for date in leaverequest.first().valid_leave_dates:
                MODELS_LEAV.Approvedleave.objects.create(
                    leavepolicy=leaverequest.first().leavepolicy,
                    user=leaverequest.first().user,
                    date=date,
                    approved_by=MODELS_USER.User.objects.get(id=request.user.id)
                )

            leaverequest.update(status=STATUS[1][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))

            total_consumed = leavesummary.first().total_consumed + len(leaverequest.first().valid_leave_dates)
            total_left = leavesummary.first().total_allocation - total_consumed
            leavesummary.update(total_consumed=total_consumed, total_left=total_left)
            return Response({'status': 'success', 'message': 'dates', 'data': []}, status=status.HTTP_200_OK)
        else: return Response({'status': 'error', 'message': f'you have left {leavesummary.first().total_left} leave - {leavesummary.first().leavepolicy.name}!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'provide a leaverequest id!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getfilteredleaverequest(request):
    kwargs = {}
    userid = request.GET.get('userid')
    if userid:
        if userid.isnumeric(): kwargs.update({'user__id': int(userid)})

    leaverequeststatus = request.GET.get('status')
    if leaverequeststatus: kwargs.update({'status__icontains': leaverequeststatus})

    leaverequests = MODELS_LEAV.Leaverequest.objects.filter(**kwargs)
    leaverequestserializers = SRLZER_LEAV.Leaverequestserializer(leaverequests, many=True)
    return Response({'data': leaverequestserializers.data, 'message': '', 'status': 'success'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getleaveallocationrequest(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'user', 'convert': None, 'replace':'user'},
                        {'name': 'leavepolicy', 'convert': None, 'replace':'leavepolicy'},
                        {'name': 'no_of_days', 'convert': None, 'replace':'no_of_days'},
                        {'name': 'reason', 'convert': None, 'replace':'reason__icontains'},
                        {'name': 'status', 'convert': None, 'replace':'status__icontains'},
                        {'name': 'approved_by', 'convert': None, 'replace':'approved_by'}
                    ]
    leaveallocationrequests = MODELS_LEAV.Leaveallocationrequest.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: leaveallocationrequests = leaveallocationrequests.order_by(column_accessor)
    leaveallocationrequestserializers=SRLZER_LEAV.Leaveallocationrequestserializer(leaveallocationrequests, many=True)
    return Response({'status': 'success', 'message': '', 'data': leaveallocationrequestserializers.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def addleaveallocationrequest(request):
    check_mood = True
    user = MODELS_USER.User.objects.get(id=request.user.id)

    leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': request.data.get('leavepolicy')})
    if check_mood:
        if leavepolicy == None: return Response({'status': 'error', 'message': 'leavepolicy doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    
    no_of_days = request.data.get('no_of_days')
    reason = request.data.get('reason')
    
    if no_of_days>0:
        leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
        if leavesummary.exists():
            leaveallocationrequestinstance = MODELS_LEAV.Leaveallocationrequest()
            leaveallocationrequestinstance.user=user
            leaveallocationrequestinstance.leavepolicy=leavepolicy
            leaveallocationrequestinstance.no_of_days=no_of_days
            if reason: leaveallocationrequestinstance.reason=reason
            leaveallocationrequestinstance.status=STATUS[0][1]
            leaveallocationrequestinstance.save()
            return Response({'status': 'success', 'message': '', 'data': []}, status=status.HTTP_200_OK)
        else: return Response({'status': 'error', 'message': 'leavesummary doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'no_of_days is required!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def approverequestleaveallocation(request, leaveallocationrequest=None):
    check_mood = True

    if leaveallocationrequest:
        approved_by = MODELS_USER.User.objects.get(id=request.user.id)

        leaveallocationrequest = ghelp().getobject(MODELS_LEAV.Leaveallocationrequest, {'id': leaveallocationrequest}, True)
        if check_mood:
            if not leaveallocationrequest.exists(): return Response({'status': 'error', 'message': 'leaveallocationrequest doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

        leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaveallocationrequest.first().user, leavepolicy=leaveallocationrequest.first().leavepolicy)
        if leavesummary.exists():
            total_allocation = leavesummary.first().total_allocation + leaveallocationrequest.first().no_of_days
            total_left = leavesummary.first().total_left + leaveallocationrequest.first().no_of_days
            leavesummary.update(total_allocation=total_allocation, total_left=total_left)
            leaveallocationrequest.update(status=STATUS[1][1], approved_by=approved_by)
            return Response({'status': 'success', 'message': '', 'data': []}, status=status.HTTP_200_OK)
        else: return Response({'status': 'error', 'message': 'leavesummary doesn\'t exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'provide a leaveallocationrequest id!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)