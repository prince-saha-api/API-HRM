from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from helps.common.generic import Generichelps as ghelp
from notice import models as MODELS_NOTI
from user import models as MODELS_USER
from branch import models as MODELS_BRAN
from company import models as MODELS_COMP
from department import models as MODELS_DEPA
from notice.serializer import serializers as SRLZER_NOTI
from notice.serializer.POST import serializers as PSRLZER_NOTI
from drf_nested_forms.utils import NestedForm
from rest_framework.response import Response
from rest_framework import status
import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getnoticeboards(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'reason__ititle'},
        {'name': 'description', 'convert': None, 'replace':'reason__idescription'},
        {'name': 'attachment', 'convert': None, 'replace':'attachment'},
        {'name': 'publish_date', 'convert': None, 'replace':'publish_date'},
        {'name': 'expiry_date', 'convert': None, 'replace':'expiry_date'},
    ]
    noticeboards = MODELS_NOTI.Noticeboard.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: noticeboards = noticeboards.order_by(column_accessor)

    total_count = noticeboards.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: noticeboards = noticeboards[(page-1)*page_size:page*page_size]

    noticeboardserializers = SRLZER_NOTI.Noticeboardserializer(noticeboards, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': noticeboardserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getnoticeboardcompanys(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'noticeboard', 'convert': None, 'replace':'noticeboard'},
        {'name': 'company', 'convert': None, 'replace':'company'},
    ]
    noticeboardcompanys = MODELS_NOTI.Noticeboardcompany.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: noticeboardcompanys = noticeboardcompanys.order_by(column_accessor)

    total_count = noticeboardcompanys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: noticeboardcompanys = noticeboardcompanys[(page-1)*page_size:page*page_size]

    noticeboardcompanyserializers = SRLZER_NOTI.Noticeboardcompanyserializer(noticeboardcompanys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': noticeboardcompanyserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getnoticeboardbranch(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'noticeboard', 'convert': None, 'replace':'noticeboard'},
        {'name': 'branch', 'convert': None, 'replace':'branch'},
    ]
    noticeboardbranchs = MODELS_NOTI.Noticeboardbranch.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: noticeboardbranchs = noticeboardbranchs.order_by(column_accessor)

    total_count = noticeboardbranchs.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: noticeboardbranchs = noticeboardbranchs[(page-1)*page_size:page*page_size]

    noticeboardbranchserializers = SRLZER_NOTI.Noticeboardbranchserializer(noticeboardbranchs, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': noticeboardbranchserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getnoticeboarddepartment(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'noticeboard', 'convert': None, 'replace':'noticeboard'},
        {'name': 'department', 'convert': None, 'replace':'department'},
    ]
    noticeboarddepartments = MODELS_NOTI.Noticeboarddepartment.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: noticeboarddepartments = noticeboarddepartments.order_by(column_accessor)

    total_count = noticeboarddepartments.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: noticeboarddepartments = noticeboarddepartments[(page-1)*page_size:page*page_size]

    noticeboarddepartmentserializers = SRLZER_NOTI.Noticeboarddepartmentserializer(noticeboarddepartments, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': noticeboarddepartmentserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getnoticeboardemployee(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'noticeboard', 'convert': None, 'replace':'noticeboard'},
        {'name': 'user', 'convert': None, 'replace':'user'},
    ]
    noticeboardemployees = MODELS_NOTI.Noticeboardemployee.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: noticeboardemployees = noticeboardemployees.order_by(column_accessor)

    total_count = noticeboardemployees.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: noticeboardemployees = noticeboardemployees[(page-1)*page_size:page*page_size]

    noticeboardemployeeserializers = SRLZER_NOTI.Noticeboardemployeeserializer(noticeboardemployees, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': noticeboardemployeeserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addnoticeboard(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    requestdata = request.data.copy()
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    unique_fields = []
    required_fields = ['title', 'description', 'publish_date', 'expiry_date']
    
    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
        classOBJ=MODELS_NOTI.Noticeboard, 
        Serializer=SRLZER_NOTI.Noticeboardserializer, 
        data=request.data, 
        extra_fields=extra_fields, 
        unique_fields=unique_fields, 
        required_fields=required_fields
    )
    response_message = responsemessage
    response_status = responsestatus
    if responsesuccessflag == 'success':
        response_data = responsedata.data.copy()
        noticeid = responsedata.instance.id
        if 'company' in requestdata:
            if isinstance(requestdata['company'], list):
                if requestdata['company']:
                    for companyid in requestdata['company']:
                        branchs = MODELS_BRAN.Branch.objects.filter(company=companyid)
                        if branchs.exists():
                            for branch in branchs:
                                departments = MODELS_DEPA.Department.objects.filter(branch=branch.id)
                                if departments.exists():
                                    for department in departments:
                                        users = department.user.all()
                                        for user in users:
                                            prepare_data = {'noticeboard': noticeid, 'user': user.id}
                                            required_fields = ['noticeboard', 'user']
                                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                                classOBJ=MODELS_NOTI.Noticeboardemployee, 
                                                Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                                                data=prepare_data, 
                                                required_fields=required_fields
                                            )

                        prepare_data=({'noticeboard': noticeid, 'company': companyid})
                        required_fields = ['noticeboard', 'company']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboardcompany, 
                            Serializer=PSRLZER_NOTI.Noticeboardcompanyserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,
                        )
                    response_successflag  = responsesuccessflag

        if 'branch' in requestdata:
            if isinstance(requestdata['branch'], list):
                if requestdata['branch']:
                    for branchid in requestdata['branch']: 
                        branch = MODELS_BRAN.Branch.objects.filter(id=branchid)
                        if branch.exists():
                            departments = MODELS_DEPA.Department.objects.filter(branch=branch.first().id)
                            for department in departments:
                                users = department.user.all()
                                for user in users:
                                    prepare_data = {'noticeboard': noticeid, 'user': user.id}
                                    required_fields = ['noticeboard', 'user']
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                        classOBJ=MODELS_NOTI.Noticeboardemployee, 
                                        Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                                        data=prepare_data, 
                                        required_fields=required_fields
                                    )
                        prepare_data=({'noticeboard': noticeid, 'branch': branchid})
                        required_fields = ['noticeboard', 'branch']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboardbranch, 
                            Serializer=PSRLZER_NOTI.Noticeboardbranchserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,

                        )
                    response_successflag  = responsesuccessflag

        if 'department' in requestdata:
            if isinstance(requestdata['department'], list):
                if requestdata['department']:
                    for departmentid in requestdata['department']:
                        department = MODELS_DEPA.Department.objects.filter(id=departmentid)
                        if department.exists():
                            users = department.first().user.all()
                            for user in users:
                                prepare_data = {'noticeboard': noticeid, 'user': user.id}
                                required_fields = ['noticeboard', 'user']
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                    classOBJ=MODELS_NOTI.Noticeboardemployee, 
                                    Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                                    data=prepare_data, 
                                    required_fields=required_fields
                                )
                        prepare_data=({'noticeboard': noticeid, 'department': departmentid})
                        required_fields = ['noticeboard', 'department']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboarddepartment, 
                            Serializer=PSRLZER_NOTI.Noticeboarddepartmentserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,

                        )
                    response_successflag  = responsesuccessflag

        if 'user' in requestdata:
            if isinstance(requestdata['user'], list):
                for userid in requestdata['user']:
                    
                    prepare_data = {'noticeboard': noticeid, 'user': userid}
                    required_fields = ['noticeboard', 'user']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_NOTI.Noticeboardemployee, 
                        Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                        data=prepare_data, 
                        required_fields=required_fields
                    )
                response_successflag  = responsesuccessflag
        else:
            for company in MODELS_COMP.Company.objects.all():
                branchs = MODELS_BRAN.Branch.objects.filter(company=company.id)
                if branchs.exists():
                    for branch in branchs:
                        departments = MODELS_DEPA.Department.objects.filter(branch=branch.id)
                        if departments.exists():
                            for department in departments:
                                users = department.user.all()
                                for user in users:
                                    prepare_data = {'noticeboard': noticeid, 'user': user.id}
                                    required_fields = ['noticeboard', 'user']
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                        classOBJ=MODELS_NOTI.Noticeboardemployee, 
                                        Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                                        data=prepare_data, 
                                        required_fields=required_fields
                                    )

                prepare_data=({'noticeboard': noticeid, 'company': company.id})
                required_fields = ['noticeboard', 'company']
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                    classOBJ=MODELS_NOTI.Noticeboardcompany, 
                    Serializer=PSRLZER_NOTI.Noticeboardcompanyserializer, 
                    data=prepare_data, 
                    required_fields=required_fields,
                )
            response_successflag  = responsesuccessflag
    return Response({'status': response_successflag, 'message': response_message, 'data': response_data}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatenoticeboard(request, noticeid=None):
    requestdata = request.data.copy()
    fields_regex = [
        {'field': 'publish_date', 'type': 'date', 'field': 'expiry_date', 'type': 'date'}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_NOTI.Noticeboard, 
        Serializer=SRLZER_NOTI.Noticeboardserializer, 
        id=noticeid, 
        data=request.data,
        fields_regex=fields_regex
    )
    if response_successflag == 'success':
        noticecompanys = MODELS_NOTI.Noticeboardcompany.objects.filter(noticeboard = noticeid) 
        for noticecompany in noticecompanys:
            response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
                classOBJ=MODELS_NOTI.Noticeboardcompany,
                id=noticecompany.id,
                )
        noticebranchs = MODELS_NOTI.Noticeboardbranch.objects.filter(noticeboard = noticeid) 
        for noticebranch in noticebranchs:
            response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
                classOBJ=MODELS_NOTI.Noticeboardbranch,
                id=noticebranch.id,
                )  
        noticedepartments = MODELS_NOTI.Noticeboarddepartment.objects.filter(noticeboard = noticeid) 
        for noticedepartment in noticedepartments:
            response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
                classOBJ=MODELS_NOTI.Noticeboarddepartment,
                id=noticedepartment.id,
                )  
        noticeemployees = MODELS_NOTI.Noticeboardemployee.objects.filter(noticeboard = noticeid) 
        for noticeemployee in noticeemployees:
            response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
                classOBJ=MODELS_NOTI.Noticeboardemployee,
                id=noticeemployee.id,
                )
    if response_successflag == 'success':    
        if 'company' in requestdata:
            if isinstance(requestdata['company'], list):
                if requestdata['company']:
                    for companyid in requestdata['company']:
                        branchs = MODELS_BRAN.Branch.objects.filter(company=companyid)
                        if branchs.exists():
                            for branch in branchs:
                                departments = MODELS_DEPA.Department.objects.filter(branch=branch.id)
                                if departments.exists():
                                    for department in departments:
                                        users = department.user.all()
                                        for user in users:
                                            prepare_data = {'noticeboard': noticeid, 'user': user.id}
                                            required_fields = ['noticeboard', 'user']
                                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                                classOBJ=MODELS_NOTI.Noticeboardemployee, 
                                                Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                                                data=prepare_data, 
                                                required_fields=required_fields
                                            )

                        prepare_data=({'noticeboard': noticeid, 'company': companyid})
                        required_fields = ['noticeboard', 'company']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboardcompany, 
                            Serializer=PSRLZER_NOTI.Noticeboardcompanyserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,
                        )
                    response_successflag  = responsesuccessflag
      
        if 'branch' in requestdata:
            if isinstance(requestdata['branch'], list):
                if requestdata['branch']:
                    for branchid in requestdata['branch']: 
                        branch = MODELS_BRAN.Branch.objects.filter(id=branchid)
                        if branch.exists():
                            departments = MODELS_DEPA.Department.objects.filter(branch=branch.first().id)
                            for department in departments:
                                users = department.user.all()
                                for user in users:
                                    prepare_data = {'noticeboard': noticeid, 'user': user.id}
                                    required_fields = ['noticeboard', 'user']
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                        classOBJ=MODELS_NOTI.Noticeboardemployee, 
                                        Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                                        data=prepare_data, 
                                        required_fields=required_fields
                                    )
                        prepare_data=({'noticeboard': noticeid, 'branch': branchid})
                        required_fields = ['noticeboard', 'branch']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboardbranch, 
                            Serializer=PSRLZER_NOTI.Noticeboardbranchserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,

                        )
                    response_successflag  = responsesuccessflag

        if 'department' in requestdata:
            if isinstance(requestdata['department'], list):
                if requestdata['department']:
                    for departmentid in requestdata['department']:
                        department = MODELS_DEPA.Department.objects.filter(id=departmentid)
                        if department.exists():
                            users = department.first().user.all()
                            for user in users:
                                prepare_data = {'noticeboard': noticeid, 'user': user.id}
                                required_fields = ['noticeboard', 'user']
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                    classOBJ=MODELS_NOTI.Noticeboardemployee, 
                                    Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                                    data=prepare_data, 
                                    required_fields=required_fields
                                )
                        prepare_data=({'noticeboard': noticeid, 'department': departmentid})
                        required_fields = ['noticeboard', 'department']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboarddepartment, 
                            Serializer=PSRLZER_NOTI.Noticeboarddepartmentserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,

                        )
                    response_successflag  = responsesuccessflag

        if 'user' in requestdata:
            if isinstance(requestdata['user'], list):
                for userid in requestdata['user']:
                    
                    prepare_data = {'noticeboard': noticeid, 'user': userid}
                    required_fields = ['noticeboard', 'user']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_NOTI.Noticeboardemployee, 
                        Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                        data=prepare_data, 
                        required_fields=required_fields
                    )
                response_successflag  = responsesuccessflag
        
        else:
            for company in MODELS_COMP.Company.objects.all():
                branchs = MODELS_BRAN.Branch.objects.filter(company=company.id)
                if branchs.exists():
                    for branch in branchs:
                        departments = MODELS_DEPA.Department.objects.filter(branch=branch.id)
                        if departments.exists():
                            for department in departments:
                                users = department.user.all()
                                for user in users:
                                    prepare_data = {'noticeboard': noticeid, 'user': user.id}
                                    required_fields = ['noticeboard', 'user']
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                        classOBJ=MODELS_NOTI.Noticeboardemployee, 
                                        Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                                        data=prepare_data, 
                                        required_fields=required_fields
                                    )

                prepare_data=({'noticeboard': noticeid, 'company': company.id})
                required_fields = ['noticeboard', 'company']
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                    classOBJ=MODELS_NOTI.Noticeboardcompany, 
                    Serializer=PSRLZER_NOTI.Noticeboardcompanyserializer, 
                    data=prepare_data, 
                    required_fields=required_fields,
                )
            response_successflag  = responsesuccessflag

    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletenoticeboard(request, noticeid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_NOTI.Noticeboard,
        id=noticeid,
        )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)