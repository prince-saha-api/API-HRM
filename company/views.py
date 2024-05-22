from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from company import models as MODELS_COMP
from company.serializer import serializers as SRLZER_COMP
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getcompanys(request):
    companys = MODELS_COMP.Company.objects.all()
    companyserializers = SRLZER_COMP.Companyserializer(companys, many=True)
    return Response(companyserializers.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def addcompany(request):
#     companyserializers = SRLZER_COMP.Companyserializer(data=request.data, many=False)
#     if companyserializers.is_valid():
#         companyserializers.save()
#         return Response({'status': 'success', 'message': '', 'data': companyserializers.data}, status=status.HTTP_201_CREATED)
#     else: return Response({'status': 'error', 'message': '', 'data': companyserializers.errors}, status=status.HTTP_400_BAD_REQUEST)

