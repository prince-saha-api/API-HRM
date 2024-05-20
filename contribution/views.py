from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from contribution import models as MODELS_CON
from contribution.serializer import serializers as SRLZER_CON
from rest_framework import status

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getaddresss(request):
    addresss = MODELS_CON.Address.objects.all()
    addressserializers = SRLZER_CON.Addressserializer(addresss, many=True)
    return Response(addressserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addaddress(request):
    addressserializers = SRLZER_CON.Addressserializer(data=request.data, many=False)
    if addressserializers.is_valid():
        addressserializers.save()
        return Response({'data': addressserializers.data}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbankaccounttypes(request):
    bankaccounttypes = MODELS_CON.Bankaccounttype.objects.all()
    bankaccounttypeserializers = SRLZER_CON.Bankaccounttypeserializer(bankaccounttypes, many=True)
    return Response(bankaccounttypeserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addbankaccounttype(request):
    bankaccounttypeserializers = SRLZER_CON.Bankaccounttypeserializer(data=request.data, many=False)
    if bankaccounttypeserializers.is_valid():
        bankaccounttypeserializers.save()
        return Response({'data': bankaccounttypeserializers.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbankaccounts(request):
    bankaccounts = MODELS_CON.Bankaccount.objects.all()
    bankaccountserializers = SRLZER_CON.Bankaccountserializer(bankaccounts, many=True)
    return Response(bankaccountserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addbankaccount(request):
    bankaccountserializers = SRLZER_CON.Bankaccountserializer(data=request.data, many=False)
    if bankaccountserializers.is_valid():
        bankaccountserializers.save()
        return Response({'data': bankaccountserializers.data}, status=status.HTTP_201_CREATED)
