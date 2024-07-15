from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user import models as MODELS_USER
from branch import models as MODELS_BRAN
from company import models as MODELS_COMP
from department import models as MODELS_DEPA
from contribution import models as MODELS_CONT
from contribution.serializer import serializers as SRLZER_CONT
from contribution.serializer.POST import serializers as PSRLZER_CONT
from rest_framework import status
from helps.common.generic import Generichelps as ghelp

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getaddresss(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'alias', 'convert': None, 'replace':'alias__icontains'},
        {'name': 'address', 'convert': None, 'replace':'address__icontains'},
        {'name': 'city', 'convert': None, 'replace':'city__icontains'},
        {'name': 'state_division', 'convert': None, 'replace':'state_division__icontains'},
        {'name': 'post_zip_code', 'convert': None, 'replace':'post_zip_code__icontains'},
        {'name': 'country', 'convert': None, 'replace':'country__icontains'},
        {'name': 'latitude', 'convert': None, 'replace':'latitude'},
        {'name': 'longitude', 'convert': None, 'replace':'longitude'},
    ]
    addresss = MODELS_CONT.Address.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: addresss = addresss.order_by(column_accessor)
    
    total_count = addresss.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: addresss = addresss[(page-1)*page_size:page*page_size]

    addressserializers = SRLZER_CONT.Addressserializer(addresss, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': addressserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addaddress(request):
    required_fields = ['address', 'city', 'state_division', 'country']

    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_CONT.Address, 
        Serializer=PSRLZER_CONT.Addressserializer, 
        data=request.data,
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateaddress(request, addressid=None):
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_CONT.Address, 
        Serializer=PSRLZER_CONT.Addressserializer,
        id=addressid,
        data=request.data
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteaddress(request, addressid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_BRAN.Branch, 'fields': [{'field': 'address', 'relation': 'onetoonefield', 'records': []}]},
        {'model': MODELS_COMP.Basicinformation, 'fields': [{'field': 'address', 'relation': 'onetoonefield', 'records': []}]},
        {'model': MODELS_COMP.Company, 'fields': [{'field': 'address', 'relation': 'onetoonefield', 'records': []}]},
        {'model': MODELS_CONT.Bankaccount, 'fields': [{'field': 'address', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_DEPA.Department, 'fields': [{'field': 'address', 'relation': 'onetoonefield', 'records': []}]},
        {'model': MODELS_USER.User, 'fields': [{'field': 'present_address', 'relation': 'onetoonefield', 'records': []}, {'field': 'permanent_address', 'relation': 'onetoonefield', 'records': []}]},
        {'model': MODELS_USER.Employeecontact, 'fields': [{'field': 'address', 'relation': 'onetoonefield', 'records': []}]},
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_CONT.Address,
        id=addressid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbankaccounttypes(request):
    filter_fields = [
                        {'name': 'id', 'convert': None, 'replace':'id'},
                        {'name': 'name', 'convert': None, 'replace':'name__icontains'}
                    ]
    bankaccounttypes = MODELS_CONT.Bankaccounttype.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: bankaccounttypes = bankaccounttypes.order_by(column_accessor)
    
    total_count = bankaccounttypes.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: bankaccounttypes = bankaccounttypes[(page-1)*page_size:page*page_size]

    bankaccounttypeserializers = SRLZER_CONT.Bankaccounttypeserializer(bankaccounttypes, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': bankaccounttypeserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addbankaccounttype(request):
    required_fields = ['name']
    unique_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_CONT.Bankaccounttype,
        Serializer=PSRLZER_CONT.Bankaccounttypeserializer,
        data=request.data,
        unique_fields=unique_fields,
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatebankaccounttype(request, bankaccounttypeid=None):
    unique_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_CONT.Bankaccounttype, 
        Serializer=PSRLZER_CONT.Bankaccounttypeserializer,
        id=bankaccounttypeid,
        data=request.data,
        unique_fields=unique_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletebankaccounttype(request, bankaccounttypeid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_CONT.Bankaccount, 'fields': [{'field': 'account_type', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_CONT.Bankaccounttype,
        id=bankaccounttypeid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbankaccounts(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'bank_name', 'convert': None, 'replace':'bank_name__icontains'},
        {'name': 'branch_name', 'convert': None, 'replace':'branch_name__icontains'},
        {'name': 'account_type', 'convert': None, 'replace':'account_type'},
        {'name': 'account_no', 'convert': None, 'replace':'account_no__icontains'},
        {'name': 'routing_no', 'convert': None, 'replace':'routing_no__icontains'},
        {'name': 'swift_bic', 'convert': None, 'replace':'swift_bic__icontains'},
        {'name': 'address', 'convert': None, 'replace':'address'}
    ]
    bankaccounts = MODELS_CONT.Bankaccount.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: bankaccounts = bankaccounts.order_by(column_accessor)
    
    total_count = bankaccounts.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: bankaccounts = bankaccounts[(page-1)*page_size:page*page_size]

    bankaccountserializers = SRLZER_CONT.Bankaccountserializer(bankaccounts, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': bankaccountserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
@permission_classes([IsAuthenticated])
def addbankaccount(request):
    bankaccounts = request.data
    if 'bank_name' not in bankaccounts: return Response({'data': {}, 'message': 'bank_name is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'branch_name' not in bankaccounts: return Response({'data': {}, 'message': 'branch_name is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'account_type' not in bankaccounts: return Response({'data': {}, 'message': 'account_type is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'account_no' not in bankaccounts: return Response({'data': {}, 'message': 'account_no is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'routing_no' not in bankaccounts: return Response({'data': {}, 'message': 'routing_no is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    bankaccountserializers = PSRLZER_CONT.Bankaccountserializer(data=request.data, many=False)
    if bankaccountserializers.is_valid():
        bankaccountserializers.save()
        return Response({'data': bankaccountserializers.data}, status=status.HTTP_201_CREATED)
