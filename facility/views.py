from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from facility import models as MODELS_FACI
from facility.serializer import serializers as SRLZER_FACI
from facility.serializer.POST import serializers as PSRLZER_FACI
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

    total_count = facilitys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: facilitys = facilitys[(page-1)*page_size:page*page_size]

    facilityserializers = SRLZER_FACI.Facilityserializer(facilitys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': facilityserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addfacility(request):
    unique_fields = ['title']
    required_fields = ['title']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_FACI.Facility,
        Serializer=PSRLZER_FACI.Facilityserializer, 
        data=request.data, 
        unique_fields=unique_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatefacility(request, facilityid=None):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    unique_fields=['title']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_FACI.Facility,
        Serializer=PSRLZER_FACI.Facilityserializer,
        id=facilityid,
        data=request.data,
        extra_fields=extra_fields,
        unique_fields=unique_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)