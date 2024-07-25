# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from jobrecord import models as MODELS_JOBR
from jobrecord.serializer import serializers as SRLZER_JOBR
from jobrecord.serializer.POST import serializers as PSRLZER_JOBR
from rest_framework.response import Response
from rest_framework import status
from helps.common.generic import Generichelps as ghelp
from helps.choice import common as CHOICE


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getjobhistorys(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'effective_from', 'convert': None, 'replace':'effective_from'},
        {'name': 'increment_on', 'convert': None, 'replace':'increment_on__icontains'},
        {'name': 'prev_salary', 'convert': None, 'replace':'prev_salary'},
        {'name': 'new_salary', 'convert': None, 'replace':'new_salary'},
        {'name': 'increment_amount', 'convert': None, 'replace':'increment_amount'},
        {'name': 'percentage', 'convert': None, 'replace':'percentage'},
        {'name': 'prev_company', 'convert': None, 'replace':'prev_company'},
        {'name': 'prev_branch', 'convert': None, 'replace':'prev_branch'},
        {'name': 'prev_department', 'convert': None, 'replace':'prev_department'},
        {'name': 'prev_designation', 'convert': None, 'replace':'prev_designation'},
        {'name': 'prev_employee_type', 'convert': None, 'replace':'prev_employee_type'},
        {'name': 'from_date', 'convert': None, 'replace':'from_date'},
        {'name': 'to_date', 'convert': None, 'replace':'to_date'},
        {'name': 'status_adjustment', 'convert': None, 'replace':'status_adjustment__icontains'},
        {'name': 'appraisal_by', 'convert': None, 'replace':'appraisal_by'},
        {'name': 'comment', 'convert': None, 'replace':'comment__icontains'}
    ]
    employeejobhistorys = MODELS_JOBR.Employeejobhistory.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: employeejobhistorys = employeejobhistorys.order_by(column_accessor)

    total_count = employeejobhistorys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: employeejobhistorys = employeejobhistorys[(page-1)*page_size:page*page_size]

    employeejobhistoryserializers = SRLZER_JOBR.Employeejobhistoryserializer(employeejobhistorys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': employeejobhistoryserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addjobhistory(request):
    # userid = request.user.id
    required_fields = ['user', 'effective_from']
    choice_fields = [
        {'name': 'increment_on', 'values': [item[1] for item in CHOICE.INCREMENT_ON]},
        {'name': 'status_adjustment', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]},
    ]
    fields_regex = [
        {'field': 'effective_from', 'type': 'date'},
        {'field': 'from_date', 'type': 'date'},
        {'field': 'to_date', 'type': 'date'},
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_JOBR.Employeejobhistory,
        Serializer=PSRLZER_JOBR.Employeejobhistoryserializer,
        data=request.data,
        required_fields=required_fields,
        choice_fields=choice_fields,
        fields_regex=fields_regex
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatejobhistory(request, jobhistoryid=None):
    choice_fields = [
        {'name': 'increment_on', 'values': [item[1] for item in CHOICE.INCREMENT_ON]},
        {'name': 'status_adjustment', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]},
    ]
    fields_regex = [
        {'field': 'effective_from', 'type': 'date'},
        {'field': 'from_date', 'type': 'date'},
        {'field': 'to_date', 'type': 'date'},
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_JOBR.Employeejobhistory,
        Serializer=PSRLZER_JOBR.Employeejobhistoryserializer,
        id=jobhistoryid,
        data=request.data,
        choice_fields=choice_fields,
        fields_regex=fields_regex
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletejobhistory(request, jobhistoryid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_JOBR.Employeejobhistory,
        id=jobhistoryid
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)