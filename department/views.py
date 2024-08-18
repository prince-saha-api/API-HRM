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
        {'name': 'company', 'convert': None, 'replace':'company'}
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
# @deco.get_permission(['get company info', 'all'])
def adddepartment(request):
    response_message = []
    requestdata = request.data.copy()

    if 'address' in requestdata:
        addressobj = requestdata['address']

        required_fields = ['address', 'city', 'state_division', 'country']
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
            classOBJ=MODELS_CONT.Address,
            Serializer=PSRLZER_CONT.Addressserializer,
            data=addressobj,
            required_fields=required_fields
        )
        if responsesuccessflag == 'success': requestdata.update({'address': responsedata.instance.id})
        elif responsesuccessflag == 'error': del requestdata['address']


    unique_fields = ['email', 'phone', 'fax']
    required_fields = ['company']
    fields_regex = [
        {'field': 'email', 'type': 'email'},
        {'field': 'phone', 'type': 'phonenumber'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_DEPA.Department, 
        Serializer=PSRLZER_DEPA.Departmentserializer, 
        data=requestdata, 
        unique_fields=unique_fields, 
        required_fields=required_fields,
        fields_regex=fields_regex
    )
    if response_successflag == 'error':
        if 'address' in requestdata: MODELS_CONT.Address.objects.filter(id=requestdata['address']).delete()
    if response_data: response_data = response_data.data
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
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                    classOBJ=MODELS_CONT.Address,
                    Serializer=PSRLZER_CONT.Addressserializer,
                    id=address_id,
                    data=addressObj
                )
            del departmentObj['address']
        fields_regex = [
            {'field': 'email', 'type': 'email'},
            {'field': 'phone', 'type': 'phonenumber'}
        ]
        unique_fields = ['email', 'phone', 'fax']
        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
            classOBJ=MODELS_DEPA.Department, 
            Serializer=PSRLZER_DEPA.Departmentserializer, 
            id=departmentid, 
            data=departmentObj,
            fields_regex=fields_regex,
            unique_fields=unique_fields
        )
        response_data = response_data.data if response_successflag == 'success' else {}
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
        classOBJ=MODELS_DEPA.Department,
        id=departmentid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)