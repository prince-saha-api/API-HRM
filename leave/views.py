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
    if 'exclude_user' in request.GET:
        kwargs = ghelp().KWARGS(request, [{'name': 'exclude_user', 'convert': None, 'replace':'leavepolicyassign__user__id'}])
        leavepolicys = MODELS_LEAV.Leavepolicy.objects.exclude(**kwargs)
    else:
        kwargs = ghelp().KWARGS(request, filter_fields)
        leavepolicys = MODELS_LEAV.Leavepolicy.objects.filter(**kwargs)

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
        {'model': MODELS_LEAV.Leaverequest, 'fields': [{'field': 'leavepolicy', 'relation': 'foreignkey', 'records': []}, {'field': 'exchange_with', 'relation': 'foreignkey', 'records': []}]},
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

    fiscalyear_response = ghelp().findFiscalyear(MODELS_SETT.Generalsettings)
    if fiscalyear_response['fiscalyear']:
        leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': request.data.get('leavepolicy')})
        if leavepolicy:
            user = ghelp().getobject(MODELS_USER.User, {'id': request.data.get('user')})
            if user:
                leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=user, leavepolicy=leavepolicy)
                if not leavepolicyassign.exists():
                    created_by = MODELS_USER.User.objects.get(id=request.user.id)
                    leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.create(user=user, leavepolicy=leavepolicy, created_by=created_by, updated_by=created_by)
                    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
                    if not leavesummary.exists():
                        MODELS_LEAV.Leavesummary.objects.create(
                            user=user,
                            leavepolicy=leavepolicy,
                            fiscal_year=fiscalyear_response['fiscalyear'],
                            total_allocation=leavepolicy.allocation_days,
                            total_consumed=0,
                            total_left=leavepolicy.allocation_days
                        )
                        response_successflag = 'success'
                        response_status = status.HTTP_202_ACCEPTED
                    else: response_message.append(f'{leavepolicy.name} leavepolicy\'s leavesummary is already exist!')
                else: response_message.append(f'{leavepolicy.name} is not associated to {user.first_name} {user.last_name}!')
            else: response_message.append('user doesn\'t exist!')
        else: response_message.append('leavepolicy doesn\'t exist!')
    else: response_message.extend(fiscalyear_response['message'])
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
        {'name': 'leavepolicy', 'convert': None, 'replace':'leavepolicy'},
        {'name': 'request_type', 'convert': None, 'replace':'request_type__icontains'},
        {'name': 'extended_days', 'convert': None, 'replace':'extended_days'},
        {'name': 'exchange_with', 'convert': None, 'replace':'exchange_with'},
        {'name': 'from_date', 'convert': None, 'replace':'from_date'},
        {'name': 'to_date', 'convert': None, 'replace':'to_date'},
        {'name': 'total_leave', 'convert': None, 'replace':'total_leave'},
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
    
    leavepolicyid = requestdata.get('leavepolicy')
    leavepolicy = None
    if leavepolicyid:
        leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, {'id': leavepolicyid})
        if leavepolicy == None: response_message.append('required valid leavepolicy!')
    else: response_message.append('required leavepolicy!')

    regexObj= ghelp().getregex('date')
    from_date = requestdata.get('from_date')
    to_date = requestdata.get('to_date')
    if from_date and to_date:
        try:
            from_date=ghelp().convert_STR_datetime_date(from_date)
            try:to_date=ghelp().convert_STR_datetime_date(to_date)
            except: response_message.append(f'to_date field\'s format is {regexObj["format"]}!')
        except: response_message.append(f'from_date field\'s format is {regexObj["format"]}!')

    if not response_message:
        assignedleavepolicys = [leavepolicyassign.leavepolicy for leavepolicyassign in MODELS_LEAV.Leavepolicyassign.objects.filter(user=user)]
        leavepolicyids_str = [str(leavepolicy.id) for leavepolicy in assignedleavepolicys]

        request_type = requestdata.get('request_type')
        if request_type == CHOICE.LEAVEREQUEST_TYPE[0][1]:
            if from_date and to_date:
                required_fields=['user', 'leavepolicy', 'from_date', 'to_date']
                dates = []
                leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
                if leavesummary.exists():
                        response = ghelp().getWorkingDates(MODELS_SETT.Generalsettings, MODELS_LEAV.Holiday, user, leavepolicy, leavesummary.first(), from_date, to_date)
                        if response['message']: response_message.extend(response['message'])
                        else:
                            dates.extend(response['dates'])
                            if leavepolicy.max_consecutive_days == 0 or len(dates)<=leavepolicy.max_consecutive_days:
                                total_left = leavesummary.first().total_left
                                if len(dates)<=total_left:
                                    if leavepolicy.require_attachment: required_fields.append('attachment')
                                else: response_message.append(f'{user.first_name} {user.last_name} has left {total_left} leave - {leavepolicy.name}!')
                            else: response_message.append(f'max_consecutive_days {leavepolicy.max_consecutive_days} have been exceeded!')
                else: response_message.append(f'{leavepolicy.name} is not associated to {user.first_name} {user.last_name}!')
                if not response_message:
                    allowed_fields=['user', 'leavepolicy', 'from_date', 'to_date', 'attachment', 'reason']
                    fields_regex = [{'field': 'from_date', 'type': 'date'},{'field': 'to_date', 'type': 'date'}]
                    extra_fields={'request_type': CHOICE.LEAVEREQUEST_TYPE[0][1], 'status': CHOICE.STATUS[0][1], 'total_leave': len(dates), 'valid_leave_dates': dates}
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_LEAV.Leaverequest,
                        Serializer=PSRLZER_LEAV.Leaverequestserializer,
                        data=requestdata,
                        allowed_fields=allowed_fields,
                        required_fields=required_fields,
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
            leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=user, leavepolicy=leavepolicy)
            if leavesummary.exists():
                exchange_with = requestdata.get('exchange_with')
                if exchange_with:
                    if exchange_with != leavepolicyid:
                        if exchange_with in leavepolicyids_str:
                            if from_date and to_date:
                                response = ghelp().getWorkingDates(MODELS_SETT.Generalsettings, MODELS_LEAV.Holiday, user, leavepolicy, leavesummary.first(), from_date, to_date)
                                if response['message']: response_message.extend(response['message'])
                                else:
                                    dates = response['dates']
                                    allowed_fields=['user', 'leavepolicy', 'exchange_with', 'from_date', 'to_date', 'reason', 'attachment']
                                    required_fields=['user', 'leavepolicy', 'exchange_with', 'from_date', 'to_date', 'attachment']
                                    fields_regex = [{'field': 'from_date', 'type': 'date'},{'field': 'to_date', 'type': 'date'}]
                                    extra_fields={'request_type': CHOICE.LEAVEREQUEST_TYPE[1][1], 'status': CHOICE.STATUS[0][1], 'total_leave': len(dates), 'valid_leave_dates': dates}
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                        classOBJ=MODELS_LEAV.Leaverequest,
                                        Serializer=PSRLZER_LEAV.Leaverequestserializer,
                                        data=requestdata,
                                        allowed_fields=allowed_fields,
                                        required_fields=required_fields,
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
                    else: response_message.append(f'both leavepolicys are same!')
                else:
                    allowed_fields=['user', 'leavepolicy', 'extended_days', 'reason', 'attachment']
                    required_fields=['user', 'leavepolicy', 'extended_days', 'attachment']
                    extra_fields={'request_type': CHOICE.LEAVEREQUEST_TYPE[1][1], 'status': CHOICE.STATUS[0][1]}
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_LEAV.Leaverequest,
                        Serializer=PSRLZER_LEAV.Leaverequestserializer,
                        data=requestdata,
                        allowed_fields=allowed_fields,
                        required_fields=required_fields,
                        extra_fields=extra_fields
                    )
                    if responsesuccessflag == 'success':
                        response_data = responsedata.data
                        response_successflag = responsesuccessflag
                        response_status = responsestatus
                    elif responsesuccessflag == 'error': response_message.extend(responsemessage)
            else: response_message.append(f'{leavepolicy.name} is not associated to {user.first_name} {user.last_name}!')
        elif request_type == CHOICE.LEAVEREQUEST_TYPE[2][1]:
            if leavepolicyid not in leavepolicyids_str:
                if from_date and to_date:
                    allowed_fields=['user', 'leavepolicy', 'from_date', 'to_date', 'attachment', 'reason']
                    required_fields=['user', 'leavepolicy', 'from_date', 'to_date', 'attachment']
                    fields_regex = [{'field': 'from_date', 'type': 'date'},{'field': 'to_date', 'type': 'date'}]
                    extra_fields={'request_type': CHOICE.LEAVEREQUEST_TYPE[2][1], 'status': CHOICE.STATUS[0][1]}
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_LEAV.Leaverequest,
                        Serializer=PSRLZER_LEAV.Leaverequestserializer,
                        data=requestdata,
                        allowed_fields=allowed_fields,
                        required_fields=required_fields,
                        fields_regex=fields_regex,
                        extra_fields=extra_fields
                    )
                    if responsesuccessflag == 'success':
                        response_data = responsedata.data
                        response_successflag = responsesuccessflag
                        response_status = responsestatus
                    elif responsesuccessflag == 'error': response_message.extend(responsemessage)
                else: response_message.append('both from_date and to_date are required!')
            else: response_message.append(f'{leavepolicy.name} is already assigned to {user.first_name} {user.last_name}!')
        else: response_message.append(f'request_type fields\'s allowed values are {", ".join([item[1] for item in CHOICE.LEAVEREQUEST_TYPE])}')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def approveleaverequest(request, leaverequestid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    leaverequest = MODELS_LEAV.Leaverequest.objects.filter(id=leaverequestid)
    if leaverequest.exists():
        if leaverequest.first().request_type == CHOICE.LEAVEREQUEST_TYPE[0][1]:
            if leaverequest.first().status != CHOICE.STATUS[1][1]:
                leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                if leavesummary.exists():
                    copydates = leaverequest.first().valid_leave_dates.copy()
                    copydates.sort()
                    if leavesummary.first().total_left >= len(copydates):
                        if leaverequest.first().status == CHOICE.STATUS[2][1]:
                            if ghelp().getToday()>=copydates[0]: response_message.append('too late to appreved as it is rejected!')
                        if not response_message:
                            for date in copydates:
                                leaveallocation = MODELS_LEAV.Approvedleave.objects.filter(
                                    leavepolicy=leaverequest.first().leavepolicy,
                                    user=leaverequest.first().user,
                                    date=date
                                )
                                if leaveallocation.exists(): response_message.append(f'{date} date is already exist in leaveallocation!')
                            if not response_message:
                                approved_dates = []
                                could_not_approved_dates = []
                                for date in copydates:
                                    try:
                                        MODELS_LEAV.Approvedleave.objects.create(
                                            leavepolicy=leaverequest.first().leavepolicy,
                                            user=leaverequest.first().user,
                                            date=date,
                                            approved_by=MODELS_USER.User.objects.get(id=request.user.id)
                                        )
                                        approved_dates.append(date)
                                    except: could_not_approved_dates.append(date)
                                if approved_dates:
                                    leaverequest.update(status=CHOICE.STATUS[1][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))

                                    total_consumed = leavesummary.first().total_consumed + len(approved_dates)
                                    total_left = leavesummary.first().total_allocation - total_consumed
                                    leavesummary.update(total_consumed=total_consumed, total_left=total_left)

                                    response_data.update({'approved_dates': approved_dates, 'could_not_approved_dates': could_not_approved_dates})
                                    response_successflag = 'success'
                                    response_status = status.HTTP_202_ACCEPTED
                    else: response_message.append(f'you have left {leavesummary.first().total_left} leave - {leavesummary.first().leavepolicy.name}!')
                else: response_message.append(f'{leaverequest.first().leavepolicy.name} is not associated to {leaverequest.first().user.first_name} {leaverequest.first().user.last_name}!')
            else: response_message.append('already approved!')
        elif leaverequest.first().request_type == CHOICE.LEAVEREQUEST_TYPE[1][1]:
            if leaverequest.first().status != CHOICE.STATUS[1][1]:
                if leaverequest.first().exchange_with:
                    leavesummary_target = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                    if leavesummary_target.exists():
                        leavesummary_exchange = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().exchange_with)
                        if leavesummary_exchange.exists():
                            if leavesummary_exchange.first().total_left >= leaverequest.first().total_leave:
                                total_allocation_exchange = leavesummary_exchange.first().total_allocation - leaverequest.first().total_leave
                                total_left_exchange = leavesummary_exchange.first().total_left - leaverequest.first().total_leave
                                try:
                                    leavesummary_exchange.update(total_allocation=total_allocation_exchange, total_left=total_left_exchange)
                                    total_allocation_target = leavesummary_target.first().total_allocation + leaverequest.first().total_leave
                                    total_left_target = leavesummary_target.first().total_left + leaverequest.first().total_leave
                                    try:
                                        leavesummary_target.update(total_allocation=total_allocation_target, total_left=total_left_target)
                                        leaverequest.update(status=CHOICE.STATUS[1][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))
                                        response_successflag = 'success'
                                        response_status = status.HTTP_202_ACCEPTED
                                    except:
                                        total_allocation_exchange += leaverequest.first().total_leave
                                        total_left_exchange += leaverequest.first().total_leave
                                        leavesummary_exchange.update(total_allocation=total_allocation_exchange, total_left=total_left_exchange)
                                        response_message.append(f'something went wrong for updating {leaverequest.first().leavepolicy.name} leavepolicy!')
                                except: response_message.append(f'something went wrong for updating {leaverequest.first().exchange_with.name} leavepolicy!')
                            else: response_message.append(f'{leaverequest.first().exchange_with.name} leavepolicy only left {leavesummary_exchange.first().total_left} days but request for {leaverequest.first().total_leave} days!')            
                        else: response_message.append(f'{leaverequest.first().exchange_with.name} is not associated to {leaverequest.first().user.first_name} {leaverequest.first().user.last_name}!')
                    else: response_message.append(f'{leaverequest.first().leavepolicy.name} is not associated to {leaverequest.first().user.first_name} {leaverequest.first().user.last_name}!')
                else:
                    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                    if leavesummary.exists():
                        total_allocation = leavesummary.first().total_allocation + leaverequest.first().extended_days
                        total_left = leavesummary.first().total_left + leaverequest.first().extended_days
                        try:
                            leavesummary.update(total_allocation=total_allocation, total_left=total_left)
                            leaverequest.update(status=CHOICE.STATUS[1][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))
                            response_successflag = 'success'
                            response_status = status.HTTP_202_ACCEPTED
                        except: response_message.append(f'something went wrong for updating {leaverequest.first().leavepolicy.name} leavepolicy!')
                    else: response_message.append(f'{leaverequest.first().leavepolicy.name} is not associated to {leaverequest.first().user.first_name} {leaverequest.first().user.last_name}!')
            else: response_message.append('already approved!')
        elif leaverequest.first().request_type == CHOICE.LEAVEREQUEST_TYPE[2][1]:
            if leaverequest.first().status != CHOICE.STATUS[1][1]:
                fiscalyear_response = ghelp().findFiscalyear(MODELS_SETT.Generalsettings)
                if fiscalyear_response['fiscalyear']:
                    if leaverequest.first().leavepolicy:
                        leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                        if not leavepolicyassign.exists():
                            created_by = MODELS_USER.User.objects.get(id=request.user.id)
                            try:
                                leavepolicyassign = MODELS_LEAV.Leavepolicyassign.objects.create(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy, created_by=created_by, updated_by=created_by)
                                leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                                if not leavesummary.exists():
                                    try:
                                        MODELS_LEAV.Leavesummary.objects.create(
                                            user=leaverequest.first().user,
                                            leavepolicy=leaverequest.first().leavepolicy,
                                            fiscal_year=fiscalyear_response['fiscalyear'],
                                            total_allocation=leaverequest.first().leavepolicy.allocation_days,
                                            total_consumed=0,
                                            total_left=leaverequest.first().leavepolicy.allocation_days
                                        )
                                        leaverequest.update(status=CHOICE.STATUS[1][1], approved_by=created_by)
                                        response_successflag = 'success'
                                        response_status = status.HTTP_202_ACCEPTED
                                    except:
                                        leavepolicyassign.delete()
                                        response_message.append(f'something went wrong for creating {leaverequest.first().leavepolicy.name} leavepolicy\'s leavesummary!')
                                else: response_message.append(f'{leaverequest.first().leavepolicy.name} leavepolicy\'s leavesummary is already exist!')
                            except: response_message.append(f'something went wrong for assigning {leaverequest.first().leavepolicy.name} leavepolicy!')
                        else:
                            leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                            if not leavesummary.exists():
                                try:
                                    MODELS_LEAV.Leavesummary.objects.create(
                                        user=leaverequest.first().user,
                                        leavepolicy=leaverequest.first().leavepolicy,
                                        fiscal_year=fiscalyear_response['fiscalyear'],
                                        total_allocation=leaverequest.first().leavepolicy.allocation_days,
                                        total_consumed=0,
                                        total_left=leaverequest.first().leavepolicy.allocation_days
                                    )
                                    leaverequest.update(status=CHOICE.STATUS[1][1], approved_by=created_by)
                                    response_successflag = 'success'
                                    response_status = status.HTTP_202_ACCEPTED
                                except:
                                    leavepolicyassign.delete()
                                    response_message.append(f'something went wrong for creating {leaverequest.first().leavepolicy.name} leavepolicy\'s leavesummary!')
                            else: response_message.append(f'{leaverequest.first().leavepolicy.name} leavepolicy\'s leavesummary is already exist!')
                    else: response_message.append('leavepolicy doesn\'t exist!')
                else: response_message.extend(fiscalyear_response['message'])
            else: response_message.append('already approved!')
        else: response_message.append('request_type doesn\'t match with LEAVEREQUEST_TYPE(Backend)!')
    else: response_message.append('leaverequest doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def rejectleaverequest(request, leaverequestid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    leaverequest = MODELS_LEAV.Leaverequest.objects.filter(id=leaverequestid)
    if leaverequest.exists():
        if leaverequest.first().request_type == CHOICE.LEAVEREQUEST_TYPE[0][1]:
            if leaverequest.first().status != CHOICE.STATUS[2][1]:
                if leaverequest.first().status == CHOICE.STATUS[1][1]:
                    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                    if leavesummary.exists():
                        copydates = leaverequest.first().valid_leave_dates.copy()
                        copydates.sort()

                        if ghelp().getToday()>=copydates[0]: response_message.append('too late to rejected!')
                        else:
                            delete_approvedleave = []
                            could_not_delete_approvedleave = []
                            could_not_found_approvedleave = []
                            for date in copydates:
                                approvedleave = MODELS_LEAV.Approvedleave.objects.filter(leavepolicy=leaverequest.first().leavepolicy, user=leaverequest.first().user, date=date)
                                if approvedleave.exists():
                                    try:
                                        approvedleave.delete()
                                        delete_approvedleave.append(date)
                                    except:
                                        could_not_delete_approvedleave.append(date)
                                        response_message.append(f'please take note(delete it manually) Model neme: {MODELS_LEAV.Approvedleave.__name__}, Leavepolicy name: {leaverequest.first().leavepolicy.name}, Username: {leaverequest.first().user.username}, Date: {date}')
                                else: could_not_found_approvedleave.append(date)
                            if delete_approvedleave:
                                total_consumed = leavesummary.first().total_consumed-len(copydates)
                                total_left = leavesummary.first().total_left+len(copydates)
                                leavesummary.update(total_consumed=total_consumed, total_left=total_left)
                                leaverequest.update(status=CHOICE.STATUS[0][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))
                                response_data.update({'delete_approvedleave': delete_approvedleave, 'could_not_delete_approvedleave': could_not_delete_approvedleave, 'could_not_found_approvedleave': could_not_found_approvedleave})
                                response_successflag = 'success'
                                response_status = status.HTTP_202_ACCEPTED
                    else: response_message.append(f'{leaverequest.first().leavepolicy.name} leavepolicy\'s leavesummary is missing!')
            else: response_message.append('already rejected!')
        elif leaverequest.first().request_type == CHOICE.LEAVEREQUEST_TYPE[1][1]:
            if leaverequest.first().status != CHOICE.STATUS[2][1]:
                if leaverequest.first().status == CHOICE.STATUS[1][1]:
                    if leaverequest.first().exchange_with:
                        leavesummary_target = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                        if leavesummary_target.exists():
                            if leavesummary_target.first().total_left>=leaverequest.first().total_leave:
                                leavesummary_exchange = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().exchange_with)
                                if leavesummary_exchange.exists():
                                    total_allocation_target = leavesummary_target.first().total_allocation - leaverequest.first().total_leave
                                    total_left_target = leavesummary_target.first().total_left - leaverequest.first().total_leave
                                    try:
                                        leavesummary_target.update(total_allocation=total_allocation_target, total_left=total_left_target)
                                        total_allocation_exchange = leavesummary_exchange.first().total_allocation + leaverequest.first().total_leave
                                        total_left_exchange = leavesummary_exchange.first().total_left + leaverequest.first().total_leave
                                        try:
                                            leavesummary_exchange.update(total_allocation=total_allocation_exchange, total_left=total_left_exchange)
                                            leaverequest.update(status=CHOICE.STATUS[0][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))
                                            response_successflag = 'success'
                                            response_status = status.HTTP_202_ACCEPTED
                                        except:
                                            total_allocation_target += leaverequest.first().total_leave
                                            total_left_target += leaverequest.first().total_leave
                                            leavesummary_target.update(total_allocation=total_allocation_target, total_left=total_left_target)
                                            response_message.append(f'something went wrong for updating {leaverequest.first().exchange_with.name} leavepolicy!')
                                    except: response_message.append(f'something went wrong for updating {leaverequest.first().leavepolicy.name} leavepolicy!')
                                else: response_message.append(f'{leaverequest.first().exchange_with.name} leavepolicy\'s leavesummary is missing(unusual activity)')
                            else: response_message.append(f'can\'t reject because {leaverequest.first().leavepolicy.name} leavepolicy only left {leavesummary_target.first().total_left} days but exchanged for {leaverequest.first().total_leave} days!')
                        else: response_message.append(f'{leaverequest.first().leavepolicy.name} leavepolicy\'s leavesummary is missing(unusual activity)')
                    else:
                        leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                        if leavesummary.exists():
                            if leavesummary.first().total_left>=leaverequest.first().extended_days:
                                total_allocation = leavesummary.first().total_allocation - leaverequest.first().extended_days
                                total_left = leavesummary.first().total_left - leaverequest.first().extended_days
                                try:
                                    leavesummary.update(total_allocation=total_allocation, total_left=total_left)
                                    leaverequest.update(status=CHOICE.STATUS[0][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))
                                    response_successflag = 'success'
                                    response_status = status.HTTP_202_ACCEPTED
                                except: response_message.append(f'something went wrong for updating {leaverequest.first().leavepolicy.name} leavepolicy!')
                            else: response_message.append(f'can\'t reject because {leaverequest.first().leavepolicy.name} leavepolicy only left {leavesummary_target.first().total_left} days but exchanged for {leaverequest.first().total_leave} days!')
                        else: response_message.append(f'{leaverequest.first().leavepolicy.name} leavepolicy\'s leavesummary is missing(unusual activity)')
            else: response_message.append('already rejected!')
        elif leaverequest.first().request_type == CHOICE.LEAVEREQUEST_TYPE[2][1]:
            if leaverequest.first().status != CHOICE.STATUS[2][1]:
                if leaverequest.first().status == CHOICE.STATUS[1][1]:
                    leavesummary = MODELS_LEAV.Leavesummary.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                    if leavesummary.exists():
                        if leavesummary.first().total_consumed == 0:
                            Leaverequest_delete = MODELS_LEAV.Leaverequest.objects.exclude(request_type=CHOICE.LEAVEREQUEST_TYPE[2][1]).filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                            if Leaverequest_delete.exists(): Leaverequest_delete.delete()
                            leavepolicyassign_delete = MODELS_LEAV.Leavepolicyassign.objects.filter(user=leaverequest.first().user, leavepolicy=leaverequest.first().leavepolicy)
                            if leavepolicyassign_delete.exists(): leavepolicyassign_delete.delete()
                            leavesummary.delete()
                            leaverequest.update(status=CHOICE.STATUS[0][1], approved_by=MODELS_USER.User.objects.get(id=request.user.id))
                            response_successflag = 'success'
                            response_status = status.HTTP_202_ACCEPTED
                        else: response_message.append(f'can\'t reject, already consumed {leaverequest.first().leavepolicy.name} leavepolicy({leavesummary.first().total_consumed})!')
                    else: response_message.append(f'{leaverequest.first().leavepolicy.name} leavepolicy\'s leavesummary is missing(unusual activity)')
            else: response_message.append('already rejected!')
        else: response_message.append('request_type doesn\'t match with LEAVEREQUEST_TYPE(Backend)!')
    else: response_message.append('leaverequest doesn\'t exist!')
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