from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from company import models as MODELS_COMP
from company.serializer import serializers as SRLZER_COMP
from company.serializer.POST import serializers as PSRLZER_COMP
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from drf_nested_forms.utils import NestedForm
from rest_framework import status
from contribution import models as MODELS_CONT
from contribution.serializer.POST import serializers as PSRLZER_CONT


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getcompanys(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'basic_information', 'convert': None, 'replace':'basic_information'},
                    {'name': 'company_owner', 'convert': 'bool', 'replace':'company_owner'}
                ]
    companys = MODELS_COMP.Company.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: companys = companys.order_by(column_accessor)

    total_count = companys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: companys = companys[(page-1)*page_size:page*page_size]

    companyserializers = SRLZER_COMP.Companyserializer(companys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': companyserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addcompany(request):
    required_fields = ['company_owner']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_COMP.Company, 
        PSRLZER_COMP.Companyserializer, 
        request.data,
        required_fields=required_fields
        )
    if response_successflag == 'success': response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatecompany(request, companyid=None):
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_COMP.Company,
        PSRLZER_COMP.Companyserializer,
        companyid,
        request.data
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbasicinformations(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'name', 'convert': None, 'replace':'name__icontains'},
                    {'name': 'legal_name', 'convert': None, 'replace':'legal_name__icontains'},
                    {'name': 'establishment_date', 'convert': None, 'replace':'establishment_date__icontains'},
                    {'name': 'industry_type', 'convert': None, 'replace':'industry_type__icontains'},
                    {'name': 'business_registration_number', 'convert': None, 'replace':'business_registration_number__icontains'},
                    {'name': 'tax_id_number', 'convert': None, 'replace':'tax_id_number__icontains'},
                    {'name': 'bin_no', 'convert': None, 'replace':'bin_no__icontains'},
                    {'name': 'description', 'convert': None, 'replace':'description__icontains'},
                    {'name': 'website_url', 'convert': None, 'replace':'website_url__icontains'},
                    {'name': 'primary_email', 'convert': None, 'replace':'primary_email__icontains'},
                    {'name': 'primary_phone_number', 'convert': None, 'replace':'primary_phone_number__icontains'},
                    {'name': 'fax', 'convert': None, 'replace':'fax__icontains'},
                    {'name': 'address', 'convert': None, 'replace':'address'}
                ]
    basicinformations = MODELS_COMP.Basicinformation.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: basicinformations = basicinformations.order_by(column_accessor)

    total_count = basicinformations.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: basicinformations = basicinformations[(page-1)*page_size:page*page_size]

    basicinformationserializers = SRLZER_COMP.Basicinformationserializer(basicinformations, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': basicinformationserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addbasicinformation(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    requestdata = request.data.copy()
    requestdata = dict(requestdata)
    options = {
        'allow_blank': True,
        'allow_empty': False
    }
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)
    basicinfo = ghelp().prepareData(form.data, 'basicinfo')

    if 'address' in basicinfo:
        address = basicinfo['address']

        required_fields = ['address', 'city', 'state_division', 'country']
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
            MODELS_CONT.Address,
            PSRLZER_CONT.Addressserializer,
            address,
            required_fields=required_fields
        )
        if responsesuccessflag == 'success': basicinfo.update({'address': responsedata.data['id']})
        elif responsesuccessflag == 'error':
            response_message.extend(responsemessage)
            del basicinfo['address']
    
    required_fields = ['name']
    unique_fields = ['name', 'business_registration_number', 'tax_id_number', 'bin_no', 'website_url', 'primary_email', 'primary_phone_number', 'fax']
    fields_regex = [
            {'field': 'establishment_date', 'type': 'date'},
            {'field': 'primary_email', 'type': 'email'},
            {'field': 'primary_phone_number', 'type': 'phonenumber'},
        ]
    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
        MODELS_COMP.Basicinformation, 
        PSRLZER_COMP.Basicinformationserializer, 
        basicinfo,
        required_fields=required_fields,
        unique_fields=unique_fields,
        fields_regex=fields_regex
    )
    if responsesuccessflag == 'success':
        response_data = responsedata.data
        response_message.extend(responsemessage)
        response_successflag = responsesuccessflag
        response_status = responsestatus
    elif responsesuccessflag == 'error':
        response_message.extend(responsemessage)
    return Response({'status': response_successflag, 'message': response_message, 'data': response_data}, status=response_status)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatebasicinformation(request, basicinformationid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    basicinformation = MODELS_COMP.Basicinformation.objects.filter(id=basicinformationid)
    if basicinformation.exists():
        requestdata = request.data.copy()
        requestdata = dict(requestdata)
        options = {
            'allow_blank': True,
            'allow_empty': False
        }
        form = NestedForm(requestdata, **options)
        form.is_nested(raise_exception=True)
        basicinfo = ghelp().prepareData(form.data, 'basicinfo')
        
        if 'address' in basicinfo:
            addressid = basicinformation.first().address.id
            address = basicinfo['address']
            del basicinfo['address']

            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                MODELS_CONT.Address, 
                PSRLZER_CONT.Addressserializer,
                addressid, 
                address
            )
            if responsesuccessflag == 'error': response_message.extend(responsemessage)
        
        if not response_message:
            unique_fields = ['name', 'business_registration_number', 'tax_id_number', 'bin_no', 'website_url', 'primary_email', 'primary_phone_number', 'fax']
            fields_regex = [
                {'field': 'establishment_date', 'type': 'date'},
                {'field': 'primary_email', 'type': 'email'},
                {'field': 'primary_phone_number', 'type': 'phonenumber'},
            ]
            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                MODELS_COMP.Basicinformation, 
                PSRLZER_COMP.Basicinformationserializer, 
                basicinformationid, 
                basicinfo,
                unique_fields=unique_fields,
                fields_regex=fields_regex
                )
            if responsesuccessflag == 'success':
                response_data = responsedata
                response_successflag = responsesuccessflag
                response_status = responsestatus
            elif responsesuccessflag == 'error': response_message.extend(responsemessage)
    else: response_message.append(f'Basic Information doean\'t exist with this id({basicinformationid})')
    
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)