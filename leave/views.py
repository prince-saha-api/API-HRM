from django.shortcuts import render
from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from user.models import User
from officialoffday.models import Offday
from leave import models as MODELS_LEAV
from leave.serializer import serializers as SRLZER_LEAV
from rest_framework.response import Response
from rest_framework import status
from hrm_settings.models import Fiscalyear
from helps.common.generic import Generichelps as ghelp
from helps.choice.common import STATUS


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def assignleavepolicy(request):
    fiscalyear = request.data.get('fiscalyear')
    if fiscalyear != None:
        if isinstance(fiscalyear, int):
            try: fiscalyear = Fiscalyear.objects.get(id=fiscalyear)
            except: return Response({'status': 'error', 'message': 'invalid fiscalyear id!', 'data': []}, status=status.HTTP_400_BAD_REQUEST) 
        else: return Response({'status': 'error', 'message': 'fiscalyear must be a integer number!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'fiscalyear is required!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    leavepolicy = request.data.get('leavepolicy')
    if leavepolicy != None:
        if isinstance(leavepolicy, int):
            try: leavepolicy = MODELS_LEAV.Leavepolicy.objects.get(id=leavepolicy)
            except: return Response({'status': 'error', 'message': 'invalid leavepolicy id!', 'data': []}, status=status.HTTP_400_BAD_REQUEST) 
        else: return Response({'status': 'error', 'message': 'leavepolicy must be a integer number!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'leavepolicy is required!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    user = request.data.get('user')
    if user != None:
        if isinstance(user, int):
            try: user = User.objects.get(id=user)
            except: return Response({'status': 'error', 'message': 'invalid user id!', 'data': []}, status=status.HTTP_400_BAD_REQUEST) 
        else: return Response({'status': 'error', 'message': 'user must be a integer number!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'user is required!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    if user not in leavepolicy.applicable_for.user.all():
        return Response({'status': 'error', 'message': 'This user can\'t have this leave!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    

    leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user, leavepolicy=leavepolicy)
    if not leavepolicyassign.exists():
        leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.create(user=user, leavepolicy=leavepolicy)
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
        else:
            leavepolicyassign.delete()
            return Response({'status': 'error', 'message': 'this leavesummary is already exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'this leavepolicyassign is already exist!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def leaverequest(request):
    user = request.data.get('user')
    if user != None:
        if user.isnumeric():
            user = int(user)
            try: user = User.objects.get(id=user)
            except: return Response({'status': 'error', 'message': 'invalid user id!', 'data': []}, status=status.HTTP_400_BAD_REQUEST) 
        else: return Response({'status': 'error', 'message': 'user must be a integer number!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'user is required!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    leavepolicy = request.data.get('leavepolicy')
    if leavepolicy != None:
        if leavepolicy.isnumeric():
            leavepolicy = int(leavepolicy)
            try: leavepolicy = MODELS_LEAV.Leavepolicy.objects.get(id=leavepolicy)
            except: return Response({'status': 'error', 'message': 'invalid leavepolicy id!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'status': 'error', 'message': 'leavepolicy must be a integer number!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'leavepolicy is required!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    from_date = request.data.get('from_date')
    try:
        from_date=ghelp().convert_STR_datetime_date(from_date)
    except: return Response({'status': 'error', 'message': 'from_date is not valid!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    to_date = request.data.get('to_date')
    try:
        to_date=ghelp().convert_STR_datetime_date(to_date)
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

        if leavepolicy.max_consecutive_days == 0:
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
                    leaverequest.status=STATUS[0][0]
                    leaverequest.save()
                    return Response({'status': 'success', 'message': dates, 'data': []}, status=status.HTTP_200_OK)
                
                else: return Response({'status': 'error', 'message': 'all the day\'s are holiday!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
            else: return Response({'status': 'error', 'message': f'you have left {total_left} leave - {leavepolicy.name}!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        elif len(dates)<=leavepolicy.max_consecutive_days:
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


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def approveleaverequest(request, leaverequest=None):

    if leaverequest != None:
        if isinstance(leaverequest, int):
            try: leaverequest = MODELS_LEAV.Leaverequest.objects.filter(id=leaverequest)
            except: return Response({'status': 'error', 'message': 'invalid leaverequest id!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'status': 'error', 'message': 'leaverequest must be a integer number!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'status': 'error', 'message': 'leaverequest is required!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)


    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
    if leavesummary.first().total_left >= len(leaverequest.first().valid_leave_dates):
        
        for date in leaverequest.first().valid_leave_dates:
            leaveallocation = MODELS_LEAV.Leaveallocation.objects.filter(
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
                # approved_by=approved_by
            )

        leaverequest.update(
            status=STATUS[1][1],
            # approved_by=approved_by
        )

        total_consumed = leavesummary.first().total_consumed + len(leaverequest.first().valid_leave_dates)
        total_left = leavesummary.first().total_allocation - total_consumed
        leavesummary.update(
            total_consumed=total_consumed,
            total_left=total_left
        )
        return Response({'status': 'success', 'message': 'dates', 'data': []}, status=status.HTTP_200_OK)
    else: return Response({'status': 'success', 'message': f'you have left {leavesummary.first().total_left} leave - {leavesummary.first().leavepolicy.name}!', 'data': []}, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getleavepolicys(request):
    leavepolicys = MODELS_LEAV.Leavepolicy.objects.all()
    leavepolicyserializers = SRLZER_LEAV.Leavepolicyserializer(leavepolicys, many=True)
    return Response(leavepolicyserializers.data, status=status.HTTP_200_OK)