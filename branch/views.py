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
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getoperatinghours(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'operating_hour_from', 'convert': None, 'replace':'operating_hour_from'},
                        {'name': 'operating_hour_to', 'convert': None, 'replace':'operating_hour_to'},
                        {'name': 'is_active', 'convert': 'bool', 'replace':'is_active'}
                    ]
    operatinghours = MODELS_BRAN.Operatinghour.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: operatinghours = operatinghours.order_by(column_accessor)
    operatinghourserializers = SRLZER_BRAN.Operatinghourserializer(operatinghours, many=True)
    return Response(operatinghourserializers.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Single Permission Details', 'all'])
# def getoperatinghours(request):
#     operatinghours = MODELS_BRAN.Operatinghour.objects.all()
#     operatinghourserializers = SRLZER_BRAN.Operatinghourserializer(operatinghours, many=True)
#     return Response(operatinghourserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addoperatinghour(request):
    operatinghourserializers = SRLZER_BRAN.Operatinghourserializer(data=request.data, many=False)
    if operatinghourserializers.is_valid():
        operatinghourserializers.save()
        return Response({'status': 'success', 'message': '', 'data': operatinghourserializers.data}, status=status.HTTP_201_CREATED)
    else: return Response({'status': 'error', 'message': '', 'data': operatinghourserializers.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getbranchs(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'company', 'convert': None, 'replace':'company'},
                        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
                        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
                        {'name': 'email', 'convert': None, 'replace':'email__icontains'},
                        {'name': 'address', 'convert': None, 'replace':'address__icontains'},
                        {'name': 'phone', 'convert': None, 'replace':'phone__icontains'},
                        {'name': 'operating_hour', 'convert': None, 'replace':'operating_hour'},
                        {'name': 'facilities', 'convert': None, 'replace':'facilities'},
                        {'name': 'is_active', 'convert': 'bool', 'replace':'is_active'},
                    ]
    branchs = MODELS_BRAN.Branch.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: branchs = branchs.order_by(column_accessor)

    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    branchs = branchs[(page-1)*page_size:page*page_size]

    branchserializers = SRLZER_BRAN.Branchserializer(branchs, many=True)
    return Response({'data': {
        'count': MODELS_BRAN.Branch.objects.all().count(),
        'page': page,
        'page_size': page_size,
        'result': branchserializers.data
    }, 'message': '', 'status': 'success'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addbranch(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['email','phone']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_BRAN.Branch, SRLZER_BRAN.Branchserializer, request.data, unique_fields=unique_fields, extra_fields=extra_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatebranch(request, branchid=None):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    allowed_fields = ['company', 'name', 'description', 'email', 'address', 'phone', 'operating_hour', 'facilities', 'is_active']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(MODELS_BRAN.Branch, SRLZER_BRAN.Branchserializer, branchid, request.data, allowed_fields=allowed_fields, extra_fields=extra_fields)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)