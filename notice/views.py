from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from helps.common.generic import Generichelps as ghelp
from notice import models as MODELS_NOTI
from notice.serializer import serializers as SRLZER_NOTI
from rest_framework.response import Response
from rest_framework import status
import random

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getnoticeboard(request):

    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'},
        {'name': 'description', 'convert': None, 'replace':'description__icontains'},
        {'name': 'publish_date', 'convert': None, 'replace':'publish_date'},
        {'name': 'expiry_date', 'convert': None, 'replace':'expiry_date'},
        {'name': 'branch', 'convert': None, 'replace':'branch__icontains'},
        
    ]
    noteboards = MODELS_NOTI.Noteboard.objects.filter(**ghelp().KWARGS(request, filter_fields))
    # filter_fields = [
    #     {'name': 'id', 'convert': None, 'replace':'id'},
    #     {'name': 'branch', 'convert': None, 'replace':'branch__icontains'},
        
    # ]
    noteboards = MODELS_NOTI.Noteboard.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: noteboards = noteboards.order_by(column_accessor)
    
    total_count = noteboards.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: noteboards = noteboards[(page-1)*page_size:page*page_size]

    noteboardserializer = SRLZER_NOTI.Noteboardserializer(noteboards, many=True)
    chars = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']]
    for userserializer in noteboardserializer.data:
        if userserializer['hr_password']:
            splitpassword = [int(each)-78 for each in noteboardserializer['hr_password'].split('-')]
            password = ''
            for value in splitpassword:
                ran_number = random.randint(0, 25)
                ch = chars[ran_number%2][ran_number]
                password += ch+chr(value)+str(ord(ch))
            userserializer['hr_password'] = password

    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': noteboardserializer.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)