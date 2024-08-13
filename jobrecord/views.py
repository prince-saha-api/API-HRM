# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from jobrecord import models as MODELS_JOBR
from user import models as MODELS_USER
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN
from department import models as MODELS_DEPA
from hrm_settings import models as MODELS_SETT
from jobrecord.serializer import serializers as SRLZER_JOBR
from jobrecord.serializer.POST import serializers as PSRLZER_JOBR
from rest_framework.response import Response
from rest_framework import status
from helps.common.generic import Generichelps as ghelp
from helps.choice import common as CHOICE


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getjobhistorys(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'effective_from', 'convert': None, 'replace':'effective_from'},
        {'name': 'increment_on', 'convert': None, 'replace':'increment_on__icontains'},
        {'name': 'salary', 'convert': None, 'replace':'salary'},
        {'name': 'increment_amount', 'convert': None, 'replace':'increment_amount'},
        {'name': 'percentage', 'convert': None, 'replace':'percentage'},
        {'name': 'company', 'convert': None, 'replace':'company'},
        {'name': 'branch', 'convert': None, 'replace':'branch'},
        {'name': 'department', 'convert': None, 'replace':'department'},
        {'name': 'designation', 'convert': None, 'replace':'designation'},
        {'name': 'employee_type', 'convert': None, 'replace':'employee_type'},
        {'name': 'date', 'convert': None, 'replace':'date'},
        {'name': 'status_adjustment', 'convert': None, 'replace':'status_adjustment__icontains'},
        {'name': 'appraisal_by', 'convert': None, 'replace':'appraisal_by'},
        {'name': 'comment', 'convert': None, 'replace':'comment__icontains'}
    ]
    employeejobhistorys = MODELS_JOBR.Employeejobhistory.objects.filter(**ghelp().KWARGS(request, filter_fields))
    column_accessor = request.GET.get('column_accessor')
    if column_accessor: employeejobhistorys = employeejobhistorys.order_by(column_accessor)

    total_count = employeejobhistorys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: employeejobhistorys = employeejobhistorys[(page-1)*page_size:page*page_size]

    employeejobhistoryserializers = SRLZER_JOBR.Employeejobhistoryserializer(employeejobhistorys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': employeejobhistoryserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addjobhistory(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST
    
    requestdata = request.data.copy()
    if requestdata.get('user'):
        user = MODELS_USER.User.objects.filter(id=requestdata.get('user'))
        if user.exists():

            generalsettings = None
            salary = requestdata.get('salary')
            if salary:
                try:
                    salary = float(salary)
                    generalsettings = ghelp().findGeneralsettings(MODELS_SETT.Generalsettings)
                    if generalsettings:
                        if generalsettings.basic_salary_percentage == None: response_message.append('basic_salary_percentage is missing in generalsettings!')
                    else: response_message.append('generalsettings is missing!')
                except: pass

            if not response_message:
                previous_employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(user=user.first().id)
                if previous_employeejobhistory.exists():
                    previous_employeejobhistory = previous_employeejobhistory.order_by('id').last()
                    
                    employeejobhistorydata = {'user': user.first().id, 'appraisal_by': request.user.id}
                    if requestdata.get('effective_from'): employeejobhistorydata.update({'effective_from': requestdata.get('effective_from')})
                    if requestdata.get('increment_on'): employeejobhistorydata.update({'increment_on': requestdata.get('increment_on')})
                    
                    prev_salary = previous_employeejobhistory.salary
                    if prev_salary:
                        if not isinstance(salary, float): salary = prev_salary
                        employeejobhistorydata.update({'salary': f'{salary}'})

                        increment_amount = salary - prev_salary
                        employeejobhistorydata.update({'increment_amount': f'{increment_amount}'})
                        percentage = (increment_amount*100)/prev_salary
                        employeejobhistorydata.update({'percentage': f'{percentage}'})

                    if requestdata.get('employee_type'): employeejobhistorydata.update({'employee_type': requestdata.get('employee_type')})
                    if requestdata.get('date'): employeejobhistorydata.update({'date': requestdata.get('date')})
                    
                    if requestdata.get('status_adjustment'): employeejobhistorydata.update({'status_adjustment': requestdata.get('status_adjustment')})

                    companyid = requestdata.get('company')
                    if companyid:
                        company = MODELS_COMP.Company.objects.filter(id=companyid)
                        if company.exists():
                            companyid = company.first().id
                            employeejobhistorydata.update({'company': companyid})
                        else:
                            if previous_employeejobhistory.company:
                                companyid = previous_employeejobhistory.company.id
                                employeejobhistorydata.update({'company': companyid})
                            else: companyid = None
                    else:
                        if previous_employeejobhistory.company:
                            companyid = previous_employeejobhistory.company.id
                            employeejobhistorydata.update({'company': companyid})
                        else: companyid = None
                    
                    branchid = None
                    if companyid:
                        branchid = requestdata.get('branch')
                        if branchid:
                            branch = MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid)
                            if branch.exists():
                                branchid = branch.first().id
                                employeejobhistorydata.update({'branch': branchid})
                            else:
                                if previous_employeejobhistory.branch:
                                    branchid = previous_employeejobhistory.branch.id
                                    employeejobhistorydata.update({'branch': branchid})
                                else: branchid = None
                        else:
                            if previous_employeejobhistory.branch:
                                branchid = previous_employeejobhistory.branch.id
                                employeejobhistorydata.update({'branch': branchid})
                            else: branchid = None

                    departmentid = None
                    if branchid:
                        departmentid = requestdata.get('department')
                        if departmentid:
                            department = MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid)
                            if department.exists():
                                departmentid = department.first().id
                                employeejobhistorydata.update({'department': departmentid})
                            else:
                                if previous_employeejobhistory.department:
                                    departmentid = previous_employeejobhistory.department.id
                                    employeejobhistorydata.update({'department': departmentid})
                                else: departmentid = None
                        else:
                            if previous_employeejobhistory.department:
                                departmentid = previous_employeejobhistory.department.id
                                employeejobhistorydata.update({'department': departmentid})
                            else: departmentid = None

                    designation = requestdata.get('designation')
                    if designation:
                        designation = MODELS_USER.Designation.objects.filter(id=designation)
                        if designation.exists():
                            employeejobhistorydata.update({'designation': designation.first().id})
                        else:
                            if previous_employeejobhistory.designation:
                                employeejobhistorydata.update({'designation': previous_employeejobhistory.designation.id})
                    else:
                        if previous_employeejobhistory.designation:
                            employeejobhistorydata.update({'designation': previous_employeejobhistory.designation.id})
                    
                    if employeejobhistorydata:
                        allowed_fields = ['user', 'effective_from', 'increment_on', 'salary', 'increment_amount', 'percentage', 'employee_type', 'date', 'status_adjustment', 'company', 'branch', 'department', 'designation', 'comment', 'doc', 'appraisal_by']
                        required_fields = ['user', 'effective_from', 'salary', 'increment_amount', 'percentage', 'employee_type', 'date', 'status_adjustment', 'company', 'branch', 'department', 'designation']
                        choice_fields = [
                            {'name': 'increment_on', 'values': [item[1] for item in CHOICE.INCREMENT_ON]},
                            {'name': 'status_adjustment', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]},
                            {'name': 'employee_type', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
                        ]
                        fields_regex = [
                            {'field': 'effective_from', 'type': 'date'},
                            {'field': 'date', 'type': 'date'}
                        ]
                        response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
                            classOBJ=MODELS_JOBR.Employeejobhistory,
                            Serializer=PSRLZER_JOBR.Employeejobhistoryserializer,
                            data=employeejobhistorydata,
                            allowed_fields=allowed_fields,
                            required_fields=required_fields,
                            choice_fields=choice_fields,
                            fields_regex=fields_regex
                        )
                        if response_data:
                            instance = response_data.instance
                            if instance.salary == user.first().gross_salary: user.update(designation=instance.designation)
                            else:
                                gross_salary = instance.salary
                                basic_salary_percentage = generalsettings.basic_salary_percentage
                                basic_salary = (basic_salary_percentage*gross_salary)/100
                                user.update(designation=instance.designation, gross_salary=gross_salary, basic_salary=basic_salary)
                            response_data = response_data.data

                else: response_message.append('last employeejobhistory doesn\'t exist!')
        else: response_message.append('user doesn\'t exist!')
    else: response_message.append('user id is missing!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def updatejobhistory(request, jobhistoryid=None):
#     response_data = {}
#     response_message = []
#     response_successflag = 'error'
#     response_status = status.HTTP_400_BAD_REQUEST
    
#     requestdata = request.data.copy()
#     user = MODELS_USER.User.objects.filter(id=requestdata.get('user'))

#     previous_employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(user=user.first().id)
#     if previous_employeejobhistory.exists():
#         previous_employeejobhistory = previous_employeejobhistory.order_by('id').last()
        
#         employeejobhistorydata = {'user': user.first().id, 'appraisal_by': request.user.id}
#         if requestdata.get('effective_from'): employeejobhistorydata.update({'effective_from': requestdata.get('effective_from')})
#         if requestdata.get('increment_on'): employeejobhistorydata.update({'increment_on': requestdata.get('increment_on')})
        
#         prev_salary = previous_employeejobhistory.salary
#         if prev_salary:
#             employeejobhistorydata.update({'prev_salary': f'{prev_salary}'})

#             salary = requestdata.get('salary')
#             if salary:
#                 try:
#                     salary = float(salary)
#                     employeejobhistorydata.update({'salary': f'{salary}'})
#                     if salary > prev_salary:
#                         increment_amount = salary - prev_salary
#                         employeejobhistorydata.update({'increment_amount': f'{increment_amount}'})
#                         percentage = (increment_amount*100)/prev_salary
#                         employeejobhistorydata.update({'percentage': f'{percentage}'})
#                 except: pass

#         if requestdata.get('employee_type'): employeejobhistorydata.update({'employee_type': requestdata.get('employee_type')})


#         from_date = requestdata.get('from_date')
#         if from_date:
#             employeejobhistorydata.update({'from_date': f'{from_date}'})
#             previous_employeejobhistory.to_date = from_date
#             previous_employeejobhistory.save()
        
#         if requestdata.get('status_adjustment'): employeejobhistorydata.update({'status_adjustment': requestdata.get('status_adjustment')})

#         companyid = requestdata.get('company')
#         if companyid:
#             company = MODELS_COMP.Company.objects.filter(id=companyid)
#             if company.exists():
#                 companyid = company.first().id
#                 employeejobhistorydata.update({'company': companyid})
#             else:
#                 if previous_employeejobhistory.company:
#                     companyid = previous_employeejobhistory.company.id
#                     employeejobhistorydata.update({'company': companyid})
#                 else: companyid = None
#         else:
#             if previous_employeejobhistory.company:
#                 companyid = previous_employeejobhistory.company.id
#                 employeejobhistorydata.update({'company': companyid})
#             else: companyid = None
        
#         branchid = None
#         if companyid:
#             branchid = requestdata.get('branch')
#             if branchid:
#                 branch = MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid)
#                 if branch.exists():
#                     branchid = branch.first().id
#                     employeejobhistorydata.update({'branch': branchid})
#                 else:
#                     if previous_employeejobhistory.branch:
#                         branchid = previous_employeejobhistory.branch.id
#                         employeejobhistorydata.update({'branch': branchid})
#                     else: branchid = None
#             else:
#                 if previous_employeejobhistory.branch:
#                     branchid = previous_employeejobhistory.branch.id
#                     employeejobhistorydata.update({'branch': branchid})
#                 else: branchid = None

#         departmentid = None
#         if branchid:
#             departmentid = requestdata.get('department')
#             if departmentid:
#                 department = MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid)
#                 if department.exists():
#                     departmentid = department.first().id
#                     employeejobhistorydata.update({'department': departmentid})
#                 else:
#                     if previous_employeejobhistory.department:
#                         departmentid = previous_employeejobhistory.department.id
#                         employeejobhistorydata.update({'department': departmentid})
#                     else: departmentid = None
#             else:
#                 if previous_employeejobhistory.department:
#                     departmentid = previous_employeejobhistory.department.id
#                     employeejobhistorydata.update({'department': departmentid})
#                 else: departmentid = None

#         designation = requestdata.get('designation')
#         if designation:
#             designation = MODELS_USER.Designation.objects.filter(id=designation)
#             if designation.exists():
#                 employeejobhistorydata.update({'designation': designation.first().id})
#             else:
#                 if previous_employeejobhistory.designation:
#                     employeejobhistorydata.update({'designation': previous_employeejobhistory.designation.id})
#         else:
#             if previous_employeejobhistory.designation:
#                 employeejobhistorydata.update({'designation': previous_employeejobhistory.designation.id})

#         # user, effective_from, increment_on, new_salary, increment_amount, percentage, employee_type, from_date, status_adjustment
#         # prev_salary, company, branch, department, designation
        
#         if employeejobhistorydata:
#             allowed_fields = ['user', 'effective_from', 'increment_on', 'prev_salary', 'salary', 'increment_amount', 'percentage', 'employee_type', 'from_date', 'status_adjustment', 'company', 'branch', 'department', 'designation', 'comment', 'doc', 'appraisal_by']
#             required_fields = ['user', 'effective_from', 'increment_on', 'prev_salary', 'salary', 'increment_amount', 'percentage', 'employee_type', 'from_date', 'status_adjustment', 'company', 'branch', 'department', 'designation']
#             choice_fields = [
#                 {'name': 'increment_on', 'values': [item[1] for item in CHOICE.INCREMENT_ON]},
#                 {'name': 'status_adjustment', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]},
#                 {'name': 'employee_type', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
#             ]
#             fields_regex = [
#                 {'field': 'effective_from', 'type': 'date'},
#                 {'field': 'from_date', 'type': 'date'},
#                 {'field': 'to_date', 'type': 'date'},
#             ]
#             response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
#                 classOBJ=MODELS_JOBR.Employeejobhistory,
#                 Serializer=PSRLZER_JOBR.Employeejobhistoryserializer,
#                 data=employeejobhistorydata,
#                 allowed_fields=allowed_fields,
#                 required_fields=required_fields,
#                 choice_fields=choice_fields,
#                 fields_regex=fields_regex
#             )
#             if response_data:
#                 user.update(designation=response_data.instance.designation)
#                 response_data = response_data.data

#     else: response_message.append('last employeejobhistory doesn\'t exist!')
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletejobhistory(request, jobhistoryid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST
    
    generalsettings = ghelp().findGeneralsettings(MODELS_SETT.Generalsettings)
    
    if generalsettings:
        if generalsettings.basic_salary_percentage:
            employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(id=jobhistoryid)
            if employeejobhistory.exists():
                user = employeejobhistory.first().user
                employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(user=user.id).order_by('id')
                if employeejobhistory.first().id != jobhistoryid:
                    if employeejobhistory.last().id == jobhistoryid:
                        
                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().deleterecord(
                            classOBJ=MODELS_JOBR.Employeejobhistory,
                            id=jobhistoryid
                        )
                        if responsesuccessflag == 'success':
                            last_employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(user=user.id).order_by('id').last()
                            gross_salary = last_employeejobhistory.salary
                            basic_salary_percentage = generalsettings.basic_salary_percentage
                            basic_salary = (basic_salary_percentage*gross_salary)/100
                            
                            user.designation = last_employeejobhistory.designation
                            user.gross_salary = gross_salary
                            user.basic_salary = basic_salary
                            user.save()
                            response_successflag = responsesuccessflag
                            response_status = responsestatus
                    else: response_message.append('only last record is eligible to delete!')
                else: response_message.append('first record can\'t be deleted!')
            else: response_message.append('record doesn\'t exist!')
        else : response_message.append('basic_salary_percentage is missing in generalsettings!')
    else: response_message.append('generalsettings doesn\'t exist!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)