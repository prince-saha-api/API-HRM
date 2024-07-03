from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from officialoffday import models as MODELS_OFFI
from officialoffday.serializer import serializers as SRLZER_OFFI
from officialoffday.serializer.POST import serializers as PSRLZER_OFFI
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status
from helps.choice import common as CHOICE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getoffdays(request):
    filter_fields = [
                    {'name': 'id', 'convert': None, 'replace':'id'},
                    {'name': 'day', 'convert': None, 'replace':'day__icontains'},
                    {'name': 'is_active', 'convert': 'bool', 'replace':'is_active'},
                ]
    offdays = MODELS_OFFI.Offday.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: offdays = offdays.order_by(column_accessor)
    offdayserializers = SRLZER_OFFI.Offdayserializer(offdays, many=True)
    return Response({'status': 'success', 'message': '', 'data': offdayserializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addoffday(request):
    # userid = request.user.id
    extra_fields = {}
    unique_fields = ['day']
    required_fields = ['day']
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    choice_fields = [
        {'name': 'day', 'values': [item[1] for item in CHOICE.DAYS]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        MODELS_OFFI.Offday, 
        PSRLZER_OFFI.Offdayserializer, 
        request.data, 
        unique_fields=unique_fields, 
        extra_fields=extra_fields, 
        choice_fields=choice_fields, 
        required_fields=required_fields
        )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateoffday(request, offdayid=None):
    # userid = request.user.id
    extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        MODELS_OFFI.Offday,
        PSRLZER_OFFI.Offdayserializer,
        offdayid,
        request.data,
        extra_fields=extra_fields
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)