from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from department import models as MODELS_DEPA
from contribution import models as MODELS_CONT
from contribution.serializer.POST import serializers as PSRLZER_CONT
from department.serializer.POST import serializers as PSRLZER_DEPA
from department.serializer import serializers as SRLZER_DEPA
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getdepartments(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
                        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
                        {'name': 'email', 'convert': None, 'replace':'email__icontains'},
                        {'name': 'phone', 'convert': None, 'replace':'phone__icontains'},
                        {'name': 'fax', 'convert': None, 'replace':'fax__icontains'},
                        {'name': 'company', 'convert': None, 'replace':'company'},
                        {'name': 'branch', 'convert': None, 'replace':'branch'}
                    ]
    departments = MODELS_DEPA.Department.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: departments = departments.order_by(column_accessor)
    
    total_count = departments.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: departments = departments[(page-1)*page_size:page*page_size]

    departmentserializers = SRLZER_DEPA.Departmentserializer(departments, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': departmentserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adddepartment(request):
    response_message = []
    departmentObj = request.data

    if 'address' in departmentObj:
        addressobj = departmentObj['address']
        addressresponse = ghelp().addaddress(MODELS_CONT.Address, addressobj)
        if addressresponse['flag']: departmentObj.update({'address': addressresponse['instance'].id})

    unique_fields = ['email', 'phone', 'fax']
    required_fields = ['company', 'branch']
    fields_regex = [
        {'field': 'email', 'type': 'email'},
        {'field': 'phone', 'type': 'phonenumber'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_DEPA.Department, 
        PSRLZER_DEPA.Departmentserializer, 
        departmentObj, 
        unique_fields=unique_fields, 
        required_fields=required_fields,
        fields_regex=fields_regex
        )
    if response_successflag == 'error':
        if 'address' in departmentObj:
            address = MODELS_CONT.Address.objects.filter(id=departmentObj['address'])
            if address.exists(): address.delete()
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatedepartment(request, departmentid=None):
    department = MODELS_DEPA.Department.objects.filter(id=departmentid)
    if department.exists():

        address_id = None
        department = department.first()
        if department.address: address_id = department.address.id

        departmentObj = request.data

        addressObj = None
        if 'address' in departmentObj:
            addressObj = departmentObj['address']
            if address_id:
                response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                    MODELS_CONT.Address,
                    PSRLZER_CONT.Addressserializer,
                    address_id,
                    addressObj
                    )
            del departmentObj['address']
        fields_regex = [
            {'field': 'email', 'type': 'email'},
            {'field': 'phone', 'type': 'phone'}
        ]
        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
            MODELS_DEPA.Department, 
            PSRLZER_DEPA.Departmentserializer, 
            departmentid, 
            departmentObj,
            fields_regex=fields_regex
            )

        return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    else: return Response({'data': {}, 'message': ['branch doesn\'t exist!'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletedepartment(request, departmentid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_DEPA.Departmentmobilenumber, 'fields': [{'field': 'department', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_DEPA.Departmentemail, 'fields': [{'field': 'department', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_DEPA.Departmentimage, 'fields': [{'field': 'department', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_DEPA.Department,
        departmentid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)