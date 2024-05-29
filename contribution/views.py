from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from contribution import models as MODELS_CONT
from contribution.serializer import serializers as SRLZER_CONT
from rest_framework import status
from helps.common.generic import Generichelps as ghelp

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getaddresss(request):
    addresss = MODELS_CONT.Address.objects.all()
    addressserializers = SRLZER_CONT.Addressserializer(addresss, many=True)
    return Response(addressserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addaddress(request):
    addresss = request.data
    if 'address' not in addresss: return Response({'data': {}, 'message': 'address is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'city' not in addresss: return Response({'data': {}, 'message': 'city is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'state_division' not in addresss: return Response({'data': {}, 'message': 'state_division is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'country' not in addresss: return Response({'data': {}, 'message': 'country is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    addressserializers = SRLZER_CONT.Addressserializer(data=request.data, many=False)
    if addressserializers.is_valid():
        addressserializers.save()
        return Response({'data': addressserializers.data}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbankaccounttypes(request):
    bankaccounttypes = MODELS_CONT.Bankaccounttype.objects.all()
    bankaccounttypeserializers = SRLZER_CONT.Bankaccounttypeserializer(bankaccounttypes, many=True)
    return Response(bankaccounttypeserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addbankaccounttype(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_CONT.Bankaccounttype, SRLZER_CONT.Bankaccounttypeserializer, request.data, ['name'])
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbankaccounts(request):
    bankaccounts = MODELS_CONT.Bankaccount.objects.all()
    bankaccountserializers = SRLZER_CONT.Bankaccountserializer(bankaccounts, many=True)
    return Response(bankaccountserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addbankaccount(request):
    bankaccounts = request.data
    if 'bank_name' not in bankaccounts: return Response({'data': {}, 'message': 'bank_name is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'branch_name' not in bankaccounts: return Response({'data': {}, 'message': 'branch_name is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'account_type' not in bankaccounts: return Response({'data': {}, 'message': 'account_type is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'account_no' not in bankaccounts: return Response({'data': {}, 'message': 'account_no is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'routing_no' not in bankaccounts: return Response({'data': {}, 'message': 'routing_no is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    bankaccountserializers = SRLZER_CONT.Bankaccountserializer(data=request.data, many=False)
    if bankaccountserializers.is_valid():
        bankaccountserializers.save()
        return Response({'data': bankaccountserializers.data}, status=status.HTTP_201_CREATED)
