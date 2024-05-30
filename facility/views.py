from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from facility import models as MODELS_FACI
from facility.serializer import serializers as SRLZER_FACI
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getfacilitys(request):
    facilitys = MODELS_FACI.Facility.objects.all()
    facilityserializers = SRLZER_FACI.Facilityserializer(facilitys, many=True)
    return Response(facilityserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addfacility(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_FACI.Facility, SRLZER_FACI.Facilityserializer, request.data, unique_fields=['title'])
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
