# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from jobrecord import models as MODELS_JOBR
from user import models as MODELS_USER
from company import models as MODELS_COMP
from branch import models as MODELS_BRAN
from department import models as MODELS_DEPA
from hrm_settings import models as MODELS_SETT
from jobrecord.serializer.CUSTOM import serializers as CSRLZER_JOBR
from jobrecord.serializer.POST import serializers as PSRLZER_JOBR
from user.serializer.POST import serializers as PSRLZER_USER
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

    employeejobhistoryserializers = CSRLZER_JOBR.Employeejobhistoryserializer(employeejobhistorys, many=True)
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
            if user.first().job_status == CHOICE.JOB_STATUS[0][1]:
                previous_employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(user=user.first().id)
                if previous_employeejobhistory.exists():
                    previous_employeejobhistory = previous_employeejobhistory.order_by('id').last()

                    userdatatoupdate = {}
                    employeejobhistorydata = {}
                    allowed_fields = ['user', 'effective_from', 'status_adjustment', 'appraisal_by', 'comment', 'doc']
                    required_fields = ['user', 'effective_from', 'status_adjustment', 'appraisal_by']
                    choice_fields = []
                    fields_regex = [{'field': 'effective_from', 'type': 'date'}]
                    
                    employeejobhistorydata.update({'user': requestdata.get('user'), 'appraisal_by': request.user.id})

                    effective_from = requestdata.get('effective_from')
                    if effective_from: employeejobhistorydata.update({'effective_from': effective_from})

                    comment = requestdata.get('comment')
                    if effective_from: employeejobhistorydata.update({'comment': comment})

                    doc = request.FILES.get('doc')
                    if doc: employeejobhistorydata.update({'doc': doc})

                    status_adjustment = requestdata.get('status_adjustment')
                    if status_adjustment:
                        if isinstance(status_adjustment, str):
                            status_adjustment = status_adjustment.replace(', ', '-').replace('[', '').replace(']', '').split('-')
                        
                        if status_adjustment:
                            employeejobhistorydata.update({'status_adjustment': status_adjustment})
                            choice_fields.append({'name': 'status_adjustment', 'type': 'list-string', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]})
                            if_anyone_checked = False

                            
                            if CHOICE.STATUS_ADJUSTMENT[1][1] in status_adjustment: # Promotion
                                if_anyone_checked = True
                                allowed_fields.extend(['designation'])
                                required_fields.extend(['designation'])
                                
                                designation = requestdata.get('designation')
                                if designation:
                                    employeejobhistorydata.update({'designation': designation})
                                    userdatatoupdate.update({'designation': designation})
                            # else:
                            #     if previous_employeejobhistory.designation:
                            #         allowed_fields.extend(['designation'])
                            #         required_fields.extend(['designation'])
                            #         employeejobhistorydata.update({'designation': previous_employeejobhistory.designation.id})

                            if CHOICE.STATUS_ADJUSTMENT[2][1] in status_adjustment: # Increment
                                if_anyone_checked = True
                                
                                allowed_fields.extend(['increment_on', 'salary', 'increment_amount', 'percentage'])
                                required_fields.extend(['increment_on', 'salary', 'increment_amount', 'percentage'])

                                increment_on = requestdata.get('increment_on')
                                if increment_on: employeejobhistorydata.update({'increment_on': increment_on})

                                salary = requestdata.get('salary')
                                if salary:
                                    try:
                                        salary = float(salary)
                                        basic_salary_response = ghelp().getBasicSalary(MODELS_SETT.Generalsettings, salary)
                                        if basic_salary_response['flag']:
                                            employeejobhistorydata.update({'salary': salary})
                                            userdatatoupdate.update({'gross_salary': salary, 'basic_salary': basic_salary_response['basic_salary']})
                                    except: pass

                                percentage = requestdata.get('percentage')
                                if percentage: employeejobhistorydata.update({'percentage': percentage})
                                
                                increment_amount = requestdata.get('increment_amount')
                                if increment_amount: employeejobhistorydata.update({'increment_amount': increment_amount})
                            # else:
                            #     allowed_fields.extend(['increment_on', 'salary', 'increment_amount', 'percentage'])
                            #     if previous_employeejobhistory.increment_on:
                            #         employeejobhistorydata.update({'increment_on': previous_employeejobhistory.increment_on})
                            #     if previous_employeejobhistory.salary:
                            #         employeejobhistorydata.update({'salary': previous_employeejobhistory.salary})
                            #     if previous_employeejobhistory.percentage:
                            #         employeejobhistorydata.update({'percentage': previous_employeejobhistory.percentage})
                            #     if previous_employeejobhistory.increment_amount:
                            #         employeejobhistorydata.update({'increment_amount': previous_employeejobhistory.increment_amount})

                            departmentid = None
                            if CHOICE.STATUS_ADJUSTMENT[3][1] in status_adjustment: # Transfer
                                if_anyone_checked = True
                                allowed_fields.extend(['company', 'branch', 'department'])
                                required_fields.extend(['company', 'branch', 'department'])

                                companyid = requestdata.get('company')
                                if companyid:
                                    company = MODELS_COMP.Company.objects.filter(id=companyid)
                                    if company.exists():
                                        companyid = company.first().id
                                        employeejobhistorydata.update({'company': companyid, 'branch': None, 'department': None})
                                    else:
                                        if previous_employeejobhistory.company:
                                            companyid = previous_employeejobhistory.company.id
                                            employeejobhistorydata.update({'company': companyid, 'branch': None, 'department': None})
                                        else: companyid = None
                                else:
                                    if previous_employeejobhistory.company:
                                        companyid = previous_employeejobhistory.company.id
                                        employeejobhistorydata.update({'company': companyid, 'branch': None, 'department': None})
                                    else: companyid = None
                                
                                branchid = None
                                if companyid:
                                    branchid = requestdata.get('branch')
                                    if branchid:
                                        branch = MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid)
                                        if branch.exists():
                                            branchid = branch.first().id
                                            employeejobhistorydata.update({'branch': branchid, 'department': None})
                                        else:
                                            if previous_employeejobhistory.branch:
                                                branchid = previous_employeejobhistory.branch.id
                                                if MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid).exists():
                                                    employeejobhistorydata.update({'branch': branchid, 'department': None})
                                                else: branchid = None
                                            else: branchid = None
                                    else:
                                        if previous_employeejobhistory.branch:
                                            branchid = previous_employeejobhistory.branch.id
                                            if MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid).exists():
                                                employeejobhistorydata.update({'branch': branchid, 'department': None})
                                            else: branchid = None
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
                                                if MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid).exists():
                                                    employeejobhistorydata.update({'department': departmentid})
                                                else: departmentid = None
                                            else: departmentid = None
                                    else:
                                        if previous_employeejobhistory.department:
                                            departmentid = previous_employeejobhistory.department.id
                                            if MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid).exists():
                                                employeejobhistorydata.update({'department': departmentid})
                                            else: departmentid = None
                                        else: departmentid = None
                            # else:
                            #     allowed_fields.extend(['company', 'branch', 'department'])
                            #     if previous_employeejobhistory.company:
                            #         employeejobhistorydata.update({'company': previous_employeejobhistory.company.id})
                            #     if previous_employeejobhistory.branch:
                            #         employeejobhistorydata.update({'branch': previous_employeejobhistory.branch.id})
                            #     if previous_employeejobhistory.department:
                            #         employeejobhistorydata.update({'department': previous_employeejobhistory.department.id})

                            if CHOICE.STATUS_ADJUSTMENT[4][1] in status_adjustment: # Status Update
                                employee_type = requestdata.get('employee_type')
                                if employee_type:
                                    allowed_fields.append('employee_type')
                                    required_fields.append('employee_type')
                                    choice_fields.append({'name': 'employee_type', 'type': 'single-string', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]})

                                    employeejobhistorydata.update({'employee_type': employee_type})
                                    userdatatoupdate.update({'employee_type': employee_type})
                                
                                # current job status will hold both user and employee transition table

                                if not if_anyone_checked:
                                    job_status = requestdata.get('job_status')
                                    if job_status:
                                        allowed_fields.append('job_status')
                                        required_fields.append('job_status')
                                        choice_fields.append({'name': 'job_status', 'type': 'single-string', 'values': [item[1] for item in CHOICE.JOB_STATUS]})
                                        employeejobhistorydata.update({'job_status': job_status})
                                        userdatatoupdate.update({'job_status': job_status})
                                        if job_status in [CHOICE.JOB_STATUS[1][1], CHOICE.JOB_STATUS[2][1], CHOICE.JOB_STATUS[3][1]]:
                                            userdatatoupdate.update({'is_active': False})
                                            employeejobhistorydata.update({'status_adjustment': [job_status]})
                            # else:
                            #     allowed_fields.extend(['employee_type', 'job_status'])
                            #     if previous_employeejobhistory.employee_type:
                            #         employeejobhistorydata.update({'employee_type': previous_employeejobhistory.employee_type})
                            #     if previous_employeejobhistory.job_status:
                            #         employeejobhistorydata.update({'job_status': previous_employeejobhistory.job_status})

                            extra_fields = {'previous_id': previous_employeejobhistory.id}
                            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                classOBJ=MODELS_JOBR.Employeejobhistory,
                                Serializer=PSRLZER_JOBR.Employeejobhistoryserializer,
                                data=employeejobhistorydata,
                                allowed_fields=allowed_fields,
                                required_fields=required_fields,
                                choice_fields=choice_fields,
                                fields_regex=fields_regex,
                                extra_fields=extra_fields
                            )
                            if responsesuccessflag == 'success':
                                instance = responsedata.instance
                                MODELS_JOBR.Employeejobhistory.objects.filter(id=previous_employeejobhistory.id).update(next_id=instance.id)

                                if departmentid:
                                    if previous_employeejobhistory.department.id != departmentid:
                                        previous_employeejobhistory.department.user.remove(user.first())
                                        responsedata.instance.department.user.add(user.first())
                                else:
                                    if previous_employeejobhistory.department:
                                        previous_employeejobhistory.department.user.remove(user.first())
                                
                                response_data = responsedata.data
                                response_status = responsestatus
                                response_successflag = responsesuccessflag

                                ghelp().updaterecord(
                                    classOBJ=MODELS_USER.User,
                                    Serializer=PSRLZER_USER.Userserializer,
                                    id=user.first().id,
                                    data=userdatatoupdate
                                )
                            elif responsesuccessflag == 'error': response_message.extend(responsemessage)
                            response_status = responsestatus
                            response_successflag = responsesuccessflag
                        else: response_message.append('no valid status_adjustment provided!')
                    else: response_message.append('please select status_adjustment!')
                else: response_message.append('last employeejobhistory doesn\'t exist!')
            else: response_message.append(f'user is already {user.first().job_status}!')
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
#     preparedata = {}
#     employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(id=jobhistoryid)
#     if employeejobhistory.exists():
#         user = employeejobhistory.first().user
#         _department = employeejobhistory.first().department
        
#         effective_from = requestdata.get('effective_from')
#         if effective_from: preparedata.update({'effective_from': effective_from})

#         increment_on = requestdata.get('increment_on')
#         if increment_on: preparedata.update({'increment_on': increment_on})

#         salary = requestdata.get('salary')
#         if salary:
#             try:
#                 salary = float(salary)
#                 preparedata.update({'salary': salary})
#             except: pass

#         # just update, no effect(if last record)
#         company = requestdata.get('company')
#         if company: preparedata.update({'company': company})

#         # just update, no effect(if last record)
#         branch = requestdata.get('branch')
#         if branch: preparedata.update({'branch': branch})
        
#         # just update, no effect(if last record) 
#         department = requestdata.get('department')
#         if department: preparedata.update({'department': department})

#         # just update, no effect(if last record) 
#         designation = requestdata.get('designation')
#         if designation: preparedata.update({'designation': designation})

#         # just update, no effect(if last record) 
#         employee_type = requestdata.get('employee_type')
#         if employee_type: preparedata.update({'employee_type': employee_type})

#         date = requestdata.get('date')
#         if date: preparedata.update({'date': date})

#         status_adjustment = requestdata.get('status_adjustment')
#         if status_adjustment: preparedata.update({'status_adjustment': status_adjustment})

#         comment = requestdata.get('comment')
#         if comment: preparedata.update({'comment': comment})

#         static_fields = []
#         doc = request.FILES.get('doc')
#         if doc:
#             preparedata.update({'doc': doc})
#             static_fields.append('doc')

#         previous_id = employeejobhistory.first().previous_id
#         next_id = employeejobhistory.first().next_id
        
#         if previous_id:
#             previous_employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(id=previous_id)
#             if previous_employeejobhistory.exists():
#                 if salary:
#                     previous_salary = previous_employeejobhistory.first().salary
#                     increment_amount = salary - previous_salary
#                     percentage = increment_amount/100

#                     preparedata.update({'increment_amount': increment_amount})
#                     preparedata.update({'percentage': percentage})
                    
#                 if next_id:
#                     next_employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(id=next_id)
#                     if next_employeejobhistory.exists():
#                         if salary:
#                             next_salary = next_employeejobhistory.first().salary
#                             increment_amount = next_salary - salary
#                             percentage = increment_amount/100
#                             next_employeejobhistory.update(increment_amount=increment_amount, percentage=percentage)
                        
#                         choice_fields = [
#                             {'name': 'increment_on', 'type': 'single-string', 'values': [item[1] for item in CHOICE.INCREMENT_ON]},
#                             {'name': 'employee_type', 'type': 'single-string', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
#                             {'name': 'status_adjustment', 'type': 'single-string', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]}
#                         ]
#                         fields_regex = [
#                             {'field': 'effective_from', 'type': 'date'},
#                             {'field': 'date', 'type': 'date'}
#                         ]

#                         responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
#                             classOBJ=MODELS_JOBR.Employeejobhistory, 
#                             Serializer=PSRLZER_JOBR.Employeejobhistoryserializer, 
#                             id=jobhistoryid, 
#                             data=preparedata,
#                             choice_fields=choice_fields,
#                             fields_regex=fields_regex,
#                             static_fields=static_fields
#                         )
#                         if responsesuccessflag == 'success':
#                             response_data = responsedata.data
#                             response_successflag = responsesuccessflag
#                             response_status = responsestatus
#                 else:
#                     ###########################################
#                     companyid = preparedata.get('company')
#                     if companyid:
#                         company = MODELS_COMP.Company.objects.filter(id=companyid)
#                         if company.exists():
#                             companyid = company.first().id
#                             preparedata.update({'company': companyid})
#                         else:
#                             if previous_employeejobhistory.company:
#                                 companyid = previous_employeejobhistory.company.id
#                                 preparedata.update({'company': companyid})
#                     else:
#                         if previous_employeejobhistory.company:
#                             companyid = previous_employeejobhistory.company.id
#                             preparedata.update({'company': companyid})
                    
#                     branchid = None
#                     if companyid:
#                         branchid = preparedata.get('branch')
#                         if branchid:
#                             branch = MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid)
#                             if branch.exists():
#                                 branchid = branch.first().id
#                                 preparedata.update({'branch': branchid})
#                             else:
#                                 if previous_employeejobhistory.branch:
#                                     branchid = previous_employeejobhistory.branch.id
#                                     if MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid).exists():
#                                         preparedata.update({'branch': branchid})
#                                     else:
#                                         branchid = None
#                                         preparedata.update({'branch': None})
#                                 else:
#                                     branchid = None
#                                     preparedata.update({'branch': None})
#                         else:
#                             if previous_employeejobhistory.branch:
#                                 branchid = previous_employeejobhistory.branch.id
#                                 if MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid).exists():
#                                     preparedata.update({'branch': branchid})
#                                 else:
#                                     branchid = None
#                                     preparedata.update({'branch': None})
#                             else:
#                                 branchid = None
#                                 preparedata.update({'branch': None})

#                     departmentid = None
#                     if branchid:
#                         departmentid = preparedata.get('department')
#                         if departmentid:
#                             department = MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid)
#                             if department.exists():
#                                 departmentid = department.first().id
#                                 preparedata.update({'department': departmentid})
#                             else:
#                                 if previous_employeejobhistory.department:
#                                     departmentid = previous_employeejobhistory.department.id
#                                     if MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid).exists():
#                                         preparedata.update({'department': departmentid})
#                                     else:
#                                         departmentid = None
#                                         preparedata.update({'department': None})
#                                 else:
#                                     departmentid = None
#                                     preparedata.update({'department': None})
#                         else:
#                             if previous_employeejobhistory.department:
#                                 departmentid = previous_employeejobhistory.department.id
#                                 if MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid).exists():
#                                     preparedata.update({'department': departmentid})
#                                 else:
#                                     departmentid = None
#                                     preparedata.update({'department': None})
#                             else:
#                                 departmentid = None
#                                 preparedata.update({'department': None})
                    
#                     choice_fields = [
#                         {'name': 'increment_on', 'type': 'single-string', 'values': [item[1] for item in CHOICE.INCREMENT_ON]},
#                         {'name': 'employee_type', 'type': 'single-string', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
#                         {'name': 'status_adjustment', 'type': 'single-string', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]}
#                     ]
#                     fields_regex = [
#                         {'field': 'effective_from', 'type': 'date'},
#                         {'field': 'date', 'type': 'date'}
#                     ]

#                     responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
#                         classOBJ=MODELS_JOBR.Employeejobhistory, 
#                         Serializer=PSRLZER_JOBR.Employeejobhistoryserializer, 
#                         id=jobhistoryid, 
#                         data=preparedata, 
#                         choice_fields=choice_fields,
#                         fields_regex=fields_regex,
#                         static_fields=static_fields
#                     )
#                     if responsesuccessflag == 'success':
#                         response_data = responsedata.data
#                         response_successflag = responsesuccessflag
#                         response_status = responsestatus

#                         if responsedata['salary'] != user.gross_salary:
#                             basicSalary = ghelp().getBasicSalary(MODELS_SETT.Generalsettings, salary)
#                             if basicSalary['flag']:
#                                 MODELS_USER.User.objects.filter(id=user.id).update(gross_salary=salary, basic_salary=basicSalary['basic_salary'])
#                             else: MODELS_USER.User.objects.filter(id=user.id).update(gross_salary=salary)

#                         if responsedata['designation'] != user.designation.id:
#                             MODELS_USER.User.objects.filter(id=user.id).update(designation=MODELS_DEPA.Department.objects.get(id=responsedata['designation']))
#                         if responsedata['department'] != _department.id:
#                             _department.user.remove(user)
#                             MODELS_DEPA.Department.objects.get(id=responsedata['department']).user.add(user)
#                     # if departmentid: pass
#                     ###########################################
#         else:
#             if next_id:
#                 next_employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(id=next_id)
#                 if next_employeejobhistory.exists():
#                     if salary:
#                         next_salary = next_employeejobhistory.first().salary
#                         increment_amount = next_salary - salary
#                         percentage = increment_amount/100
#                         next_employeejobhistory.update(increment_amount=increment_amount, percentage=percentage)
                    
#                     choice_fields = [
#                         {'name': 'increment_on', 'type': 'single-string', 'values': [item[1] for item in CHOICE.INCREMENT_ON]},
#                         {'name': 'employee_type', 'type': 'single-string', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
#                         {'name': 'status_adjustment', 'type': 'single-string', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]}
#                     ]
#                     fields_regex = [
#                         {'field': 'effective_from', 'type': 'date'},
#                         {'field': 'date', 'type': 'date'}
#                     ]

#                     responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
#                         classOBJ=MODELS_JOBR.Employeejobhistory, 
#                         Serializer=PSRLZER_JOBR.Employeejobhistoryserializer, 
#                         id=jobhistoryid, 
#                         data=preparedata,
#                         choice_fields=choice_fields,
#                         fields_regex=fields_regex,
#                         static_fields=static_fields
#                     )
#                     if responsesuccessflag == 'success':
#                         response_data = responsedata.data
#                         response_successflag = responsesuccessflag
#                         response_status = responsestatus
#             else:
#                 ###########################################
#                 companyid = preparedata.get('company')
#                 if companyid:
#                     company = MODELS_COMP.Company.objects.filter(id=companyid)
#                     if company.exists():
#                         companyid = company.first().id
#                         preparedata.update({'company': companyid})
#                     else:
#                         if previous_employeejobhistory.company:
#                             companyid = previous_employeejobhistory.company.id
#                             preparedata.update({'company': companyid})
#                 else:
#                     if previous_employeejobhistory.company:
#                         companyid = previous_employeejobhistory.company.id
#                         preparedata.update({'company': companyid})
                
#                 branchid = None
#                 if companyid:
#                     branchid = preparedata.get('branch')
#                     if branchid:
#                         branch = MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid)
#                         if branch.exists():
#                             branchid = branch.first().id
#                             preparedata.update({'branch': branchid})
#                         else:
#                             if previous_employeejobhistory.branch:
#                                 branchid = previous_employeejobhistory.branch.id
#                                 if MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid).exists():
#                                     preparedata.update({'branch': branchid})
#                                 else:
#                                     branchid = None
#                                     preparedata.update({'branch': None})
#                             else:
#                                 branchid = None
#                                 preparedata.update({'branch': None})
#                     else:
#                         if previous_employeejobhistory.branch:
#                             branchid = previous_employeejobhistory.branch.id
#                             if MODELS_BRAN.Branch.objects.filter(id=branchid, company=companyid).exists():
#                                 preparedata.update({'branch': branchid})
#                             else:
#                                 branchid = None
#                                 preparedata.update({'branch': None})
#                         else:
#                             branchid = None
#                             preparedata.update({'branch': None})

#                 departmentid = None
#                 if branchid:
#                     departmentid = preparedata.get('department')
#                     if departmentid:
#                         department = MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid)
#                         if department.exists():
#                             departmentid = department.first().id
#                             preparedata.update({'department': departmentid})
#                         else:
#                             if previous_employeejobhistory.department:
#                                 departmentid = previous_employeejobhistory.department.id
#                                 if MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid).exists():
#                                     preparedata.update({'department': departmentid})
#                                 else:
#                                     departmentid = None
#                                     preparedata.update({'department': None})
#                             else:
#                                 departmentid = None
#                                 preparedata.update({'department': None})
#                     else:
#                         if previous_employeejobhistory.department:
#                             departmentid = previous_employeejobhistory.department.id
#                             if MODELS_DEPA.Department.objects.filter(id=departmentid, branch=branchid).exists():
#                                 preparedata.update({'department': departmentid})
#                             else:
#                                 departmentid = None
#                                 preparedata.update({'department': None})
#                         else:
#                             departmentid = None
#                             preparedata.update({'department': None})
                
#                 choice_fields = [
#                     {'name': 'increment_on', 'type': 'single-string', 'values': [item[1] for item in CHOICE.INCREMENT_ON]},
#                     {'name': 'employee_type', 'type': 'single-string', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
#                     {'name': 'status_adjustment', 'type': 'single-string', 'values': [item[1] for item in CHOICE.STATUS_ADJUSTMENT]}
#                 ]
#                 fields_regex = [
#                     {'field': 'effective_from', 'type': 'date'},
#                     {'field': 'date', 'type': 'date'}
#                 ]

#                 responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
#                     classOBJ=MODELS_JOBR.Employeejobhistory, 
#                     Serializer=PSRLZER_JOBR.Employeejobhistoryserializer, 
#                     id=jobhistoryid, 
#                     data=preparedata,
#                     choice_fields=choice_fields,
#                     fields_regex=fields_regex,
#                     static_fields=static_fields
#                 )
#                 if responsesuccessflag == 'success':
#                     response_data = responsedata.data
#                     response_successflag = responsesuccessflag
#                     response_status = responsestatus

#                     if responsedata['salary'] != user.gross_salary:
#                         basicSalary = ghelp().getBasicSalary(MODELS_SETT.Generalsettings, salary)
#                         if basicSalary['flag']:
#                             MODELS_USER.User.objects.filter(id=user.id).update(gross_salary=salary, basic_salary=basicSalary['basic_salary'])
#                         else: MODELS_USER.User.objects.filter(id=user.id).update(gross_salary=salary)

#                     if responsedata['designation'] != user.designation.id:
#                         MODELS_USER.User.objects.filter(id=user.id).update(designation=MODELS_DEPA.Department.objects.get(id=responsedata['designation']))
#                     if responsedata['department'] != _department.id:
#                         _department.user.remove(user)
#                         MODELS_DEPA.Department.objects.get(id=responsedata['department']).user.add(user)
#                 ###########################################
#     else: response_message.append(f'employee job history with this id{jobhistoryid} is missing!')
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Permission list Details', 'all'])
# def deletejobhistory(request, jobhistoryid=None):
#     response_data = {}
#     response_message = []
#     response_successflag = 'error'
#     response_status = status.HTTP_400_BAD_REQUEST
    
#     employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(id=jobhistoryid)
#     if employeejobhistory.exists():
#         user = employeejobhistory.first().user
#         previous_id = employeejobhistory.first().previous_id
#         next_id = employeejobhistory.first().next_id


#         designation = employeejobhistory.first().designation
#         department = employeejobhistory.first().department
#         salary = employeejobhistory.first().salary

#         employeejobhistory = MODELS_JOBR.Employeejobhistory.objects.filter(user=user.id).order_by('id')
#         if employeejobhistory.first().id != jobhistoryid:

#             responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().deleterecord(
#                 classOBJ=MODELS_JOBR.Employeejobhistory,
#                 id=jobhistoryid
#             )
#             if responsesuccessflag == 'success':
#                 if previous_id:
#                     previous = MODELS_JOBR.Employeejobhistory.objects.filter(id=previous_id)
#                     if previous.exists():
#                         if next_id:
#                             next = MODELS_JOBR.Employeejobhistory.objects.filter(id=next_id)
#                             if next.exists():
#                                 previous.update(next_id=next_id)

#                                 previous_salary = previous.first().salary
#                                 next_salary = next.first().salary

#                                 increment_amount = next_salary - previous_salary
#                                 percentage = (increment_amount*100)/previous_salary

#                                 next.update(previous_id=previous_id, increment_amount=increment_amount, percentage=percentage)
#                         else:
#                             previous.update(next_id=None)
#                             if previous.first().department.id != department.id:
#                                 department.user.remove(user)
#                                 previous.first().department.user.add(user)
#                             if user.gross_salary != previous.first().salary:
#                                 MODELS_USER.User.objects.filter(id=user.id).update(gross_salary = previous.first().salary)
#                             if user.designation != previous.first().designation:
#                                 MODELS_USER.User.objects.filter(id=user.id).update(designation = previous.first().designation)
#                     else: pass
#                 else: pass
#                 response_successflag = responsesuccessflag
#                 response_status = responsestatus
#             elif responsesuccessflag == 'error': response_message.extend(responsemessage)
#         else: response_message.append('first record can\'t be deleted!')
#     else: response_message.append('record doesn\'t exist!')
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)