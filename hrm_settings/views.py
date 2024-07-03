from hrm_settings.serializer.POST import serializers as PSRLZER_SETT
from rest_framework.decorators import api_view, permission_classes
from hrm_settings.serializer import serializers as SRLZER_SETT
from rest_framework.permissions import IsAuthenticated
from helps.common.generic import Generichelps as ghelp
from hrm_settings import models as MODELS_SETT
from rest_framework.response import Response
from helps.choice import common as CHOICE
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getweekdays(request):
    for day in [each[1] for each in CHOICE.DAYS]:
        if not MODELS_SETT.Weekdays.objects.filter(day=day).exists():
            MODELS_SETT.Weekdays.objects.create(day=day)
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'day', 'convert': None, 'replace':'day__icontains'}
                ]
    weekdays = MODELS_SETT.Weekdays.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: weekdays = weekdays.order_by(column_accessor)

    total_count = weekdays.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: weekdays = weekdays[(page-1)*page_size:page*page_size]

    weekdaysserializers = SRLZER_SETT.Weekdaysserializer(weekdays, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': weekdaysserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addweekdays(request):
#     # userid = request.user.id
#     unique_fields = ['day']
#     required_fields= ['day']
#     choice_fields = [{'name': 'day', 'values': [item[1] for item in CHOICE.DAYS]}]
#     response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
#         MODELS_SETT.Weekdays, 
#         SRLZER_SETT.Weekdaysserializer, 
#         request.data, 
#         unique_fields=unique_fields, 
#         required_fields=required_fields,
#         choice_fields=choice_fields
#         )
#     if response_data: response_data = response_data.data
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def updateweekdays(request, weekdaysid=None):
#     allowed_fields = ['name', 'grade']
#     choice_fields = [{'name': 'day', 'values': [item[1] for item in CHOICE.DAYS]}]
#     response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
#         MODELS_SETT.Weekdays, 
#         SRLZER_SETT.Weekdaysserializer, 
#         weekdaysid,
#         request.data,
#         allowed_fields=allowed_fields,
#         choice_fields=choice_fields
#         )
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def deleteweekdays(request, weekdaysid=None):
#     classOBJpackage_tocheck_assciaativity = [
#         {'model': MODELS_SETT.Weeklyholiday, 'fields': [{'field': 'day', 'relation': 'manytomanyfield', 'records': MODELS_SETT.Weekdays.objects.filter(id=weekdaysid).first().weeklyholiday_set.all()}]}
#     ]
#     response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
#         MODELS_SETT.Weekdays,
#         weekdaysid,
#         classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
#         )
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getgeneralsettings(request):
    generalsetting = MODELS_SETT.Generalsettings.objects.all().last()
    generalsettingsserializer = SRLZER_SETT.Generalsettingsserializer(generalsetting, many=False).data
    return Response(generalsettingsserializer, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addgeneralsettings(request):
    requesteddata = request.data.copy()
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST
    weekdaysinstance = []
    if 'weekly_holiday' in requesteddata:
        if isinstance(requesteddata['weekly_holiday'], list):
            weekly_holiday = []
            for value in requesteddata['weekly_holiday']:
                if value:
                    if isinstance(value, str):
                        if value.isnumeric(): weekly_holiday.append(int(value))
                    elif isinstance(value, int): weekly_holiday.append(value)
            weekdaysinstance = MODELS_SETT.Weekdays.objects.filter(id__in=weekly_holiday)

    if not response_message:
        weeklyholiday = MODELS_SETT.Weeklyholiday.objects.create()
        weeklyholiday.day.set(weekdaysinstance)

        requesteddata.update({'weekly_holiday': weeklyholiday.id})
        required_fields = ['fiscalyear_month', 'weekly_holiday', 'workingday_starts_at', 'consider_attendance_on_holidays']
        fields_regex = [
            {'field': 'workingday_starts_at', 'type': 'time'}
        ]
        choice_fields = [
            {'name': 'fiscalyear_month', 'values': [item[1] for item in CHOICE.MONTHS]},
            {'name': 'consider_attendance_on_holidays', 'values': [item[1] for item in CHOICE.ATTENDANCE_OVERTIME]},
        ]
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
            MODELS_SETT.Generalsettings, 
            PSRLZER_SETT.Generalsettingsserializer, 
            requesteddata, 
            required_fields=required_fields,
            fields_regex=fields_regex,
            choice_fields=choice_fields
        )
        if responsesuccessflag == 'success':
            response_data.update(responsedata.data)
            response_successflag = responsesuccessflag
            MODELS_SETT.Generalsettings.objects.exclude(id=responsedata.data['id']).delete()
            response_status = responsestatus
        elif responsesuccessflag == 'error':
            response_message.extend(responsemessage)
            if weeklyholiday: weeklyholiday.delete()
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def updategeneralsettings(request, generalsettingsid=None):
    requesteddata = request.data.copy()
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_201_CREATED
    
    generalsettings = MODELS_SETT.Generalsettings.objects.filter(id=generalsettingsid)
    if generalsettings.exists():

        update_weekly_holiday = False
        weekdaysinstance = []
        if 'weekly_holiday' in requesteddata:
            update_weekly_holiday = True
            if isinstance(requesteddata['weekly_holiday'], list):
                weekly_holiday = []
                for value in requesteddata['weekly_holiday']:
                    if value:
                        if isinstance(value, str):
                            if value.isnumeric(): weekly_holiday.append(int(value))
                        elif isinstance(value, int): weekly_holiday.append(value)
                weekdaysinstance = MODELS_SETT.Weekdays.objects.filter(id__in=weekly_holiday)

        if update_weekly_holiday:
            generalsettings.first().weekly_holiday.day.clear()
            generalsettings.first().weekly_holiday.day.set(weekdaysinstance)
            requesteddata.update({'weekly_holiday': generalsettings.first().weekly_holiday.id})
        fields_regex = [
            {'field': 'workingday_starts_at', 'type': 'time'}
        ]
        choice_fields = [
            {'name': 'fiscalyear_month', 'values': [item[1] for item in CHOICE.MONTHS]},
            {'name': 'consider_attendance_on_holidays', 'values': [item[1] for item in CHOICE.ATTENDANCE_OVERTIME]},
        ]
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
            MODELS_SETT.Generalsettings, 
            PSRLZER_SETT.Generalsettingsserializer, 
            generalsettingsid,
            requesteddata,
            choice_fields=choice_fields,
            fields_regex=fields_regex
        )
        if responsesuccessflag == 'success':
            response_data = responsedata
            response_successflag = responsesuccessflag
            response_status = responsestatus
        elif responsesuccessflag == 'error':
            response_message.extend(responsemessage)
    else: response_message.append('doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)