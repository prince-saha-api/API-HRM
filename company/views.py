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


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getcompanys(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'basic_information', 'convert': None, 'replace':'basic_information'},
                    {'name': 'address', 'convert': 'bool', 'replace':'address'},
                    {'name': 'company_owner', 'convert': 'bool', 'replace':'company_owner'},
                    {'name': 'is_active', 'convert': 'bool', 'replace':'is_active'},
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
def addcompany(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = []
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields = ['company_owner']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_COMP.Company, 
        PSRLZER_COMP.Companyserializer, 
        request.data,
        unique_fields=unique_fields, 
        extra_fields=extra_fields, 
        required_fields=required_fields
        )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatecompany(request, companyid=None):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_COMP.Company,
        PSRLZER_COMP.Companyserializer,
        companyid,
        request.data,
        extra_fields=extra_fields
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
                    {'name': 'industry_type', 'convert': None, 'replace':'industry_type'},
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
# @permission_classes([IsAuthenticated])
def addbasicinformation(request):
    requestdata = dict(request.data)
    options = {
        'allow_blank': True,
        'allow_empty': False
    }
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)


    response_message = []

    name = form.data.get('name')
    if name: name = name[0]

    legal_name = form.data.get('legal_name')
    if legal_name: legal_name = legal_name[0]

    establishment_date = form.data.get('establishment_date')
    if establishment_date: establishment_date = establishment_date[0]

    # industry_type = form.data.get('industry_type')
    print("----------------------------", form.data.get('industry_type'))
    if industry_type:
        industry_type = industry_type[0]
        if industry_type.isnumeric():
            industry_type = MODELS_COMP.Companytype.objects.filter(id=int(industry_type))
            if industry_type.exists():
                industry_type = industry_type.first()
            else:
                industry_type = None
                response_message.append('please provide a valid company_type id!')
        else:
            industry_type = None
            response_message.append('please provide a valid company_type id!')

    business_registration_number = form.data.get('business_registration_number')
    if business_registration_number: business_registration_number = business_registration_number[0]

    tax_id_number = form.data.get('tax_id_number')
    if tax_id_number: tax_id_number = tax_id_number[0]

    bin_no = form.data.get('bin_no')
    if bin_no: bin_no = bin_no[0]

    description = form.data.get('description')
    if description: description = description[0]

    website_url = form.data.get('website_url')
    if website_url: website_url = website_url[0]

    primary_email = form.data.get('primary_email')
    if primary_email: primary_email = primary_email[0]

    primary_phone_number = form.data.get('primary_phone_number')
    if primary_phone_number: primary_phone_number = primary_phone_number[0]

    fax = form.data.get('fax')
    if fax: fax = fax[0]

    logo = request.FILES.get('logo')

    city = state_division = post_zip_code = country = address = None
    if 'address' in form.data:
        if 'city' in form.data['address']:
            city = form.data['address']['city']
            if city: city = city[0]

        if 'state_division' in form.data['address']:
            state_division = form.data['address']['state_division']
            if state_division: state_division = state_division[0]

        if 'post_zip_code' in form.data['address']:
            post_zip_code = form.data['address']['post_zip_code']
            if post_zip_code: post_zip_code = post_zip_code[0]

        if 'country' in form.data['address']:
            country = form.data['address']['country']
            if country: country = country[0]

        if 'address' in form.data['address']:
            address = form.data['address']['address']
            if address: address = address[0]
        address_required_fields = [
            {'field': 'address', 'value': address},
            {'field': 'city', 'value': city},
            {'field': 'state_division', 'value': state_division},
            {'field': 'country', 'value': country}]        
        
        for required_field in address_required_fields:
            if not required_field['value']:
                response_message.append(f"{required_field['field']} is required in address!")

    unique_fields = [{'field': 'name', 'value': name}, 
                     {'field': 'business_registration_number', 'value': business_registration_number}, 
                     {'field': 'tax_id_number', 'value': tax_id_number},
                     {'field': 'bin_no', 'value': bin_no},
                     {'field': 'website_url', 'value': website_url},
                     {'field': 'primary_email', 'value': primary_email},
                     {'field': 'primary_phone_number', 'value': primary_phone_number},
                     {'field': 'fax', 'value': fax}]
    for unique_field in unique_fields:
        is_exist = MODELS_COMP.Basicinformation.objects.filter(**{unique_field['field']: unique_field['value']}).exists()
        if is_exist:
            response_message.append(f"{unique_field['field']} is already exist!")
    
    required_fields = [{'field': 'name', 'value': name}]

    for required_field in required_fields:
        if not bool(required_field['value']):
            response_message.append(f"{unique_field['field']} is required!")
    
    if not response_message:
        addressinstnace = MODELS_CONT.Address()
        if city: addressinstnace.city = city
        if state_division: addressinstnace.state_division = state_division
        if post_zip_code: addressinstnace.post_zip_code = post_zip_code
        if country: addressinstnace.country = country
        if address: addressinstnace.address = address
        addressinstnace.save()
        
        basicinformationinstance = MODELS_COMP.Basicinformation()
        if name: basicinformationinstance.name = name
        if legal_name: basicinformationinstance.legal_name = legal_name
        if establishment_date: basicinformationinstance.establishment_date = establishment_date
        if industry_type: basicinformationinstance.industry_type = industry_type
        if business_registration_number: basicinformationinstance.business_registration_number = business_registration_number
        if tax_id_number: basicinformationinstance.tax_id_number = tax_id_number
        if bin_no: basicinformationinstance.bin_no = bin_no
        if description: basicinformationinstance.description = description
        if website_url: basicinformationinstance.website_url = website_url
        if primary_email: basicinformationinstance.primary_email = primary_email
        if primary_phone_number: basicinformationinstance.primary_phone_number = primary_phone_number
        if fax: basicinformationinstance.fax = fax
        if logo: basicinformationinstance.logo = logo
        if addressinstnace: basicinformationinstance.address = addressinstnace
        basicinformationinstance.save()
        return Response({'data': SRLZER_COMP.Basicinformationserializer(basicinformationinstance, many=False).data, 'message': '', 'status': 'success'}, status=status.HTTP_200_OK)

    else: return Response({'status': 'error', 'message': response_message, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatebasicinformation(request, basicinformationid=None):
    requestdata = dict(request.data)
    options = {
        'allow_blank': True,
        'allow_empty': False
    }
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)

    userid = request.user.id
    error_message = []
    response_data = {}

    address_dict = {}
    addressid=MODELS_COMP.Basicinformation.objects.filter(id=basicinformationid).first().address.id
    if 'address' in form.data:
        if 'city' in form.data['address']:
            city = form.data['address']['city']
            if city: address_dict.update({'city': city[0]})

        if 'state_division' in form.data['address']:
            state_division = form.data['address']['state_division']
            if state_division: address_dict.update({'state_division': state_division[0]})

        if 'post_zip_code' in form.data['address']:
            post_zip_code = form.data['address']['post_zip_code']
            if post_zip_code: address_dict.update({'post_zip_code': post_zip_code[0]})

        if 'country' in form.data['address']:
            country = form.data['address']['country']
            if country: address_dict.update({'country': country[0]})

        if 'address' in form.data['address']:
            address = form.data['address']['address']
            if address: address_dict.update({'address': address[0]})

    if address_dict:
        _, response_message, _, _ = ghelp().updaterecord(
            MODELS_CONT.Address,
            PSRLZER_CONT.Addressserializer,
            addressid,
            address_dict
            )
        error_message.extend(response_message)

    basic_dict = {}
    name = form.data.get('name')
    if name: basic_dict.update({'name': name[0]})

    legal_name = form.data.get('legal_name')
    if legal_name: basic_dict.update({'legal_name': legal_name[0]})

    establishment_date = form.data.get('establishment_date')
    if establishment_date: basic_dict.update({'establishment_date': establishment_date[0]})

    industry_type = form.data.get('industry_type')
    if industry_type:
        try: basic_dict.update({'industry_type': int(industry_type[0])})
        except: pass

    business_registration_number = form.data.get('business_registration_number')
    if business_registration_number: basic_dict.update({'business_registration_number': business_registration_number[0]})

    tax_id_number = form.data.get('tax_id_number')
    if tax_id_number: basic_dict.update({'tax_id_number': tax_id_number[0]})

    bin_no = form.data.get('bin_no')
    if bin_no: basic_dict.update({'bin_no': bin_no[0]})

    description = form.data.get('description')
    if description: basic_dict.update({'description': description[0]})

    website_url = form.data.get('website_url')
    if website_url: basic_dict.update({'website_url': website_url[0]})

    primary_email = form.data.get('primary_email')
    if primary_email: basic_dict.update({'primary_email': primary_email[0]})

    primary_phone_number = form.data.get('primary_phone_number')
    if primary_phone_number: basic_dict.update({'primary_phone_number': primary_phone_number[0]})

    fax = form.data.get('fax')
    if fax: basic_dict.update({'fax': fax[0]})

    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})

    logo = request.FILES.get('logo')
    if logo: extra_fields.update({'logo': logo})
    
    if extra_fields:
        unique_fields = ['name', 'business_registration_number', 'tax_id_number', 'bin_no', 'website_url', 'primary_email', 'primary_phone_number', 'fax']
        fields_regex = [
            {'field': 'establishment_date', 'type': 'date'},
            {'field': 'primary_email', 'type': 'email'}
        ]
        response_data, response_message, _, _ = ghelp().updaterecord(
            MODELS_COMP.Basicinformation, 
            PSRLZER_COMP.Basicinformationserializer, 
            basicinformationid, 
            basic_dict,
            unique_fields=unique_fields,
            extra_fields=extra_fields,
            fields_regex=fields_regex
            )
        error_message.extend(response_message)
    
    return Response({'message': error_message, 'data': response_data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getcompanytypes(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'name', 'convert': None, 'replace':'name__icontains'}
                ]
    
    companytypes = MODELS_COMP.Companytype.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: companytypes = companytypes.order_by(column_accessor)

    total_count = companytypes.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: companytypes = companytypes[(page-1)*page_size:page*page_size]

    companytypeserializers = SRLZER_COMP.Companytypeserializer(companytypes, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': companytypeserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addcompanytype(request):
    required_fields = ['name']
    unique_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_COMP.Companytype,
        PSRLZER_COMP.Companytypeserializer, 
        request.data,
        unique_fields=unique_fields, 
        required_fields=required_fields
        )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatecompanytype(request, companytypeid=None):
    unique_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_COMP.Companytype,
        PSRLZER_COMP.Companytypeserializer,
        companytypeid,
        request.data,
        unique_fields=unique_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletecompanytype(request, companytypeid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_COMP.Basicinformation, 'fields': [{'field': 'industry_type', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_COMP.Companytype,
        companytypeid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)