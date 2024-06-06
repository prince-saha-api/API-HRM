from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from facility import models as MODELS_FACI
from facility.serializer import serializers as SRLZER_FACI
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getfacilitys(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'title', 'convert': None, 'replace':'title__icontains'},
                    {'name': 'description', 'convert': None, 'replace':'description__icontains'},
                    {'name': 'is_active', 'convert': "bool", 'replace':'is_active'},
                    {'name': 'created_at', 'convert': None, 'replace':'created_at'},
                    {'name': 'updated_at', 'convert': None, 'replace':'updated_at'}
                ]
    facilitys = MODELS_FACI.Facility.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: facilitys = facilitys.order_by(column_accessor)
    facilityserializers = SRLZER_FACI.Facilityserializer(facilitys, many=True)
    return Response({'status': 'success', 'message': '', 'data': facilityserializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addfacility(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['title']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_FACI.Facility, SRLZER_FACI.Facilityserializer, request.data, unique_fields=unique_fields, extra_fields=extra_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatefacility(request, facilityid=None):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    allowed_fields = ['title', 'description', 'is_active']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(MODELS_FACI.Facility, SRLZER_FACI.Facilityserializer, facilityid, request.data, allowed_fields=allowed_fields, extra_fields=extra_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)