from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from branch import models as MODELS_BRAN
from contribution import models as MODELS_CONT
from department import models as MODELS_DEPA
from branch.serializer import serializers as SRLZER_BRAN
from branch.serializer.POST import serializers as PSRLZER_BRAN
from contribution.serializer.POST import serializers as PSRLZER_CONT
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
    operatinghourserializers = PSRLZER_BRAN.Operatinghourserializer(data=request.data, many=False)
    if operatinghourserializers.is_valid():
        operatinghourserializers.save()
        return Response({'status': 'success', 'message': [], 'data': operatinghourserializers.data}, status=status.HTTP_201_CREATED)
    else: return Response({'status': 'error', 'message': [], 'data': operatinghourserializers.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateoperatinghour(request, operatinghourid=None):
    fields_regex = [
        {'field': 'operating_hour_from', 'type': 'time'},
        {'field': 'operating_hour_to', 'type': 'time'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_BRAN.Operatinghour, 
        PSRLZER_BRAN.Operatinghourserializer, 
        operatinghourid, 
        request.data,
        fields_regex=fields_regex
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteoperatinghour(request, operatinghourid=None):
    classOBJpackage_tocheck_assciaativity = [
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_BRAN.Operatinghour,
        operatinghourid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def getbranchs(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
                        {'name': 'company', 'convert': None, 'replace':'company__id'},
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
            MODELS_CONT.Address,
            PSRLZER_CONT.Addressserializer,
            addressobj,
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
        MODELS_BRAN.Branch,
        PSRLZER_BRAN.Branchserializer,
        branchObj,
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

    if branchid:
        branch = MODELS_BRAN.Branch.objects.filter(id=branchid)
        if branch.exists():
            branchObj = request.data
            if 'address' in branchObj:
                addressObj = branchObj['address']
                addressid = branch.first().address.id
                if addressid:
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                        MODELS_CONT.Address,
                        PSRLZER_CONT.Addressserializer,
                        addressid,
                        addressObj
                    )
                    if responsesuccessflag == 'error': response_message.extend(responsemessage)
                del branchObj['address']

            fields_regex = [
                {'field': 'email', 'type': 'email'},
                {'field': 'phone', 'type': 'phonenumber'}
            ]
            unique_fields = ['email', 'phone', 'fax']
            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                MODELS_BRAN.Branch, 
                PSRLZER_BRAN.Branchserializer, 
                branchid, 
                branchObj,
                unique_fields=unique_fields,
                fields_regex=fields_regex
            )
            if responsesuccessflag == 'success':
                response_data = responsedata
                response_successflag = responsesuccessflag
                response_status = responsestatus
            if responsesuccessflag == 'error':
                response_message.extend(responsemessage)
        else: response_message.append('branch doesn\'t exist!')
    else: response_message.append('please provide a branch id!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletebranch(request, branchid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_BRAN.Branchphonenumber, 'fields': [{'field': 'branch', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_BRAN.Branchemail, 'fields': [{'field': 'branch', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_BRAN.Contactperson, 'fields': [{'field': 'branch', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_DEPA.Department, 'fields': [{'field': 'branch', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        MODELS_BRAN.Branch,
        branchid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)