from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from branch import models as MODELS_BRAN
from branch.serializer import serializers as SRLZER_BRAN
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getoperatinghours(request):
    operatinghours = MODELS_BRAN.Operatinghour.objects.all()
    operatinghourserializers = SRLZER_BRAN.Operatinghourserializer(operatinghours, many=True)
    return Response(operatinghourserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addoperatinghour(request):
    operatinghourserializers = SRLZER_BRAN.Operatinghourserializer(data=request.data, many=False)
    if operatinghourserializers.is_valid():
        operatinghourserializers.save()
        return Response({'status': 'success', 'message': '', 'data': operatinghourserializers.data}, status=status.HTTP_201_CREATED)
    else: return Response({'status': 'error', 'message': '', 'data': operatinghourserializers.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbranchs(request):
    branchs = MODELS_BRAN.Branch.objects.all()
    branchserializers = SRLZER_BRAN.Branchserializer(branchs, many=True)
    return Response(branchserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addbranch(request):
    branchserializers = SRLZER_BRAN.Branchserializer(data=request.data, many=False)
    if branchserializers.is_valid():
        branchserializers.save()
        return Response({'status': 'success', 'message': '', 'data': branchserializers.data}, status=status.HTTP_201_CREATED)
    else: return Response({'status': 'error', 'message': '', 'data': branchserializers.errors}, status=status.HTTP_400_BAD_REQUEST)
