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
            is_created = False
            while not is_created:
                try:
                    MODELS_SETT.Weekdays.objects.create(day=day)
                    is_created = True
                except: pass
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getgeneralsettings(request):
    
    classOBJ = {
        'Weekdays': MODELS_SETT.Weekdays,
        'Weeklyholiday': MODELS_SETT.Weeklyholiday,
        'Fiscalyear': MODELS_SETT.Fiscalyear,
        'Generalsettings': MODELS_SETT.Generalsettings
    }
    Serializer = {
        'Fiscalyear': PSRLZER_SETT.Fiscalyearserializer,
        'Generalsettings': PSRLZER_SETT.Generalsettingsserializer
    }
    ghelp().addGenarelSettings(classOBJ, Serializer)

    generalsettingsserializer = {}
    resonse_status = status.HTTP_400_BAD_REQUEST
    generalsetting = ghelp().findGeneralsettings(MODELS_SETT.Generalsettings)
    if generalsetting:
        generalsettingsserializer.update(SRLZER_SETT.Generalsettingsserializer(generalsetting, many=False).data)
        resonse_status = status.HTTP_200_OK
    return Response(generalsettingsserializer, status=resonse_status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addgeneralsettings(request):
    requestdata = request.data.copy()
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    classOBJ = {
        'Weekdays': MODELS_SETT.Weekdays,
        'Weeklyholiday': MODELS_SETT.Weeklyholiday,
        'Fiscalyear': MODELS_SETT.Fiscalyear,
        'Generalsettings': MODELS_SETT.Generalsettings
    }
    Serializer = {
        'Fiscalyear': PSRLZER_SETT.Fiscalyearserializer,
        'Generalsettings': PSRLZER_SETT.Generalsettingsserializer
    }
    response = ghelp().addGenarelSettings(classOBJ, Serializer, requestdata)
    if not response['backend_message']:
        if response['flag']:
            response_data = response['data'].data
            response_successflag = 'success'
            response_status = status.HTTP_201_CREATED
        else: response_message.extend(response['message'])
    else: response_message.append('inform backend, data is missing in backend!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def updategeneralsettings(request, generalsettingsid=None):
    requestdata = request.data.copy()
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_201_CREATED
    
    generalsettings = MODELS_SETT.Generalsettings.objects.filter(id=generalsettingsid)
    if generalsettings.exists():

        update_weekly_holiday = False
        weekdaysinstance = []
        if 'weekly_holiday' in requestdata:
            update_weekly_holiday = True
            if isinstance(requestdata['weekly_holiday'], list):
                weekly_holiday = []
                for value in requestdata['weekly_holiday']:
                    if value:
                        if isinstance(value, str):
                            if value.isnumeric(): weekly_holiday.append(int(value))
                        elif isinstance(value, int): weekly_holiday.append(value)
                weekdaysinstance = MODELS_SETT.Weekdays.objects.filter(id__in=weekly_holiday)

        if 'fiscalyear_month' in requestdata:
            from_date, to_date = ghelp().getFiscalyearBoundary(requestdata['fiscalyear_month'], CHOICE.MONTHS_D)
            if from_date:
                fields_regex = [
                    {'field': 'from_date', 'type': 'date'},
                    {'field': 'to_date', 'type': 'date'}
                ]
                choice_fields = [
                    {'name': 'from_month', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MONTHS]},
                    {'name': 'to_month', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MONTHS]},
                ]
                from_datesplit = [int(each) for each in f'{from_date}'.split('-')]
                to_datesplit = [int(each) for each in f'{to_date}'.split('-')]
                fiscalyeardata = {
                    'from_month': CHOICE.MONTHS_DR[f'{from_datesplit[1]}'],
                    'from_year': from_datesplit[0],
                    'to_month': CHOICE.MONTHS_DR[f'{to_datesplit[1]}'],
                    'to_year': to_datesplit[0],
                    'from_date': f'{from_date}',
                    'to_date': f'{to_date}'
                }
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                    classOBJ=MODELS_SETT.Fiscalyear, 
                    Serializer=PSRLZER_SETT.Fiscalyearserializer, 
                    id=generalsettings.first().fiscalyear.id,
                    data=fiscalyeardata,
                    choice_fields=choice_fields,
                    fields_regex=fields_regex
                )
        if update_weekly_holiday:
            generalsettings.first().weekly_holiday.day.clear()
            generalsettings.first().weekly_holiday.day.set(weekdaysinstance)
            requestdata.update({'weekly_holiday': generalsettings.first().weekly_holiday.id})
            
        fields_regex = [{'field': 'workingday_starts_at', 'type': 'time'}]
        choice_fields = [
            {'name': 'fiscalyear_month', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MONTHS]},
            {'name': 'consider_attendance_on_holidays', 'type': 'single-string', 'values': [item[1] for item in CHOICE.ATTENDANCE_OVERTIME]},
        ]
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
            classOBJ=MODELS_SETT.Generalsettings, 
            Serializer=PSRLZER_SETT.Generalsettingsserializer, 
            id=generalsettingsid,
            data=requestdata,
            choice_fields=choice_fields,
            fields_regex=fields_regex
        )
        if responsesuccessflag == 'success':
            response_data = SRLZER_SETT.Generalsettingsserializer(MODELS_SETT.Generalsettings.objects.get(id=generalsettingsid), many=False).data
            response_successflag = responsesuccessflag
            response_status = responsestatus
        elif responsesuccessflag == 'error':
            response_message.extend(responsemessage)
    else: response_message.append('doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)