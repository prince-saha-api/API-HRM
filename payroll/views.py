from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from payroll import models as MODELS_PAYR
from payroll.serializer import serializers as SRLZER_PAYR
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
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
    payrollearningserializers = SRLZER_PAYR.Payrollearningserializer(payrollearnings, many=True)
    return Response({'status': 'success', 'message': '', 'data': payrollearningserializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addpayrollearning(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_PAYR.Payrollearning, SRLZER_PAYR.Payrollearningserializer, request.data, allowed_fields=['__all__'], unique_fields=[], extra_fields=extra_fields)
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
                    {'name': 'amount', 'convert': None, 'replace':'amount'},
                    {'name': 'updated_by', 'convert': None, 'replace':'updated_by'},
                    {'name': 'created_by', 'convert': None, 'replace':'created_by'}
                ]
    payrolldeductions = MODELS_PAYR.Payrolldeduction.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: payrolldeductions = payrolldeductions.order_by(column_accessor)
    payrolldeductionserializers = SRLZER_PAYR.Payrolldeductionserializer(payrolldeductions, many=True)
    return Response({'status': 'success', 'message': '', 'data': payrolldeductionserializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addpayrolldeduction(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_PAYR.Payrolldeduction, SRLZER_PAYR.Payrolldeductionserializer, request.data, allowed_fields=['__all__'], unique_fields=[], extra_fields=extra_fields)
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
def addpayrolltax(request):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_PAYR.Payrolltax, SRLZER_PAYR.Payrolltaxserializer, request.data, allowed_fields=['__all__'], unique_fields=['title'], extra_fields=extra_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def addpayrolltax(request):
#     response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_PAYR.Payrolltax, SRLZER_PAYR.Payrolltaxserializer, request.data, [])
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

