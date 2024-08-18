from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from payroll import models as MODELS_PAYR
from payroll.serializer import serializers as SRLZER_PAYR
from payroll.serializer.POST import serializers as PSRLZER_PAYR
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from helps.choice import common as CHOICE
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getpayrollearnings(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'},
        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
        {'name': 'is_taxable', 'convert': 'bool', 'replace':'is_taxable'},
        {'name': 'depends_on_attendance', 'convert': 'bool', 'replace':'depends_on_attendance'},
        {'name': 'amount_type', 'convert': None, 'replace':'amount_type__icontains'},
        {'name': 'amount', 'convert': None, 'replace':'amount'},
        {'name': 'updated_by', 'convert': None, 'replace':'updated_by'},
        {'name': 'created_by', 'convert': None, 'replace':'created_by'}
    ]
    payrollearnings = MODELS_PAYR.Payrollearning.objects.filter(**ghelp().KWARGS(request, filter_fields))

    column_accessor = request.GET.get('column_accessor')
    if column_accessor: payrollearnings = payrollearnings.order_by(column_accessor)
    
    total_count = payrollearnings.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: payrollearnings=payrollearnings[(page-1)*page_size:page*page_size]

    payrollearningserializers = SRLZER_PAYR.Payrollearningserializer(payrollearnings, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': payrollearningserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addpayrollearning(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    choice_fields = [
        {'name': 'day', 'values': [item[1] for item in CHOICE.AMOUNT_TYPE]}
    ]
    required_fields = ['title', 'amount']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_PAYR.Payrollearning, 
        Serializer=PSRLZER_PAYR.Payrollearningserializer, 
        data=request.data, 
        unique_fields=[], 
        extra_fields=extra_fields, 
        choice_fields=choice_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatepayrollearning(request, payrollearningid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_PAYR.Payrollearning,
        Serializer=PSRLZER_PAYR.Payrollearningserializer,
        id=payrollearningid,
        data=request.data,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getpayrolldeductions(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'},
        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
        {'name': 'exempted_for_tax', 'convert': 'bool', 'replace':'exempted_for_tax'},
        {'name': 'depends_on_attendance', 'convert': 'bool', 'replace':'depends_on_attendance'},
        {'name': 'amount_type', 'convert': None, 'replace':'amount_type__icontains'},
        {'name': 'amount', 'convert': None, 'replace':'amount'}
    ]
    payrolldeductions = MODELS_PAYR.Payrolldeduction.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: payrolldeductions = payrolldeductions.order_by(column_accessor)

    total_count = payrolldeductions.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: payrolldeductions = payrolldeductions[(page-1)*page_size:page*page_size]

    payrolldeductionserializers = SRLZER_PAYR.Payrolldeductionserializer(payrolldeductions, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': payrolldeductionserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addpayrolldeduction(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    choice_fields = [
        {'name': 'day', 'values': [item[1] for item in CHOICE.AMOUNT_TYPE]}
    ]
    required_fields = ['title', 'amount']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_PAYR.Payrolldeduction, 
        Serializer=PSRLZER_PAYR.Payrolldeductionserializer, 
        data=request.data, 
        extra_fields=extra_fields, 
        choice_fields=choice_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatepayrolldeduction(request, payrolldeductionid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_PAYR.Payrolldeduction,
        Serializer=PSRLZER_PAYR.Payrolldeductionserializer,
        id=payrolldeductionid,
        data=request.data,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getpayrolltaxs(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'},
        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
        {'name': 'min_income', 'convert': None, 'replace':'min_income'},
        {'name': 'max_income', 'convert': None, 'replace':'max_income'},
        {'name': 'ethnicgroup', 'convert': None, 'replace':'ethnicgroup'},
        {'name': 'percentage', 'convert': None, 'replace':'percentage'},
        {'name': 'updated_by', 'convert': None, 'replace':'updated_by'},
        {'name': 'created_by', 'convert': None, 'replace':'created_by'}
    ]
    payrolltaxs = MODELS_PAYR.Payrolltax.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: payrolltaxs = payrolltaxs.order_by(column_accessor)
    payrolltaxserializers = SRLZER_PAYR.Payrolltaxserializer(payrolltaxs, many=True)
    return Response({'status': 'success', 'message': '', 'data': payrolltaxserializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addpayrolltax(request):
    userid = request.user.id
    extra_fields = {}
    unique_fields = ['title']
    required_fields = ['title', 'min_income', 'max_income', 'percentage']
    if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_PAYR.Payrolltax, 
        Serializer=PSRLZER_PAYR.Payrolltaxserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        extra_fields=extra_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatepayrolltax(request, payrolltaxid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    unique_fields=['title']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_PAYR.Payrolltax,
        Serializer=PSRLZER_PAYR.Payrolltaxserializer,
        id=payrolltaxid,
        data=request.data,
        unique_fields=unique_fields,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
