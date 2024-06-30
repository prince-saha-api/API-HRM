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
def addaddress(request):
    # userid = request.user.id
    required_fields = ['address', 'city', 'state_division', 'country']

    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_CONT.Address, 
        PSRLZER_CONT.Addressserializer, 
        request.data,
        required_fields=required_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateaddress(request, addressid=None):
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_CONT.Address, 
        PSRLZER_CONT.Addressserializer,
        addressid,
        request.data
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteaddress(request, addressid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_BRAN.Branch, 'fields': ['address']},
        {'model': MODELS_COMP.Basicinformation, 'fields': ['address']},
        {'model': MODELS_COMP.Company, 'fields': ['address']},
        {'model': MODELS_CONT.Bankaccount, 'fields': ['address']},
        {'model': MODELS_DEPA.Department, 'fields': ['address']},
        {'model': MODELS_USER.User, 'fields': ['present_address', 'permanent_address']},
        {'model': MODELS_USER.Employeecontact, 'fields': ['address']},
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(MODELS_CONT.Address, classOBJpackage_tocheck_assciaativity, addressid)
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
        MODELS_CONT.Bankaccounttype,
        PSRLZER_CONT.Bankaccounttypeserializer,
        request.data,
        unique_fields=unique_fields,
        required_fields=required_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatebankaccounttype(request, bankaccounttypeid=None):
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_CONT.Bankaccounttype, 
        PSRLZER_CONT.Bankaccounttypeserializer,
        bankaccounttypeid,
        request.data
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletebankaccounttype(request, bankaccounttypeid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_CONT.Bankaccount, 'fields': ['account_type']}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(MODELS_CONT.Bankaccounttype, classOBJpackage_tocheck_assciaativity, bankaccounttypeid)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getbankaccounts(request):
    bankaccounts = MODELS_CONT.Bankaccount.objects.all()
    bankaccountserializers = SRLZER_CONT.Bankaccountserializer(bankaccounts, many=True)
    return Response(bankaccountserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
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
