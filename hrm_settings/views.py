from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from hrm_settings import models as MODELS_SETT
from hrm_settings.serializer import serializers as SRLZER_SETT
from hrm_settings.serializer.POST import serializers as PSRLZER_SETT
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getfiscalyears(request):
    fiscalyears = MODELS_SETT.Fiscalyear.objects.all()
    fiscalyearserializers = SRLZER_SETT.Fiscalyearserializer(fiscalyears, many=True)
    return Response(fiscalyearserializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def addfiscalyear(request):
    fiscalyearserializers = PSRLZER_SETT.Fiscalyearserializer(data=request.data, many=False)
    if fiscalyearserializers.is_valid():
        fiscalyearserializers.save()
        return Response({'data': fiscalyearserializers.data}, status=status.HTTP_201_CREATED)
    else: return Response({'data': []}, status=status.HTTP_400_BAD_REQUEST)