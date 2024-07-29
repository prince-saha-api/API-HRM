from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from user import models as MODELS_USER
from leave import models as MODELS_LEAV
from leave.serializer import serializers as SRLZER_LEAV
from leave.serializer.POST import serializers as PSRLZER_LEAV
from rest_framework.response import Response
from rest_framework import status
from hrm_settings import models as MODELS_SETT
from helps.common.generic import Generichelps as ghelp
from helps.choice import common as CHOICE

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getleavepolicys(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'leavepolicyassign__user__id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
        {'name': 'allocation_days', 'convert': None, 'replace':'allocation_days'},
        {'name': 'leave_type', 'convert': None, 'replace':'leave_type__icontains'},
        {'name': 'max_consecutive_days', 'convert': None, 'replace':'max_consecutive_days'},
        {'name': 'require_attachment', 'convert': 'bool', 'replace':'require_attachment'},
        {'name': 'is_optional', 'convert': 'bool', 'replace':'is_optional'},
        {'name': 'is_calendar_day', 'convert': 'bool', 'replace':'is_calendar_day'}
    ]
    leavepolicys = MODELS_LEAV.Leavepolicy.objects.filter(**ghelp().KWARGS(request, filter_fields))

    column_accessor = request.GET.get('column_accessor')
    if column_accessor: leavepolicys = leavepolicys.order_by(column_accessor)
    
    total_count = leavepolicys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: leavepolicys=leavepolicys[(page-1)*page_size:page*page_size]

    leavepolicyserializers = SRLZER_LEAV.Leavepolicyserializer(leavepolicys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': leavepolicyserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addleavepolicy(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid, 'created_by': userid})
    unique_fields = ['name']
    required_fields = ['name', 'leave_type']
    choice_fields = [
        {'name': 'leave_type', 'values': [item[1] for item in CHOICE.LEAVE_TYPE]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_LEAV.Leavepolicy, 
        Serializer=PSRLZER_LEAV.Leavepolicyserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        extra_fields=extra_fields, 
        choice_fields=choice_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateleavepolicy(request, leavepolicyid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    leavepolicys = MODELS_LEAV.Leavepolicy.objects.filter(id=leavepolicyid)
    if leavepolicys.exists():
        leavepolicys = leavepolicys.first()
        allowed_fields = ['name', 'description', 'leave_type', 'max_consecutive_days', 'require_attachment', 'is_optional', 'is_calendar_day', 'is_active']

        allocation_days = request.data.get('allocation_days')
        if allocation_days != None:
            allocation_days = int(allocation_days)
            if allocation_days != leavepolicys.allocation_days:
                if allocation_days > leavepolicys.allocation_days: allowed_fields.append('allocation_days')
                else: response_message.append('allocation_days must have to be incresed compared to previous allocation_days!') 

        if not response_message:
            extra_fields = {}
            userid = request.user.id
            if userid: extra_fields.update({'updated_by': userid})
            unique_fields=['name']
            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                classOBJ=MODELS_LEAV.Leavepolicy,
                Serializer=PSRLZER_LEAV.Leavepolicyserializer,
                id=leavepolicyid,
                data=request.data,
                unique_fields=unique_fields,
                allowed_fields=allowed_fields,
                extra_fields=extra_fields
            )
            response_data.update(responsedata)
            response_message.extend(responsemessage)
            response_successflag = responsesuccessflag
            response_status = responsestatus
    else: response_message.append('doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteleavepolicy(request, leavepolicyid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_LEAV.Leavepolicyassign, 'fields': [{'field': 'leavepolicy', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_LEAV.Approvedleave, 'fields': [{'field': 'leavepolicy', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_LEAV.Leavesummary, 'fields': [{'field': 'leavepolicy', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_LEAV.Leaveallocationrequest, 'fields': [{'field': 'leavepolicy', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_LEAV.Leaverequest, 'fields': [{'field': 'leavepolicy', 'relation': 'foreignkey', 'records': []}]},
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_LEAV.Leavepolicy,
        id=leavepolicyid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getassignleavepolicys(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'leavepolicy', 'convert': None, 'replace':'leavepolicy'},
        {'name': 'updated_by', 'convert': None, 'replace':'updated_by'},
        {'name': 'created_by', 'convert': None, 'replace':'created_by'}
    ]
    leavepolicyassigns = MODELS_LEAV.Leavepolicyassign.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: leavepolicyassigns = leavepolicyassigns.order_by(column_accessor)

    total_count = leavepolicyassigns.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: leavepolicyassigns = leavepolicyassigns[(page-1)*page_size:page*page_size]

    leavepolicyassignserializers = SRLZER_LEAV.Leavepolicyassignserializer(leavepolicyassigns, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': leavepolicyassignserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def assignleavepolicy(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    generalsettings = MODELS_SETT.Generalsettings.objects.all().order_by('id')
    if generalsettings.exists():
        leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': request.data.get('leavepolicy')})
        if leavepolicy:
            user = ghelp().getobject(MODELS_USER.User, {'id': request.data.get('user')})
            if user:
                # if leavepolicy.applicable_for.name != 'all':
                #     if user not in leavepolicy.applicable_for.user.all():
                #         return Response({'data': {}, 'message': ['This user can\'t have this leave!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                

                leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user, leavepolicy=leavepolicy)
                if not leavepolicyassign.exists():
                    created_by = MODELS_USER.User.objects.get(id=request.user.id)
                    leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.create(user=user, leavepolicy=leavepolicy, created_by=created_by, updated_by=created_by)
                    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
                    if not leavesummary.exists():
                        MODELS_LEAV.Leavesummary.objects.create(
                            user=user,
                            leavepolicy=leavepolicy,
                            fiscal_year=generalsettings.first().fiscalyear,
                            total_allocation=leavepolicy.allocation_days,
                            total_consumed=0,
                            total_left=leavepolicy.allocation_days
                        )
                        response_successflag = 'success'
                        response_status = status.HTTP_200_OK
                    else: response_message.append('this leavesummary is already exist!')
                else: response_message.append('this leavepolicyassign is already exist!')
            else: response_message.append('user doesn\'t exist!')
        else: response_message.append('leavepolicy doesn\'t exist!')
    else: response_message.append('please fillup general settings first!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def removeassignedleavepolicy(request, leavepolicyassignid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    if leavepolicyassignid:
        leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(id=leavepolicyassignid)
        if leavepolicyassign.exists():
            leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leavepolicyassign.first().user, leavepolicy=leavepolicyassign.first().leavepolicy)
            if leavesummary.exists():
                if leavesummary.first().total_consumed == 0:
                    leaverequest = MODELS_LEAV.Leaverequest.objects.filter(user=leavesummary.first().user, leavepolicy=leavesummary.first().leavepolicy)
                    if leaverequest.exists():
                        if leaverequest.first().status in [CHOICE.STATUS[0][1], CHOICE.STATUS[2][1]]:
                            leaverequest.delete()
                            leavesummary.delete()
                            leavepolicyassign.delete()

                            response_message.append('successfully deleted!')
                            response_successflag = 'success'
                            response_status = status.HTTP_200_OK
                        else: response_message.append(f'can\'t delete, leaverequest is already {leaverequest.first().status}, please solve it manually!')
                    else:
                        leavesummary.delete()
                        leavepolicyassign.delete()

                        response_message.append('successfully deleted!')
                        response_successflag = 'success'
                        response_status = status.HTTP_200_OK

                else: response_message.append(f'can\'t remove {leavesummary.first().leavepolicy.name} leave policy(already consumed {leavesummary.first().total_consumed}).')
            else:
                leavepolicyassign.delete()
                response_message.append('successfully deleted!')
                response_message.append('leavesummary is missing!')
                response_successflag = 'success'
                response_status = status.HTTP_200_OK
        else: response_message.append('leavepolicyassignid doesn\'t exist.')
    else: response_message.append('provide leavepolicyassign id.')

    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

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

    total_count = leavesummarys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: leavesummarys = leavesummarys[(page-1)*page_size:page*page_size]

    leavesummaryserializers = SRLZER_LEAV.Leavesummaryserializer(leavesummarys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': leavesummaryserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getleaverequest(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'request_type', 'convert': None, 'replace':'request_type__icontains'},
        {'name': 'exchange_with', 'convert': None, 'replace':'exchange_with'},
        {'name': 'from_date', 'convert': None, 'replace':'from_date'},
        {'name': 'to_date', 'convert': None, 'replace':'to_date'},
        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
        {'name': 'status', 'convert': None, 'replace':'status__icontains'},
        {'name': 'reason', 'convert': None, 'replace':'reason__icontains'},
        {'name': 'approved_by', 'convert': None, 'replace':'approved_by'}
    ]
    leaverequests = MODELS_LEAV.Leaverequest.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: leaverequests = leaverequests.order_by(column_accessor)

    total_count = leaverequests.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: leaverequests = leaverequests[(page-1)*page_size:page*page_size]

    leaverequestserializers=SRLZER_LEAV.Leaverequestserializer(leaverequests, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': leaverequestserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addleaverequest(request):
    requestdata = request.data.copy()

    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    user = ghelp().getobject(MODELS_USER.User, {'id': requestdata.get('user')})
    if user == None: response_message.append('required valid user!')
    leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': requestdata.get('leavepolicy')})
    if leavepolicy == None: response_message.append('required valid leavepolicy!')

    regexObj= ghelp().getregex('date')
    from_date = requestdata.get('from_date')
    to_date = requestdata.get('to_date')
    if from_date and to_date:
        try: from_date=ghelp().convert_STR_datetime_date(from_date)
        except: response_message.append(f'from_date field\'s format is {regexObj["format"]}!')
        try: to_date=ghelp().convert_STR_datetime_date(to_date)
        except: response_message.append(f'to_date field\'s format is {regexObj["format"]}!')

    if not response_message:
        request_type = requestdata.get('request_type')
        if request_type == CHOICE.LEAVEREQUEST_TYPE[0][1]:

            if from_date and to_date:
                dates = []
                if bool(user) and bool(leavepolicy):
                    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
                    if leavesummary.exists():
                            response = ghelp().getWorkingDates(MODELS_SETT.Generalsettings, MODELS_LEAV.Holiday, user, leavepolicy, leavesummary.first(), from_date, to_date)
                            if response['message']: response_message.extend(response['message'])
                            else:
                                dates.extend(response['dates'])
                                if leavepolicy.max_consecutive_days == 0 or len(dates)<=leavepolicy.max_consecutive_days:
                                    total_left = leavesummary.first().total_left
                                    if len(dates)<=total_left:
                                        if leavepolicy.require_attachment:
                                            if not request.FILES.get('attachment'): response_message.append('attachment is required!')
                                    else: response_message.append(f'{user.first_name} {user.last_name} has left {total_left} leave - {leavepolicy.name}!')
                                else: response_message.append(f'max_consecutive_days {leavepolicy.max_consecutive_days} have been exceeded!')
                    else: response_message.append(f'{leavepolicy.name} is not associated to {user.first_name} {user.last_name}!')

                allowed_fields=['user', 'leavepolicy', 'from_date', 'to_date', 'attachment', 'description', 'reason']
                required_fields=['user', 'leavepolicy', 'from_date', 'to_date']
                choice_fields = [
                    {'name': 'request_type', 'values': [item[1] for item in CHOICE.LEAVEREQUEST_TYPE]},
                    {'name': 'status', 'values': [item[1] for item in CHOICE.STATUS]},
                ]
                fields_regex = [
                    {'field': 'from_date', 'type': 'date'},
                    {'field': 'to_date', 'type': 'date'}
                ]
                extra_fields={'request_type': CHOICE.LEAVEREQUEST_TYPE[0][1], 'status': CHOICE.STATUS[0][1], 'total_leave': len(dates), 'valid_leave_dates': dates}
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                    classOBJ=MODELS_LEAV.Leaverequest,
                    Serializer=PSRLZER_LEAV.Leaverequestserializer,
                    data=requestdata,
                    allowed_fields=allowed_fields,
                    required_fields=required_fields,
                    choice_fields=choice_fields,
                    fields_regex=fields_regex,
                    extra_fields=extra_fields
                )
                if responsesuccessflag == 'success':
                    response_data = responsedata.data
                    response_successflag = responsesuccessflag
                    response_status = responsestatus
                elif responsesuccessflag == 'error': response_message.extend(responsemessage)
            else: response_message.append('both from_date and to_date are required!')
        elif request_type == CHOICE.LEAVEREQUEST_TYPE[1][1]:
            assignedleavepolicys = [leavepolicyassign.leavepolicy for leavepolicyassign in MODELS_LEAV.Leavepolicyassign.objects.filter(user=user)]
            leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
            if leavesummary.exists():
                exchange_with = requestdata.get('exchange_with')
                if exchange_with:
                    leavepolicyids_str = [str(leavepolicy.id) for leavepolicy in assignedleavepolicys]
                    if exchange_with in leavepolicyids_str:
                        if from_date and to_date:
                            
                            response = ghelp().getWorkingDates(MODELS_SETT.Generalsettings, MODELS_LEAV.Holiday, user, leavepolicy, leavesummary.first(), from_date, to_date)
                            if response['message']: response_message.extend(response['message'])
                            else:
                                dates = response['dates']
                                allowed_fields=['user', 'leavepolicy', 'exchange_with', 'from_date', 'to_date', 'reason', 'attachment']
                                required_fields=['user', 'leavepolicy', 'request_type', 'from_date', 'to_date', 'status']
                                choice_fields = [
                                    {'name': 'request_type', 'values': [item[1] for item in CHOICE.LEAVEREQUEST_TYPE]},
                                    {'name': 'status', 'values': [item[1] for item in CHOICE.STATUS]},
                                ]
                                fields_regex = [
                                    {'field': 'from_date', 'type': 'date'},
                                    {'field': 'to_date', 'type': 'date'}
                                ]
                                extra_fields={'request_type': CHOICE.LEAVEREQUEST_TYPE[1][1], 'status': CHOICE.STATUS[0][1], 'total_leave': len(dates), 'valid_leave_dates': dates}
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                    classOBJ=MODELS_LEAV.Leaverequest,
                                    Serializer=PSRLZER_LEAV.Leaverequestserializer,
                                    data=requestdata,
                                    allowed_fields=allowed_fields,
                                    required_fields=required_fields,
                                    choice_fields=choice_fields,
                                    fields_regex=fields_regex,
                                    extra_fields=extra_fields
                                )
                                if responsesuccessflag == 'success':
                                    response_data = responsedata.data
                                    response_successflag = responsesuccessflag
                                    response_status = responsestatus
                                elif responsesuccessflag == 'error': response_message.extend(responsemessage)
                        else: response_message.append('both from_date and to_date are required!')
                    else: response_message.append(f'{leavepolicy.name} is not associated to {user.first_name} {user.last_name}!')
                else:
                    allowed_fields=['user', 'leavepolicy', 'extended_days', 'reason', 'attachment']
                    required_fields=['user', 'leavepolicy', 'extended_days', 'attachment', 'request_type', 'status']
                    choice_fields = [
                        {'name': 'request_type', 'values': [item[1] for item in CHOICE.LEAVEREQUEST_TYPE]},
                        {'name': 'status', 'values': [item[1] for item in CHOICE.STATUS]},
                    ]
                    extra_fields={'request_type': CHOICE.LEAVEREQUEST_TYPE[1][1], 'status': CHOICE.STATUS[0][1]}
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_LEAV.Leaverequest,
                        Serializer=PSRLZER_LEAV.Leaverequestserializer,
                        data=requestdata,
                        allowed_fields=allowed_fields,
                        required_fields=required_fields,
                        choice_fields=choice_fields,
                        extra_fields=extra_fields
                    )
                    if responsesuccessflag == 'success':
                        response_data = responsedata.data
                        response_successflag = responsesuccessflag
                        response_status = responsestatus
                    elif responsesuccessflag == 'error': response_message.extend(responsemessage)
            else: response_message.append(f'{leavepolicy.name} is not associated to {user.first_name} {user.last_name}!')
        elif request_type == CHOICE.LEAVEREQUEST_TYPE[2][1]:
            allowed_fields=['user', 'leavepolicy', 'from_date', 'to_date', 'attachment', 'description', 'reason']
            required_fields=['user', 'leavepolicy', 'request_type', 'from_date', 'to_date', 'status']
            choice_fields = [
                {'name': 'request_type', 'values': [item[1] for item in CHOICE.LEAVEREQUEST_TYPE]},
                {'name': 'status', 'values': [item[1] for item in CHOICE.STATUS]},
            ]
            fields_regex = [
                {'field': 'from_date', 'type': 'date'},
                {'field': 'to_date', 'type': 'date'}
            ]
            extra_fields={'request_type': CHOICE.LEAVEREQUEST_TYPE[2][1], 'status': CHOICE.STATUS[0][1], 'total_leave': len(dates), 'valid_leave_dates': dates}
            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                classOBJ=MODELS_LEAV.Leaverequest,
                Serializer=PSRLZER_LEAV.Leaverequestserializer,
                data=requestdata,
                allowed_fields=allowed_fields,
                required_fields=required_fields,
                choice_fields=choice_fields,
                fields_regex=fields_regex,
                extra_fields=extra_fields
            )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


    # user = None
    # userid = request.data.get('user')
    # if userid:
    #     if isinstance(userid, list):
    #         userid = userid[0]
    #         user = MODELS_USER.User.objects.get(id=userid)
    #     else: user = MODELS_USER.User.objects.get(id=userid)
    # if user == None: return Response({'data': {}, 'message': ['please provide an user!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    # leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': request.data.get('leavepolicy')})

    # from_date = request.data.get('from_date')
    # try: from_date=ghelp().convert_STR_datetime_date(from_date)
    # except: return Response({'data': {}, 'message': ['from_date is not valid!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    # to_date = request.data.get('to_date')
    # try: to_date=ghelp().convert_STR_datetime_date(to_date)
    # except: return Response({'data': {}, 'message': ['to_date is not valid!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    # description = request.data.get('description')
    # attachment = request.FILES.get('attachment')

    # leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
    
    # if leavesummary.exists():
    #     response = ghelp().getWorkingDates(MODELS_SETT.Generalsettings, MODELS_LEAV.Holiday, user, leavepolicy, leavesummary.first(), from_date, to_date)
    #     if response['message']: return Response({'data': {}, 'message': response['message'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    #     dates = response['dates']
        
    #     if leavepolicy.max_consecutive_days == 0 or len(dates)<=leavepolicy.max_consecutive_days:
    #         total_left = leavesummary.first().total_left
    #         if len(dates)<=total_left:

    #             if leavepolicy.require_attachment:
    #                 if not attachment: return Response({'data': {}, 'message': ['attachment is required!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                
    #             if len(dates)>0:
    #                 leaverequest=MODELS_LEAV.Leaverequest()
    #                 leaverequest.user=user
    #                 leaverequest.leavepolicy=leavepolicy
    #                 leaverequest.request_type=CHOICE.LEAVEREQUEST_TYPE[0][1]
    #                 leaverequest.from_date=from_date
    #                 leaverequest.to_date=to_date
    #                 leaverequest.total_leave=len(dates)
    #                 leaverequest.valid_leave_dates=dates
    #                 if attachment: leaverequest.attachment=attachment
    #                 if description: leaverequest.description=description
    #                 leaverequest.status=CHOICE.STATUS[0][1]
    #                 leaverequest.save()
    #                 return Response({'data': {}, 'message': dates, 'status': 'success'}, status=status.HTTP_200_OK)
                
    #             else: return Response({'data': {}, 'message': ['all the day\'s are weekly holiday!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    #         else: return Response({'data': {}, 'message': [f'you have left {total_left} leave - {leavepolicy.name}!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    #     else: return Response({'data': {}, 'message': [f'max_consecutive_days {leavepolicy.max_consecutive_days} have been exceeded!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    # else: return Response({'data': {}, 'message': [f'you are not permitted to have {leavepolicy.name} leave!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def approveleaverequest(request, leaverequestid=None):
    if leaverequestid:
        leaverequest = MODELS_LEAV.Leaverequest.objects.filter(id=leaverequestid)
        if leaverequest.exists():
            if leaverequest.first().status != CHOICE.STATUS[1][1]:
                leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                if leavesummary.exists():
                    copydates = leaverequest.first().valid_leave_dates.copy()
                    copydates.sort()
                    if leavesummary.first().total_left >= len(copydates):

                        if leaverequest.first().status == CHOICE.STATUS[2][1]:
                            firstdate = copydates[0]
                            todaydate = ghelp().getToday()
                            if todaydate>=firstdate:
                                return Response({'data': {}, 'message': ['too late to appreved as it is rejected!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                        for date in copydates:
                            leaveallocation = MODELS_LEAV.Approvedleave.objects.filter(
                                leavepolicy=leaverequest.first().leavepolicy,
                                user=leaverequest.first().user,
                                date=date
                            )
                            if leaveallocation.exists(): return Response({'data': {}, 'message': [f'{date} date is already exist in leaveallocation!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                        
                        for date in copydates:
                            MODELS_LEAV.Approvedleave.objects.create(
                                leavepolicy=leaverequest.first().leavepolicy,
                                user=leaverequest.first().user,
                                date=date,
                                approved_by=MODELS_USER.User.objects.get(id=request.user.id)
                            )

                        leaverequest.update(status=CHOICE.STATUS[1][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))

                        total_consumed = leavesummary.first().total_consumed + len(leaverequest.first().valid_leave_dates)
                        total_left = leavesummary.first().total_allocation - total_consumed
                        leavesummary.update(total_consumed=total_consumed, total_left=total_left)
                        return Response({'data': {}, 'message': [copydates], 'status': 'success'}, status=status.HTTP_200_OK)
                    else: return Response({'data': {}, 'message': [f'you have left {leavesummary.first().total_left} leave - {leavesummary.first().leavepolicy.name}!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                else: return Response({'data': {}, 'message': ['leavesummary doesn\'t exist!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            else:return Response({'data': {}, 'message': ['already approved!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'data': {}, 'message': ['leaverequest doesn\'t exist!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': ['provide a leaverequest id!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def rejectleaverequest(request, leaverequestid=None):
    if leaverequestid:
        leaverequest = MODELS_LEAV.Leaverequest.objects.filter(id=leaverequestid)
        if leaverequest.exists():
            if leaverequest.first().status != CHOICE.STATUS[2][1]:
                if leaverequest.first().status == CHOICE.STATUS[1][1]:
                    copydates = leaverequest.first().valid_leave_dates.copy()
                    copydates.sort()

                    firstdate = copydates[0]
                    todaydate = ghelp().getToday()
                    if todaydate>=firstdate:
                        return Response({'data': {}, 'message': ['too late to rejected!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                    for date in copydates:
                        leaveallocation = MODELS_LEAV.Approvedleave.objects.filter(
                            leavepolicy=leaverequest.first().leavepolicy,
                            user=leaverequest.first().user,
                            date=date
                        )
                        if leaveallocation.exists: leaveallocation.delete()

                    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                    if leavesummary.exists():
                        total_consumed = leavesummary.first().total_consumed-len(copydates)
                        total_left = leavesummary.first().total_left+len(copydates)
                        leavesummary.update(
                            total_consumed=total_consumed,
                            total_left=total_left
                        )
                leaverequest.update(status=CHOICE.STATUS[2][1])
                return Response({'data': {}, 'message': ['leave request rejected!'], 'status': 'success'}, status=status.HTTP_200_OK)
            else: return Response({'data': {}, 'message': ['already rejected!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'data': {}, 'message': ['leaverequest doesn\'t exist!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': ['provide a leaverequest id!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def getleaveallocationrequest(request):
#     filter_fields = [
#         {'name': 'id', 'convert': None, 'replace':'id'},
#         {'name': 'user', 'convert': None, 'replace':'user'},
#         {'name': 'leavepolicy', 'convert': None, 'replace':'leavepolicy'},
#         {'name': 'no_of_days', 'convert': None, 'replace':'no_of_days'},
#         {'name': 'reason', 'convert': None, 'replace':'reason__icontains'},
#         {'name': 'status', 'convert': None, 'replace':'status__icontains'},
#         {'name': 'approved_by', 'convert': None, 'replace':'approved_by'}
#     ]
#     leaveallocationrequests = MODELS_LEAV.Leaveallocationrequest.objects.filter(**ghelp().KWARGS(request, filter_fields))
#     column_accessor = request.GET.get('column_accessor')
#     if column_accessor: leaveallocationrequests = leaveallocationrequests.order_by(column_accessor)

#     total_count = leaveallocationrequests.count()
#     page = int(request.GET.get('page')) if request.GET.get('page') else 1
#     page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
#     if page and page_size: leaveallocationrequests = leaveallocationrequests[(page-1)*page_size:page*page_size]

#     leaveallocationrequestserializers=SRLZER_LEAV.Leaveallocationrequestserializer(leaveallocationrequests, many=True)
#     return Response({'data': {
#         'count': total_count,
#         'page': page,
#         'page_size': page_size,
#         'result': leaveallocationrequestserializers.data
#     }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def addleaveallocationrequest(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': request.data.get('leavepolicy')})
    if leavepolicy:
        userid = request.data.get('user')
        if userid:
            user = ghelp().getobject(MODELS_USER.User, {'id': userid})
            if user:
                reason = request.data.get('reason')
                attachment = request.FILES.get('attachment')
                exchange_with = request.data.get('exchange_with')

                extended_days = request.data.get('extended_days')
                if extended_days:
                    if extended_days.isnumeric(): extended_days = int(extended_days)
                    else:
                        extended_days = None
                        response_message.append('extended_days should be integer!')
                else:
                    extended_days = None
                    response_message.append('extended_days is required!')
                
                leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
                if leavesummary.exists():
                    if bool(exchange_with):
                        from_date = request.data.get('from_date')
                        try: from_date=ghelp().convert_STR_datetime_date(from_date)
                        except: response_message.append('from_date is not valid!')
                        to_date = request.data.get('to_date')
                        try: to_date=ghelp().convert_STR_datetime_date(to_date)
                        except: response_message.append('to_date is not valid!')

                        response = ghelp().getWorkingDates(MODELS_SETT.Generalsettings, MODELS_LEAV.Holiday, user, leavepolicy, leavesummary.first(), from_date, to_date)
                        if response['message']: return Response({'data': {}, 'message': response['message'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                        dates = response['dates']
                        
                        # if extended_days:
                        #     if extended_days>0:
                        #         leaverequestinstance = MODELS_LEAV.Leaverequest()
                        #         leaverequestinstance.user=user
                        #         leaverequestinstance.leavepolicy=leavepolicy
                        #         leaverequestinstance.request_type=CHOICE.LEAVEREQUEST_TYPE[1][1]
                        #         leaverequestinstance.extended_days=extended_days
                        #         if reason: leaverequestinstance.reason=reason
                        #         if attachment: leaverequestinstance.attachment=attachment
                        #         leaverequestinstance.status=CHOICE.STATUS[0][1]
                        #         try:
                        #             leaverequestinstance.save()
                        #             response_successflag = 'success'
                        #             response_status = status.HTTP_200_OK
                        #         except: response_message.append('something went wrong!')
                        #     else: response_message.append('extended_days should be a positive value!')
                        # else: response_message.append('extended_days is required!')
                    else:
                        if extended_days:
                            if extended_days>0:
                                leaverequestinstance = MODELS_LEAV.Leaverequest()
                                leaverequestinstance.user=user
                                leaverequestinstance.leavepolicy=leavepolicy
                                leaverequestinstance.request_type=CHOICE.LEAVEREQUEST_TYPE[1][1]
                                leaverequestinstance.extended_days=extended_days
                                if reason: leaverequestinstance.reason=reason
                                if attachment: leaverequestinstance.attachment=attachment
                                leaverequestinstance.status=CHOICE.STATUS[0][1]
                                try:
                                    leaverequestinstance.save()
                                    response_successflag = 'success'
                                    response_status = status.HTTP_200_OK
                                except: response_message.append('something went wrong!')
                            else: response_message.append('extended_days should be a positive value!')
                        else: response_message.append('extended_days is required!')
                else:

                    leaverequestinstance = MODELS_LEAV.Leaverequest()
                    leaverequestinstance.user=user
                    leaverequestinstance.leavepolicy=leavepolicy
                    leaverequestinstance.request_type=CHOICE.LEAVEREQUEST_TYPE[2][1]
                    # leaverequestinstance.no_of_days=no_of_days
                    if reason: leaverequestinstance.reason=reason
                    if attachment: leaverequestinstance.attachment=attachment
                    leaverequestinstance.status=CHOICE.STATUS[0][1]
                    try:
                        leaverequestinstance.save()
                        response_successflag = 'success'
                        response_status = status.HTTP_200_OK
                    except: response_message.append('something went wrong!')
                    # response_message.append('leavesummary doesn\'t exist!')
            else: response_message.append('please enter a valid user id(integer value)')
        else: response_message.append('user id is required!')
    else: response_message.append('leavepolicy doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def addleaveallocationrequest(request):
#     response_data = {}
#     response_message = []
#     response_successflag = 'error'
#     response_status = status.HTTP_400_BAD_REQUEST

#     leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': request.data.get('leavepolicy')})
#     if leavepolicy:
#         userid = request.data.get('user')
#         if userid:
#             user = ghelp().getobject(MODELS_USER.User, {'id': userid})
#             if user:
#                 reason = request.data.get('reason')
#                 attachment = request.FILES.get('attachment')
                
#                 no_of_days = request.data.get('no_of_days')
#                 if no_of_days:
#                     if no_of_days.isnumeric(): no_of_days = int(no_of_days)
#                     else:
#                         no_of_days = None
#                         response_message.append('no_of_days should be integer!')
#                 else:
#                     no_of_days = None
#                     response_message.append('no_of_days is required!')
                
#                 leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
#                 if leavesummary.exists():
#                     if no_of_days:
#                         if no_of_days>0:
#                             leaveallocationrequestinstance = MODELS_LEAV.Leaveallocationrequest()
#                             leaveallocationrequestinstance.user=user
#                             leaveallocationrequestinstance.leavepolicy=leavepolicy
#                             leaveallocationrequestinstance.no_of_days=no_of_days
#                             if reason: leaveallocationrequestinstance.reason=reason
#                             if attachment: leaveallocationrequestinstance.attachment=attachment
#                             leaveallocationrequestinstance.status=CHOICE.STATUS[0][1]
#                             try:
#                                 leaveallocationrequestinstance.save()
#                                 response_successflag = 'success'
#                                 response_status = status.HTTP_200_OK
#                             except: response_message.append('something went wrong!')
#                         else: response_message.append('no_of_days should be a positive value!')
#                     else: response_message.append('no_of_days is required!')
#                 else:
#                     leaveallocationrequestinstance = MODELS_LEAV.Leaveallocationrequest()
#                     leaveallocationrequestinstance.user=user
#                     leaveallocationrequestinstance.leavepolicy=leavepolicy
#                     # leaveallocationrequestinstance.no_of_days=no_of_days
#                     if reason: leaveallocationrequestinstance.reason=reason
#                     if attachment: leaveallocationrequestinstance.attachment=attachment
#                     leaveallocationrequestinstance.status=CHOICE.STATUS[0][1]
#                     try:
#                         leaveallocationrequestinstance.save()
#                         response_successflag = 'success'
#                         response_status = status.HTTP_200_OK
#                     except: response_message.append('something went wrong!')
#                     # response_message.append('leavesummary doesn\'t exist!')
#             else: response_message.append('please enter a valid user id(integer value)')
#         else: response_message.append('user id is required!')
#     else: response_message.append('leavepolicy doesn\'t exist!')
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def approverequestleaveallocation(request, leaveallocationrequestid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    if leaveallocationrequestid:
        leaveallocationrequest = ghelp().getobject(MODELS_LEAV.Leaveallocationrequest, {'id': leaveallocationrequestid}, True)
        if leaveallocationrequest:
            approved_by = MODELS_USER.User.objects.get(id=request.user.id)
            leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaveallocationrequest.first().user, leavepolicy=leaveallocationrequest.first().leavepolicy)
            if leavesummary.exists():
                total_allocation = leavesummary.first().total_allocation + leaveallocationrequest.first().no_of_days
                total_left = leavesummary.first().total_left + leaveallocationrequest.first().no_of_days
                leavesummary.update(total_allocation=total_allocation, total_left=total_left)
                leaveallocationrequest.update(status=CHOICE.STATUS[1][1], approved_by=approved_by)
                response_successflag = 'success'
                response_status = status.HTTP_200_OK
            else:
                generalsettings = MODELS_SETT.Generalsettings.objects.all().order_by('id')
                if generalsettings.exists():
                    MODELS_LEAV.Leavepolicyassign.objects.create(
                        user=leaveallocationrequest.first().user,
                        leavepolicy=leaveallocationrequest.first().leavepolicy,
                        created_by=leaveallocationrequest.first().approved_by,
                        updated_by=approved_by
                    )
                    MODELS_LEAV.Leavesummary.objects.create(
                        user=leaveallocationrequest.first().user,
                        leavepolicy=leaveallocationrequest.first().leavepolicy,
                        fiscal_year=generalsettings.first().fiscalyear,
                        total_allocation=leaveallocationrequest.first().leavepolicy.allocation_days,
                        total_consumed=0,
                        total_left=leaveallocationrequest.first().leavepolicy.allocation_days
                    )
                    leaveallocationrequest.update(status=CHOICE.STATUS[1][1], approved_by=approved_by)
                    response_successflag = 'success'
                    response_status = status.HTTP_200_OK
                else: response_message.append('please fillup general settings first!')
        else: response_message.append('leaveallocationrequest doesn\'t exist!')
    else: response_message.append('provide a leaveallocationrequest id!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getholidays(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'},
        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
        {'name': 'date', 'convert': None, 'replace':'date'},
        {'name': 'is_recuring', 'convert': "bool", 'replace':'is_recuring'},
        {'name': 'employee_grade', 'convert': None, 'replace':'employee_grade'}
    ]
    holidays = MODELS_LEAV.Holiday.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: holidays = holidays.order_by(column_accessor)

    total_count = holidays.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: holidays = holidays[(page-1)*page_size:page*page_size]

    holidayserializers = SRLZER_LEAV.Holidayserializer(holidays, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': holidayserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addholiday(request):
    userid = request.user.id
    extra_fields = {}
    unique_fields = []
    if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields = ['title', 'date']
    fields_regex = [
        {'field': 'date', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_LEAV.Holiday, 
        Serializer=PSRLZER_LEAV.Holidayserializer, 
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
def updateholiday(request, holidayid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    fields_regex = [
        {'field': 'date', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_LEAV.Holiday,
        Serializer=PSRLZER_LEAV.Holidayserializer,
        id=holidayid,
        data=request.data,
        extra_fields=extra_fields,
        fields_regex=fields_regex
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteholiday(request, holidayid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_LEAV.Holiday,
        id=holidayid
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)