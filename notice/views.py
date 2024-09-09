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
from rest_framework.response import Response
from drf_nested_forms.utils import NestedForm
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
    noticeboardserializers = ghelp().getUsersWhoWillGetNotice(MODELS_BRAN.Branch, MODELS_DEPA.Department, MODELS_USER.User, SRLZER_NOTI.Noticeboardserializer, noticeboards)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': noticeboardserializers
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

    requestdata = dict(request.data)
    requestdata.update({'abcdef[abcdef]': ['abcdef']})
    options = {'allow_blank': True, 'allow_empty': False}
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)

    requestdata = ghelp().prepareData(form.data, 'noticeboard')

    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    allowed_fields = ['title', 'description', 'attachment', 'expiry_date']
    required_fields = ['title', 'description', 'expiry_date']
    fields_regex = [{'field': 'expiry_date', 'type': 'date'}]
    
    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
        classOBJ=MODELS_NOTI.Noticeboard, 
        Serializer=PSRLZER_NOTI.Noticeboardserializer, 
        data=requestdata, 
        allowed_fields=allowed_fields,
        extra_fields=extra_fields, 
        required_fields=required_fields,
        fields_regex=fields_regex
    )
    response_message = responsemessage
    response_status = responsestatus

    if responsesuccessflag == 'success':
        response_data = responsedata.data
        noticeid = response_data['id']
        if 'company' in requestdata:
            companys = requestdata['company']
            if isinstance(companys, list):
                if companys:
                    for companyid in companys:
                        prepare_data={'noticeboard': noticeid, 'company': companyid}
                        required_fields = ['noticeboard', 'company']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboardcompany, 
                            Serializer=PSRLZER_NOTI.Noticeboardcompanyserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,
                        )
                    response_successflag  = 'success'
        if 'branch' in requestdata:
            branchs = requestdata['branch']
            if isinstance(branchs, list):
                if branchs:
                    for branchid in branchs: 
                        prepare_data={'noticeboard': noticeid, 'branch': branchid}
                        required_fields = ['noticeboard', 'branch']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboardbranch, 
                            Serializer=PSRLZER_NOTI.Noticeboardbranchserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,
                        )
                    response_successflag  = 'success'
        if 'department' in requestdata:
            departments = requestdata['department']
            if isinstance(departments, list):
                if departments:
                    for departmentid in departments:
                        prepare_data={'noticeboard': noticeid, 'department': departmentid}
                        required_fields = ['noticeboard', 'department']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                            classOBJ=MODELS_NOTI.Noticeboarddepartment, 
                            Serializer=PSRLZER_NOTI.Noticeboarddepartmentserializer, 
                            data=prepare_data, 
                            required_fields=required_fields,

                        )
                    response_successflag  = 'success'
        if 'user' in requestdata:
            users = requestdata['user']
            if isinstance(users, list):
                for userid in users:
                    
                    prepare_data = {'noticeboard': noticeid, 'user': userid}
                    required_fields = ['noticeboard', 'user']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                        classOBJ=MODELS_NOTI.Noticeboardemployee, 
                        Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, 
                        data=prepare_data, 
                        required_fields=required_fields
                    )
                response_successflag  = 'success'
        else:
            for company in MODELS_COMP.Company.objects.all():
                prepare_data={'noticeboard': noticeid, 'company': company.id}
                required_fields = ['noticeboard', 'company']
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                    classOBJ=MODELS_NOTI.Noticeboardcompany, 
                    Serializer=PSRLZER_NOTI.Noticeboardcompanyserializer, 
                    data=prepare_data, 
                    required_fields=required_fields,
                )
            response_successflag  = 'success'
    elif responsesuccessflag == 'error':response_message.extend(responsemessage)
    
    return Response({'status': response_successflag, 'message': response_message, 'data': response_data}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatenoticeboard(request, noticeid=None):
    requestdata = dict(request.data)
    requestdata.update({'abcdef[abcdef]': ['abcdef']})
    options = {'allow_blank': True, 'allow_empty': False}
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)
    requestdata = ghelp().prepareData(form.data, 'noticeboard')
    
    allowed_fields=['title', 'description', 'attachment', 'expiry_date']
    fields_regex = [{'field': 'expiry_date', 'type': 'date'}]
    static_fields = ['attachment']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_NOTI.Noticeboard, 
        Serializer=PSRLZER_NOTI.Noticeboardserializer, 
        id=noticeid, 
        data=requestdata,
        allowed_fields=allowed_fields,
        fields_regex=fields_regex,
        static_fields=static_fields
    )
    if response_successflag == 'success':

        new_companyids = requestdata.get('company', [])
        if isinstance(new_companyids, list):
            previous_companyids = {}
            for each in MODELS_NOTI.Noticeboardcompany.objects.filter(noticeboard=noticeid): previous_companyids.update({str(each.company.id): each})
            
            add_companys = []
            remove_companys = []
            for companyid in new_companyids:
                if companyid not in previous_companyids: add_companys.append(companyid)
            for companyid in previous_companyids.keys():
                if companyid not in new_companyids: remove_companys.append(previous_companyids[companyid])

            for company in remove_companys: company.delete()
            for companyid in add_companys: ghelp().addtocolass(classOBJ=MODELS_NOTI.Noticeboardcompany, Serializer=PSRLZER_NOTI.Noticeboardcompanyserializer, data={'noticeboard': noticeid, 'company': companyid})

        new_branchids = requestdata.get('branch', [])
        if isinstance(new_branchids, list):
            previous_branchids = {}
            for each in MODELS_NOTI.Noticeboardbranch.objects.filter(noticeboard=noticeid): previous_branchids.update({str(each.branch.id): each})
            
            add_branchs = []
            remove_branchs = []
            for branchid in new_branchids:
                if branchid not in previous_branchids: add_branchs.append(branchid)
            for branchid in previous_branchids.keys():
                if branchid not in new_branchids: remove_branchs.append(previous_branchids[branchid])

            for branch in remove_branchs: branch.delete()
            for branchid in add_branchs: ghelp().addtocolass(classOBJ=MODELS_NOTI.Noticeboardbranch, Serializer=PSRLZER_NOTI.Noticeboardbranchserializer, data={'noticeboard': noticeid, 'branch': branchid})

        new_departmentids = requestdata.get('department', [])
        if isinstance(new_departmentids, list):
            previous_departmentids = {}
            for each in MODELS_NOTI.Noticeboarddepartment.objects.filter(noticeboard=noticeid): previous_departmentids.update({str(each.department.id): each})
            
            add_departments = []
            remove_departments = []
            for departmentid in new_departmentids:
                if departmentid not in previous_departmentids: add_departments.append(departmentid)
            for departmentid in previous_departmentids.keys():
                if departmentid not in new_departmentids: remove_departments.append(previous_departmentids[departmentid])

            for department in remove_departments: department.delete()
            for departmentid in add_departments: ghelp().addtocolass(classOBJ=MODELS_NOTI.Noticeboarddepartment, Serializer=PSRLZER_NOTI.Noticeboarddepartmentserializer, data={'noticeboard': noticeid, 'department': departmentid})

        new_userids = requestdata.get('user', [])
        if isinstance(new_userids, list):
            previous_userids = {}
            for each in MODELS_NOTI.Noticeboardemployee.objects.filter(noticeboard=noticeid): previous_userids.update({str(each.user.id): each})
            
            add_users = []
            remove_users = []
            for userid in new_userids:
                if userid not in previous_userids: add_users.append(userid)
            for userid in previous_userids.keys():
                if userid not in new_userids: remove_users.append(previous_userids[userid])

            for user in remove_users: user.delete()
            for userid in add_users: ghelp().addtocolass(classOBJ=MODELS_NOTI.Noticeboardemployee, Serializer=PSRLZER_NOTI.Noticeboardemployeeserializer, data={'noticeboard': noticeid, 'user': userid})

        response_data = ghelp().getUsersWhoWillGetNotice(MODELS_BRAN.Branch, MODELS_DEPA.Department, MODELS_USER.User, SRLZER_NOTI.Noticeboardserializer, response_data.instance, many=False)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletenoticeboard(request, noticeid=None):
    classOBJpackage_tocheck_assciaativity = [
        {'model': MODELS_NOTI.Noticeboardcompany, 'fields': [{'field': 'noticeboard', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_NOTI.Noticeboardbranch, 'fields': [{'field': 'noticeboard', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_NOTI.Noticeboarddepartment, 'fields': [{'field': 'noticeboard', 'relation': 'foreignkey', 'records': []}]},
        {'model': MODELS_NOTI.Noticeboardemployee, 'fields': [{'field': 'noticeboard', 'relation': 'foreignkey', 'records': []}]}
    ]
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_NOTI.Noticeboard,
        id=noticeid,
        classOBJpackage_tocheck_assciaativity=classOBJpackage_tocheck_assciaativity
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)