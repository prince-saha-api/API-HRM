from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from payroll import models as MODELS_PAYR
from payroll.serializer import serializers as SRLZER_PAYR
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getpayrollearnings(request):
    payrollearnings = MODELS_PAYR.Payrollearning.objects.all()
    payrollearningserializers = SRLZER_PAYR.Payrollearningserializer(payrollearnings, many=True)
    return Response(payrollearningserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addpayrollearning(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_PAYR.Payrollearning, SRLZER_PAYR.Payrollearningserializer, request.data, [])
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getpayrolldeductions(request):
    payrolldeductions = MODELS_PAYR.Payrolldeduction.objects.all()
    payrolldeductionserializers = SRLZER_PAYR.Payrolldeductionserializer(payrolldeductions, many=True)
    return Response(payrolldeductionserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addpayrolldeduction(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_PAYR.Payrolldeduction, SRLZER_PAYR.Payrolldeductionserializer, request.data, [])
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getpayrolltaxs(request):
    payrolltaxs = MODELS_PAYR.Payrolltax.objects.all()
    payrolltaxserializers = SRLZER_PAYR.Payrolltaxserializer(payrolltaxs, many=True)
    return Response(payrolltaxserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addpayrolltax(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_PAYR.Payrolltax, SRLZER_PAYR.Payrolltaxserializer, request.data, [])
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

