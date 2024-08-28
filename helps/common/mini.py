import random
from django.contrib.auth.hashers import make_password
from helps.common.micro import Microhelps

class Minihelps(Microhelps):

    def getPermissionsListIfAll(self, permissions, user):
        permissions_dict = {}
        for role in user.role.all():
            for permission in role.permission.all():
                permissions_dict.update({permission.name: ''})
        permissions.extend([permission.lower() for permission in permissions_dict.keys()])

    def getPermissionsListIfActiveOrInactive(self, permissions, user, is_active):
        permissions_dict = {}
        for role in user.role.all():
            for permission in role.permission.filter(is_active=is_active):
                permissions_dict.update({permission.name: ''})
        permissions.extend([permission.lower() for permission in permissions_dict.keys()])
    
    def ifallrecordsexistornot(self, classOBJ, idlist): # New
        flag = True
        if idlist:
            for id in idlist:
                object = self.getobject(classOBJ, {'id': id})
                if object == None: flag = False
        return flag
    
    def getuserdetails(self, classOBJpackage, serializerOBJpackage, createdInstance,  personalDetails, officialDetails, salaryAndLeaves, photo, created_by): # New
        response = {'flag': True, 'message': [], 'data': {}}
        
        addbankaccountdetails = None
        if salaryAndLeaves:
            if 'bank_account' in salaryAndLeaves:
                if salaryAndLeaves['bank_account']:
                    addbankaccountdetails=self.addbankaccount(classOBJpackage, serializerOBJpackage, salaryAndLeaves['bank_account'], createdInstance)
                    if not addbankaccountdetails['flag']:
                        response['message'].extend([f'user\'s {each}' for each in addbankaccountdetails['message']])
                        # response['flag'] = False
                        addbankaccountdetails = None
                        

        # details = {
        #     'data': {
        #         'bank_account': {
        #             "bank_name":"Prime Asia",
        #             "branch_name": "Banani",
        #             "account_type": 1,
        #             "account_no": "1111111111",
        #             "routing_no": "22222222222",
        #             "swift_bic": "33333333333",
        #             "address": {
        #                 "address": "asdafefaeds",
        #                 "city": "saddsfd",
        #                 "state_division": "csfsfsfsf",
        #                 "country": "sddfferfv"
        #             }
        #         }
        #     },
        #     'order': ['bank_account', 'address'],
        #     'info': {
        #         'address': {
        #             'model': classOBJpackage['Address'],
        #             'serializer': serializerOBJpackage['Address'],
        #             'required_fields': ['address', 'city', 'state_division', 'country']
        #         },
        #         'bank_account': {
        #             'model': classOBJpackage['Bankaccount'],
        #             'serializer': serializerOBJpackage['Bankaccount'],
        #             'required_fields': ['bank_name', 'branch_name', 'account_type', 'account_no', 'routing_no']
        #         }
        #     }
        # }
        # addbankaccountdetails = None
        # if salaryAndLeaves:
        #     if 'bank_account' in salaryAndLeaves:
        #         if salaryAndLeaves['bank_account']:
        #             addbankaccountdetails=self.nestedObjectPrepare(details)
        #             print(addbankaccountdetails)
        #             input()
        #             if not addbankaccountdetails['flag']:
        #                 response['message'].extend([f'user\'s {each}' for each in addbankaccountdetails['message']])
        #                 # response['flag'] = False
        #                 addbankaccountdetails = None



        presentaddressdetails = None
        if personalDetails:
            if 'present_address' in personalDetails:
                if personalDetails['present_address']:
                    required_fields = ['address', 'city', 'state_division', 'country']
                    responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                        classOBJ=classOBJpackage['Address'],
                        Serializer=serializerOBJpackage['Address'],
                        data=personalDetails['present_address'],
                        required_fields=required_fields
                    )
                    if responsesuccessflag == 'success':
                        presentaddressdetails = responsedata.instance
                        createdInstance.append(presentaddressdetails)
                    elif responsesuccessflag == 'error':
                        response['message'].extend([f'user present address\'s {each}' for each in responsemessage])
                        response['flag'] = False
        
        permanentaddressdetails = None
        same_as_present_address = False
        if personalDetails:
            if 'permanentAddressSameAsPresent' in personalDetails:
                if personalDetails['permanentAddressSameAsPresent']:
                    permanentaddressdetails = presentaddressdetails
                    same_as_present_address = True
        if not same_as_present_address:
            if personalDetails:
                if 'permanent_address' in personalDetails:
                    if personalDetails['permanent_address']:
                        required_fields = ['address', 'city', 'state_division', 'country']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                            classOBJ=classOBJpackage['Address'],
                            Serializer=serializerOBJpackage['Address'],
                            data=personalDetails['permanent_address'],
                            required_fields=required_fields
                        )
                        if responsesuccessflag == 'success':
                            permanentaddressdetails = responsedata.instance
                            createdInstance.append(permanentaddressdetails)
                        elif responsesuccessflag == 'error':
                            response['message'].extend([f'user permanet address {each}' for each in responsemessage])
                            response['flag'] = False
        if not response['message']:
            fields_to_prepare_details_obj = self.prepareUserObjInfo(personalDetails, officialDetails, salaryAndLeaves)
            for each in fields_to_prepare_details_obj:
                self.ifExistThanAddToDict(each['obj'], each['field'], each['replace'], response['data'])

            if 'gross_salary' in response['data']:
                if 'Generalsettings' in classOBJpackage:
                    try:
                        gross_salary = float(response['data']['gross_salary'])
                        basicSalary = self.getBasicSalary(classOBJpackage['Generalsettings'], gross_salary)
                        if basicSalary['flag']: response['data'].update({'basic_salary': basicSalary['basic_salary']})
                    except: pass

            religion = self.getobject(classOBJpackage['Religion'], {'id': personalDetails.get('religion')})
            if religion: response['data'].update({'religion': religion.id})
            if presentaddressdetails: response['data'].update({'present_address': presentaddressdetails.id})
            if permanentaddressdetails: response['data'].update({'permanent_address': permanentaddressdetails.id})
            designation = self.getobject(classOBJpackage['Designation'], {'id': officialDetails.get('designation')})
            if designation: response['data'].update({'designation': designation.id})
            shift = self.getobject(classOBJpackage['Shift'], {'id': officialDetails.get('shift')})
            if shift: response['data'].update({'shift': shift.id})
            grade = self.getobject(classOBJpackage['Grade'], {'id': officialDetails.get('grade')})
            if grade: response['data'].update({'grade': grade.id})
            supervisor = self.getobject(classOBJpackage['User'], {'id': officialDetails.get('supervisor')})
            if supervisor: response['data'].update({'supervisor': supervisor.id})
            expense_approver = self.getobject(classOBJpackage['User'], {'id': officialDetails.get('expense_approver')})
            if expense_approver: response['data'].update({'expense_approver': expense_approver.id})
            leave_approver = self.getobject(classOBJpackage['User'], {'id': officialDetails.get('leave_approver')})
            if leave_approver: response['data'].update({'leave_approver': leave_approver.id})
            shift_request_approver = self.getobject(classOBJpackage['User'], {'id': officialDetails.get('shift_request_approver')})
            if shift_request_approver: response['data'].update({'shift_request_approver': shift_request_approver.id})
            if addbankaccountdetails: response['data'].update({'bank_account': addbankaccountdetails['instance'].id})
            response['data'].update({'created_by': created_by.id, 'updated_by': created_by.id})
            if photo:
                photo_response = self.validateprofilepic(photo)
                if photo_response['flag']: response['data'].update({'photo': photo})
                else: response['message'].extend(photo_response['message'])
            response['flag'] = True
        return response
    
    def createuserinstance(self, User, details, photo): # New
        response = {'flag': True, 'message': [], 'instance': {}}
        userinstance = User()
        if details.get('username'): userinstance.username=details['username']
        if details.get('first_name'): userinstance.first_name=details['first_name']
        if details.get('last_name'): userinstance.last_name=details['last_name']
        if details.get('gender'): userinstance.gender=details['gender']
        if details.get('dob'): userinstance.dob=details['dob']
        if details.get('blood_group'): userinstance.blood_group=details['blood_group']
        if details.get('fathers_name'): userinstance.fathers_name=details['fathers_name']
        if details.get('mothers_name'): userinstance.mothers_name=details['mothers_name']
        if details.get('marital_status'): userinstance.marital_status=details['marital_status']
        if details.get('spouse_name'): userinstance.spouse_name=details['spouse_name']
        if details.get('nationality'): userinstance.nationality=details['nationality']
        if details.get('religion'): userinstance.religion=details['religion']
        if details.get('personal_email'): userinstance.personal_email=details['personal_email']
        if details.get('personal_phone'): userinstance.personal_phone=details['personal_phone']
        if details.get('nid_passport_no'): userinstance.nid_passport_no=details['nid_passport_no']
        if details.get('tin_no'): userinstance.tin_no=details['tin_no']
        if details.get('present_address'): userinstance.present_address=details['present_address']
        if details.get('permanent_address'): userinstance.permanent_address=details['permanent_address']
        userinstance.dummy_salary=random.randint(5000,300000)
        if details.get('official_id'): userinstance.official_id=details['official_id']
        if details.get('official_email'): userinstance.official_email=details['official_email']
        if details.get('official_phone'): userinstance.official_phone=details['official_phone']
        if details.get('password'): userinstance.password=details['password']
        if details.get('hr_password'): userinstance.hr_password=details['hr_password']
        if details.get('employee_type'): userinstance.employee_type=details['employee_type']
        if details.get('designation'): userinstance.designation=details['designation']
        if details.get('shift'): userinstance.shift=details['shift']
        if details.get('grade'): userinstance.grade=details['grade']
        if details.get('official_note'): userinstance.official_note=details['official_note']
        if details.get('joining_date'): userinstance.joining_date=details['joining_date']
        if details.get('job_status'): userinstance.job_status=details['job_status']
        if details.get('rfid'): userinstance.rfid=details['rfid']
        if details.get('allow_overtime'): userinstance.allow_overtime=details['allow_overtime']
        if details.get('allow_remote_checkin'): userinstance.allow_remote_checkin=details['allow_remote_checkin']
        if details.get('active_dummy_salary'): userinstance.active_dummy_salary=details['active_dummy_salary']
        if details.get('supervisor'): userinstance.supervisor=details['supervisor']
        if details.get('expense_approver'): userinstance.expense_approver=details['expense_approver']
        if details.get('leave_approver'): userinstance.leave_approver=details['leave_approver']
        if details.get('shift_request_approver'): userinstance.shift_request_approver=details['shift_request_approver']
        if details.get('payment_in'): userinstance.payment_in=details['payment_in']
        if details.get('bank_account'): userinstance.bank_account=details['bank_account']
        if details.get('gross_salary'): userinstance.gross_salary=details['gross_salary']
        if details.get('created_by'): userinstance.created_by=details['created_by']
        if details.get('updated_by'): userinstance.updated_by=details['updated_by']
        if photo: userinstance.photo=photo
        try:
            userinstance.save()
            response['instance'] = userinstance
        except: response['flag'] = False

        return response
    
    def getOBJDetails(self, object, fields): # New
        mainObj = {}
        for field in fields['fieldlist']:
            if field['field'] in object:
                if object[field['field']]:
                    if field['type'] == 'str':
                        if field['field'] in object:
                            if isinstance(object[field['field']], list):
                                if object[field['field']][0]:
                                    mainObj.update({field['field']: object[field['field']][0]})
                            else: mainObj.update({field['field']: object[field['field']]})
                        
                    elif field['type'] == 'int':
                        if field['field'] in object:
                            if isinstance(object[field['field']], list):
                                if object[field['field']][0]:
                                    try: mainObj.update({field['field']: int(object[field['field']][0])})
                                    except: pass
                            else:
                                try: mainObj.update({field['field']: int(object[field['field']])})
                                except: pass

                        
                    elif field['type'] == 'bool':
                        if field['field'] in object:
                            value = None
                            if isinstance(object[field['field']], list):
                                if object[field['field']][0]:
                                    try: value = True if object[field['field']][0].lower() == 'true' else False if object[field['field']][0].lower() == 'false' else None
                                    except: pass
                            else:
                                try: value = True if object[field['field']].lower() == 'true' else False if object[field['field']].lower() == 'false' else None
                                except: pass
                            if value != None: mainObj.update({field['field']: value})
                    elif field['type'] == 'list-int':
                        if field['field'] in object:
                            if isinstance(object[field['field']], list):
                                subList = []
                                for each in object[field['field']]:
                                    if each.isnumeric():
                                        if each not in subList: subList.append(int(each))
                                if subList: mainObj.update({field['field']: subList})
                    elif field['type'] == 'list-str':
                        if field['field'] in object:
                            if isinstance(object[field['field']], list):
                                subList = []
                                for each in object[field['field']]:
                                    if each:
                                        if each not in subList: subList.append(each)
                                if subList: mainObj.update({field['field']: subList})
        if 'nestedfields' in fields:
            for nestedfield in fields['nestedfields']:
                if nestedfield['field'] in object:
                    subObj = {}
                    if nestedfield['fieldlist']:
                        for field in nestedfield['fieldlist']:
                            if field['field'] in object[nestedfield['field']]:
                                if object[nestedfield['field']][field['field']]:
                                    if field['type'] == 'str':
                                        if isinstance(object[nestedfield['field']][field['field']], list):
                                            if object[nestedfield['field']][field['field']][0]:
                                                subObj.update({field['field']: object[nestedfield['field']][field['field']][0]})
                                        else: subObj.update({field['field']: object[nestedfield['field']][field['field']]})
                                    elif field['type'] == 'int':
                                        if isinstance(object[nestedfield['field']][field['field']], list):
                                            if object[nestedfield['field']][field['field']][0]:
                                                try: subObj.update({field['field']: int(object[nestedfield['field']][field['field']][0])})
                                                except: pass
                                        else:
                                            try: subObj.update({field['field']: int(object[nestedfield['field']][field['field']])})
                                            except: pass
                                    elif field['type'] == 'bool':
                                        value = None
                                        if isinstance(object[nestedfield['field']][field['field']], list):
                                            if object[nestedfield['field']][field['field']][0]:
                                                try: value = True if object[nestedfield['field']][field['field']][0].lower() == 'true' else False if object[nestedfield['field']][field['field']][0].lower() == 'false' else None
                                                except: pass
                                        else:
                                            try: value = True if object[nestedfield['field']][field['field']].lower() == 'true' else False if object[nestedfield['field']][field['field']].lower() == 'false' else None
                                            except: pass
                                        if value != None: subObj.update({field['field']: value})

                                    elif field['type'] == 'list-int':
                                        if isinstance(object[nestedfield['field']][field['field']], list):
                                            subList = []
                                            for each in object[nestedfield['field']][field['field']]:
                                                if each.isnumeric():
                                                    if each not in subList: subList.append(int(each))
                                            if subList: subObj.update({field['field']: subList})
                                    elif field['type'] == 'list-str':
                                        if isinstance(object[nestedfield['field']][field['field']], list):
                                            subList = []
                                            for each in object[nestedfield['field']][field['field']]:
                                                if each:
                                                    if each not in subList: subList.append(each)
                                            if subList: subObj.update({field['field']: subList})
                    if subObj: mainObj.update({nestedfield['field']: subObj})
        return mainObj if mainObj else None
    


    def addUserRecord(self, information={}): # New
        response = {'failed': [], 'message': [], 'backend_message': []}
        if information:
            if isinstance(information, dict):
                outer_details = information['outer_details'] if 'outer_details' in information else {}
                inner_details = information['inner_details'] if 'inner_details' in information else {}
                if outer_details:
                    if 'userid' in outer_details:
                        if 'classOBJ' in outer_details:
                            if 'Serializer' in outer_details:
                                if 'data' in outer_details:
                                    if isinstance(outer_details['data'], list):
                                        for index, details in enumerate(outer_details['data']):

                                            details_copy = details.copy()
                                            details.update({'user': outer_details['userid']})
                                            
                                            inner_instance = None
                                            inner_responsemessage = []
                                            if inner_details:
                                                if 'classOBJ' in inner_details:
                                                    if 'Serializer' in inner_details:
                                                        if 'key' in inner_details:
                                                            if inner_details['key'] in details:
                                                                if details[inner_details['key']]:

                                                                    allowed_fields = inner_details['allowed_fields'] if 'allowed_fields' in inner_details else []
                                                                    unique_fields = inner_details['unique_fields'] if 'unique_fields' in inner_details else []
                                                                    required_fields = inner_details['required_fields'] if 'required_fields' in inner_details else []
                                                                    extra_fields = inner_details['extra_fields'] if 'extra_fields' in inner_details else {}
                                                                    choice_fields = inner_details['choice_fields'] if 'choice_fields' in inner_details else []
                                                                    fields_regex = inner_details['fields_regex'] if 'fields_regex' in inner_details else []

                                                                    responsedata, responsemessage, responsesuccessflag, _ = self.addtocolass(
                                                                        classOBJ=inner_details['classOBJ'],
                                                                        Serializer=inner_details['Serializer'],
                                                                        data=details[inner_details['key']],
                                                                        allowed_fields=allowed_fields,
                                                                        unique_fields=unique_fields,
                                                                        required_fields=required_fields,
                                                                        extra_fields=extra_fields,
                                                                        choice_fields=choice_fields,
                                                                        fields_regex=fields_regex
                                                                    )
                                                                    if responsesuccessflag == 'success':
                                                                        inner_instance = responsedata.instance
                                                                        details.update({inner_details['key']: responsedata.instance.id})
                                                                    elif responsesuccessflag == 'error':
                                                                        inner_responsemessage.extend([f'Warning: {outer_details["classOBJ"].__name__}(index: {index})\'s address {each}, therefore couldn\'t add {inner_details["classOBJ"].__name__}, please update later!' for each in responsemessage])
                                                                        del details[inner_details['key']]
                                                                else: del details[inner_details['key']]
                                                            else: response['backend_message'].append(f'{inner_details["key"]} key doesn\'t exist in provided object!')
                                                        else: response['backend_message'].append('inner_details object key is missing!')    
                                                    else: response['backend_message'].append('Serializer is missing in inner_details!')
                                                else: response['backend_message'].append('classOBJ is missing in inner_details!')
                                            

                                            allowed_fields = outer_details['allowed_fields'] if 'allowed_fields' in outer_details else []
                                            unique_fields = outer_details['unique_fields'] if 'unique_fields' in outer_details else []
                                            required_fields = outer_details['required_fields'] if 'required_fields' in outer_details else []
                                            extra_fields = outer_details['extra_fields'] if 'extra_fields' in outer_details else {}
                                            choice_fields = outer_details['choice_fields'] if 'choice_fields' in outer_details else []
                                            fields_regex = outer_details['fields_regex'] if 'fields_regex' in outer_details else []
                                            
                                            _, response_message, response_successflag, _ = self.addtocolass(
                                                classOBJ=outer_details['classOBJ'],
                                                Serializer=outer_details['Serializer'],
                                                data=details,
                                                allowed_fields=allowed_fields,
                                                unique_fields=unique_fields,
                                                required_fields=required_fields,
                                                extra_fields=extra_fields,
                                                choice_fields=choice_fields,
                                                fields_regex=fields_regex
                                            )
                                            if response_successflag == 'success': response['message'].extend(inner_responsemessage)
                                            elif response_successflag == 'error':
                                                failed_messages = [f'{outer_details["classOBJ"].__name__} {each}, therefore couldn\'t add this(index: {index}) record!' for each in response_message]
                                                objects = {'details': details_copy, 'message': failed_messages}
                                                response['failed'].append(objects)
                                                response['message'].extend(failed_messages)
                                                if inner_instance: inner_instance.delete()
                                    else: response['message'].append(f'{outer_details["classOBJ"].__name__}\'s data should be type of list!')
                                else: response['backend_message'].append('data is missing in outer_details!')
                            else: response['backend_message'].append('Serializer is missing in outer_details!')
                        else: response['backend_message'].append('classOBJ is missing in outer_details!')
                    else: response['backend_message'].append('user id is missing in outer_details!')
                else: response['backend_message'].append('provide outer_details!')
            else: response['backend_message'].append('type of information should be dict!')
        return response
    
    def assignLeavepolicyToBulkUser(self, classOBJpackage, userlist, leavepolicyid, fiscalyear, manipulate_info): # New
        response = {'flag': False, 'message': []}
        if userlist:
            if isinstance(userlist, list):

                leavepolicy = self.getobject(classOBJpackage['Leavepolicy'], {'id': leavepolicyid})
                if leavepolicy:
                    for userid in userlist:
                        user = self.getobject(classOBJpackage['User'], {'id': userid})
                        if user:
                            is_already_assigned = True
                            leavepolicyassign = classOBJpackage['Leavepolicyassign'].objects.filter(user=user, leavepolicy=leavepolicy)
                            if not leavepolicyassign.exists():
                                created_by = classOBJpackage['User'].objects.get(id=manipulate_info['created_by'])
                                leavepolicyassign = classOBJpackage['Leavepolicyassign'].objects.create(user=user, leavepolicy=leavepolicy, created_by=created_by, updated_by=created_by)
                                is_already_assigned = False
                            leavesummary = classOBJpackage['Leavesummary'].objects.filter(user=user, leavepolicy=leavepolicy)
                            if not leavesummary.exists():
                                classOBJpackage['Leavesummary'].objects.create(
                                    user=user,
                                    leavepolicy=leavepolicy,
                                    fiscal_year=fiscalyear,
                                    total_allocation=leavepolicy.allocation_days,
                                    total_consumed=0,
                                    total_left=leavepolicy.allocation_days
                                )
                                is_already_assigned = False
                            if is_already_assigned:
                                response['flag'] = True
                                response['message'].append(f'{leavepolicy.name} leavepolicy is already assigned to {user.get_full_name()}({userid})!')
                            else:
                                response['flag'] = True
                                response['message'].append(f'successfully assigned {leavepolicy.name}({leavepolicyid}) to {user.get_full_name()}({userid})')
                        else: response['message'].append(f'user{userid} doesn\'t exist therefor couldn\'t assign leavepolicy!')
                else: response['message'].append(f'leavepolicy{leavepolicyid} doesn\'t exist therefor couldn\'t assign to given users!')
            else: response['message'].append('userid will be placed in list!')
        else: response['message'].append('user list is blank!')
        return response
    