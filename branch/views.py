from contribution.serializer.POST import serializers as PSRLZER_CONT
from rest_framework.decorators import api_view, permission_classes
from branch.serializer.POST import serializers as PSRLZER_BRAN
from branch.serializer import serializers as SRLZER_BRAN
from helps.common.generic import Generichelps as ghelp
from rest_framework.permissions import IsAuthenticated
from contribution import models as MODELS_CONT
from department import models as MODELS_DEPA
from rest_framework.response import Response
from branch import models as MODELS_BRAN
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getoperatinghours(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'operating_hour_from', 'convert': None, 'replace':'operating_hour_from'},
        {'name': 'operating_hour_to', 'convert': None, 'replace':'operating_hour_to'}
    ]
    operatinghours = MODELS_BRAN.Operatinghour.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: operatinghours = operatinghours.order_by(column_accessor)

    total_count = operatinghours.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: operatinghours = operatinghours[(page-1)*page_size:page*page_size]

    operatinghourserializers = SRLZER_BRAN.Operatinghourserializer(operatinghours, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': operatinghourserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def addoperatinghour(request):
    required_fields = ['operating_hour_from', 'operating_hour_to']
    fields_regex = [
        {'field': 'operating_hour_from', 'type': 'time'},
        {'field': 'operating_hour_to', 'type': 'time'},
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_BRAN.Operatinghour,
        Serializer=PSRLZER_BRAN.Operatinghourserializer,
        data=request.data,
        required_fields=required_fields,
        fields_regex=fields_regex
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateoperatinghour(request, operatinghourid=None):
    fields_regex = [
        {'field': 'operating_hour_from', 'type': 'time'},
        {'field': 'operating_hour_to', 'type': 'time'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_BRAN.Operatinghour, 
        Serializer=PSRLZER_BRAN.Operatinghourserializer, 
        id=operatinghourid, 
        data=request.data,
        fields_regex=fields_regex
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteoperatinghour(request, operatinghourid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_BRAN.Operatinghour,
        id=operatinghourid
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getbranchs(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'company', 'convert': None, 'replace':'branch_company__id'},
        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
        {'name': 'email', 'convert': None, 'replace':'email__icontains'},
        {'name': 'phone', 'convert': None, 'replace':'phone__icontains'},
        {'name': 'fax', 'convert': None, 'replace':'fax__icontains'}
    ]
    branchs = MODELS_BRAN.Branch.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: branchs = branchs.order_by(column_accessor)

    total_count = branchs.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: branchs = branchs[(page-1)*page_size:page*page_size]

    branchserializers = SRLZER_BRAN.Branchserializer(branchs, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': branchserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def addbranch(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    branchObj = request.data
    if 'address' in branchObj:
        addressobj = branchObj['address']

        required_fields = ['address', 'city', 'state_division', 'country']
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
            classOBJ=MODELS_CONT.Address,
            Serializer=PSRLZER_CONT.Addressserializer,
            data=addressobj,
            required_fields=required_fields
        )
        if responsesuccessflag == 'success': branchObj.update({'address': responsedata.data['id']})
        elif responsesuccessflag == 'error':
            response_message.extend(responsemessage)
            del branchObj['address']

    required_fields = ['name', 'company']
    unique_fields = ['email', 'phone', 'fax']
    fields_regex = [
        {'field': 'email', 'type': 'email'},
        {'field': 'phone', 'type': 'phonenumber'}
    ]
    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
        classOBJ=MODELS_BRAN.Branch,
        Serializer=PSRLZER_BRAN.Branchserializer,
        data=branchObj,
        unique_fields=unique_fields,
        required_fields=required_fields,
        fields_regex=fields_regex
    )
    if responsesuccessflag == 'success':
        response_data = responsedata.data
        response_successflag = responsesuccessflag
        response_status = responsestatus
    elif responsesuccessflag == 'error':
        response_message.extend(responsemessage)

    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatebranch(request, branchid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    branch = MODELS_BRAN.Branch.objects.filter(id=branchid)
    if branch.exists():
        branchObj = request.data
        if 'address' in branchObj:
            addressObj = branchObj['address']
            addressid = branch.first().address.id
            if addressid:
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                    classOBJ=MODELS_CONT.Address,
                    Serializer=PSRLZER_CONT.Addressserializer,
                    id=addressid,
                    data=addressObj
                )
                if responsesuccessflag == 'error': response_message.extend(responsemessage)
            del branchObj['address']

        fields_regex = [
            {'field': 'email', 'type': 'email'},
            {'field': 'phone', 'type': 'phonenumber'}
        ]
        unique_fields = ['email', 'phone', 'fax']
        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
            classOBJ=MODELS_BRAN.Branch, 
            Serializer=PSRLZER_BRAN.Branchserializer, 
            id=branchid, 
            data=branchObj,
            unique_fields=unique_fields,
            fields_regex=fields_regex
        )
        if responsesuccessflag == 'success':
            response_data = responsedata.data
            response_successflag = responsesuccessflag
            response_status = responsestatus
        if responsesuccessflag == 'error':
            response_message.extend(responsemessage)
    else: response_message.append('branch doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletebranch(request, branchid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_BRAN.Branchphonenumber, 'fields': [{'field': 'branch', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_BRAN.Branchemail, 'fields': [{'field': 'branch', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_BRAN.Contactperson, 'fields': [{'field': 'branch', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_BRAN.Branch,
        id=branchid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)