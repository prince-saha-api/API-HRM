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
        if 'bank_account' in salaryAndLeaves:
            addbankaccountdetails=self.addbankaccount(classOBJpackage, serializerOBJpackage, salaryAndLeaves['bank_account'], createdInstance)
            if not addbankaccountdetails['flag']:
                response['message'].extend([f'user\'s {each}' for each in addbankaccountdetails['message']])
                response['flag'] = False
                addbankaccountdetails = None

        presentaddressdetails = None
        if 'present_address' in personalDetails:
            required_fields = ['address', 'city', 'state_division', 'country']
            response_data, response_message, response_successflag, response_status = self.addtocolass(
                classOBJ=classOBJpackage['Address'],
                Serializer=serializerOBJpackage['Address'],
                data=personalDetails['present_address'],
                required_fields=required_fields
            )
            if response_successflag == 'success':
                presentaddressdetails = response_data.instance
                createdInstance.append(presentaddressdetails)
            elif response_successflag == 'error':
                response['message'].extend([f'user present address\'s {each}' for each in response_message])
                response['flag'] = False
        
        permanentaddressdetails = None
        same_as_present_address = False
        if 'permanentAddressSameAsPresent' in personalDetails:
            if personalDetails['permanentAddressSameAsPresent']:
                permanentaddressdetails = presentaddressdetails
                same_as_present_address = True
        if not same_as_present_address:
            if 'permanent_address' in personalDetails:
                required_fields = ['address', 'city', 'state_division', 'country']
                response_data, response_message, response_successflag, response_status = self.addtocolass(
                    classOBJ=classOBJpackage['Address'],
                    Serializer=serializerOBJpackage['Address'],
                    data=personalDetails['permanent_address'],
                    required_fields=required_fields
                )
                if response_successflag == 'success':
                    permanentaddressdetails = response_data.instance
                    createdInstance.append(permanentaddressdetails)
                elif response_successflag == 'error':
                    response['message'].extend([f'user permanet address {each}' for each in response_message])
                    response['flag'] = False
                
        if response['flag']:
            fields_to_prepare_details_obj = self.prepareUserObjInfo(personalDetails, officialDetails, salaryAndLeaves)
            for each in fields_to_prepare_details_obj:
                self.ifExistThanAddToDict(each['obj'], each['field'], each['replace'], response['data'])

            if 'gross_salary' in response['data']:
                if 'Generalsettings' in classOBJpackage:
                    generalsettings = self.findGeneralsettings(classOBJpackage['Generalsettings'])
                    if generalsettings:
                        if generalsettings.basic_salary_percentage:
                            try:
                                gross_salary = float(response['data']['gross_salary'])
                                basic_salary_percentage = generalsettings.basic_salary_percentage
                                basic_salary = (basic_salary_percentage*gross_salary)/100
                                response['data'].update({'basic_salary': basic_salary})
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
                if self.validatejpgimg(photo): response['data'].update({'photo': photo})
                else: response['message'].append('please, provide an image within 100 kb and jpg format!')
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

    # def getOBJDetails(self, object, fields): # New
    #     print(object)
    #     input()
    #     mainObj = {}
    #     for field in fields['fieldlist']:
    #         if field['field'] in object:
    #             if isinstance(object[field['field']], list):
    #                 if len(object[field['field']])>=1:
    #                     if object[field['field']][0]:
    #                         if field['type'] == 'str':
    #                             # print('str')
    #                             # print(field['field'])
    #                             # print(object[field['field']])
    #                             # print(object[field['field']][0])
    #                             mainObj.update({field['field']: object[field['field']][0]})
    #                         elif field['type'] == 'int':
    #                             print('int')
    #                             print(field['field'])
    #                             print(object[field['field']])
    #                             print(object[field['field']][0])
    #                             mainObj.update({field['field']: int(object[field['field']][0])})
    #                         elif field['type'] == 'bool':
    #                             print('bool')
    #                             print(field['field'])
    #                             print(object[field['field']])
    #                             print(object[field['field']][0])
    #                             value = True if object[field['field']][0].lower() == 'true' else False if object[field['field']][0].lower() == 'false' else None
    #                             if value != None: mainObj.update({field['field']: value})
    #                         elif field['type'] == 'list-int':
    #                             print('list-int')
    #                             print(field['field'])
    #                             print(object[field['field']])
    #                             print(object[field['field']][0])
    #                             subList = []
    #                             for each in object[field['field']]:
    #                                 if each.isnumeric():
    #                                     if each not in subList: subList.append(int(each))
    #                             if subList: mainObj.update({field['field']: subList})
    #                         elif field['type'] == 'list-str':
    #                             print('list-str')
    #                             print(field['field'])
    #                             print(object[field['field']])
    #                             print(object[field['field']][0])
    #                             subList = []
    #                             for each in object[field['field']]:
    #                                 if each:
    #                                     if each not in subList: subList.append(each)
    #                             if subList: mainObj.update({field['field']: subList})
    #     if 'nestedfields' in fields:
    #         for nestedfield in fields['nestedfields']:
    #             if nestedfield['field'] in object:
    #                 subObj = {}
    #                 if nestedfield['fieldlist']:
    #                     for field in nestedfield['fieldlist']:
    #                         if field['field'] in object[nestedfield['field']]:
    #                             if isinstance(object[nestedfield['field']][field['field']], list):
    #                                 if len(object[nestedfield['field']][field['field']])>=1:
    #                                     if object[nestedfield['field']][field['field']][0]:
    #                                         if field['type'] == 'str':
    #                                             print('str')
    #                                             print(field['field'])
    #                                             print(object[field['field']])
    #                                             print(object[field['field']][0])
    #                                             subObj.update({field['field']: object[nestedfield['field']][field['field']][0]})
    #                                         elif field['type'] == 'int':
    #                                             print('int')
    #                                             print(field['field'])
    #                                             print(object[field['field']])
    #                                             print(object[field['field']][0])
    #                                             subObj.update({field['field']: int(object[nestedfield['field']][field['field']][0])})
    #                                         elif field['type'] == 'bool':
    #                                             print('bool')
    #                                             print(field['field'])
    #                                             print(object[field['field']])
    #                                             print(object[field['field']][0])
    #                                             value = True if object[nestedfield['field']][field['field']][0].lower() == 'true' else False if object[nestedfield['field']][field['field']][0].lower() == 'false' else None
    #                                             if value != None: mainObj.update({field['field']: value})
    #                                         elif field['type'] == 'list-int':
    #                                             print('list-int')
    #                                             print(field['field'])
    #                                             print(object[field['field']])
    #                                             print(object[field['field']][0])
    #                                             subList = []
    #                                             for each in object[nestedfield['field']][field['field']]:
    #                                                 if each.isnumeric():
    #                                                     if each not in subList: subList.append(int(each))
    #                                             if subList: mainObj.update({field['field']: subList})
    #                                         elif field['type'] == 'list-str':
    #                                             print('list-str')
    #                                             print(field['field'])
    #                                             print(object[field['field']])
    #                                             print(object[field['field']][0])
    #                                             subList = []
    #                                             for each in object[nestedfield['field']][field['field']]:
    #                                                 if each:
    #                                                     if each not in subList: subList.append(each)
    #                                             if subList: mainObj.update({field['field']: subList})
    #                 if subObj: mainObj.update({nestedfield['field']: subObj})
    #     return mainObj if mainObj else None
    
    def addemergencycontact(self, Employeecontact, Employeecontactserializer, Address, Addressserializer, userinstance, emergencyContact): # New
        response = {'success': [], 'failed': [], 'message': []}
        if isinstance(emergencyContact, list):
            for index, details in enumerate(emergencyContact):
                details_copy = details.copy()
                details.update({'user': userinstance.id})
                
                address_flag = True
                address_responsemessage = []

                allowed_fields = ['alias', 'address', 'city', 'state_division', 'post_zip_code', 'country', 'latitude', 'longitude']
                required_fields = ['address', 'city', 'state_division', 'country']
                responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                    classOBJ=Address,
                    Serializer=Addressserializer,
                    data=details,
                    allowed_fields=allowed_fields,
                    required_fields=required_fields
                )

                if responsesuccessflag == 'success': details.update({'address': responsedata.instance.id})
                elif responsesuccessflag == 'error':
                    address_responsemessage.extend(responsemessage)
                    address_flag = False
                    del details['address']

                allowed_fields = ['name', 'user', 'age', 'phone_no', 'email', 'address', 'relation']
                required_fields = ['name', 'user']
                unique_fields = ['phone_no']
                fields_regex = [
                    {'field': 'phone_no', 'type': 'phonenumber'},
                    {'field': 'email', 'type': 'email'}
                ]
                response_data, response_message, response_successflag, response_status = self.addtocolass(
                    classOBJ=Employeecontact,
                    Serializer=Employeecontactserializer,
                    data=details,
                    allowed_fields=allowed_fields,
                    required_fields=required_fields,
                    unique_fields=unique_fields,
                    fields_regex=fields_regex
                )
                if response_successflag == 'success':
                    objects = {'details': details_copy, 'message': []}
                    if not address_flag: objects['message'].extend([f'{index+1} user\'s emergency contact address {each}' for each in address_responsemessage])
                    response['success'].append(objects)
                elif response_successflag == 'error':
                    objects = {'details': details_copy, 'message': []}
                    objects['message'].extend([f'{index+1} user\'s emergency contact {each}' for each in response_message])
                    if not address_flag: objects['message'].extend([f'{index+1} user\'s emergency contact address {each}' for each in address_responsemessage])
                    response['failed'].append(objects)
        else: response['message'].append('emergencycontact is not list type!')
        return response
    
    def addacademicrecord(self, Employeeacademichistory, Employeeacademichistoryserializer, userinstance, academicRecord): # New
        response = {'success': [], 'failed': [], 'message': []}
        if isinstance(academicRecord, list):
            for index, details in enumerate(academicRecord):
                details_copy = details.copy()
                details.update({'user': userinstance.id})

                required_fields = ['user', 'board_institute_name', 'certification', 'level', 'score_grade', 'year_of_passing']
                response_data, response_message, response_successflag, response_status = self.addtocolass(
                    classOBJ=Employeeacademichistory,
                    Serializer=Employeeacademichistoryserializer,
                    data=details,
                    required_fields=required_fields
                )
                if response_successflag == 'success':
                    objects = {'details': details_copy, 'message': []}
                    response['success'].append(objects)
                elif response_successflag == 'error':
                    objects = {'details': details_copy, 'message': []}
                    objects['message'].extend([f'{index+1} user\'s academic record {each}' for each in response_message])
                    response['failed'].append(objects)
        else: response['message'].append('academicrecord is not list type!')
        return response
    
    def addpreviousexperience(self, Employeeexperiencehistory, Employeeexperiencehistoryserializer, userinstance, previousExperience): # New 
        response = {'success': [], 'failed': [], 'message': []}
        if isinstance(previousExperience, list):
            for index, details in enumerate(previousExperience):
                details_copy = details.copy()
                details.update({'user': userinstance.id})

                required_fields = ['user', 'company_name', 'designation', 'address', 'from_date', 'to_date']
                fields_regex = [
                    {'field': 'from_date', 'type': 'date'},
                    {'field': 'to_date', 'type': 'date'}
                ]
                response_data, response_message, response_successflag, response_status = self.addtocolass(
                    classOBJ=Employeeexperiencehistory,
                    Serializer=Employeeexperiencehistoryserializer,
                    data=details,
                    required_fields=required_fields,
                    fields_regex=fields_regex
                )
                if response_successflag == 'success':
                    objects = {'details': details_copy, 'message': []}
                    response['success'].append(objects)
                elif response_successflag == 'error':
                    objects = {'details': details_copy, 'message': []}
                    objects['message'].extend([f'{index+1} user\'s previous experience {each}' for each in response_message])
                    response['failed'].append(objects)
        else: response['message'].append('previousexperience is not list type!')
        return response
    
    
    def addLeavepolicy(self, classOBJpackage, leavepolicylist, userdata): # New 
        response_message = []
        if 'Generalsettings' in classOBJpackage:
            if 'Leavepolicy' in classOBJpackage:
                if 'Leavepolicyassign' in classOBJpackage:
                    if 'Leavesummary' in classOBJpackage:
                        fiscalyear_response = self.findFiscalyear(classOBJpackage['Generalsettings'])
                        if fiscalyear_response['fiscalyear']:
                            if leavepolicylist:
                                if isinstance(leavepolicylist, list):
                                    for id in leavepolicylist:
                                        leavepolicy = self.getobject(classOBJpackage['Leavepolicy'], {'id': id})
                                        if leavepolicy:
                                            leavepolicyassign_flag = True
                                            if not classOBJpackage['Leavepolicyassign'].objects.filter(user=userdata['instance'], leavepolicy=leavepolicy).exists():
                                                try: classOBJpackage['Leavepolicyassign'].objects.create(user=userdata['instance'], leavepolicy=leavepolicy, created_by=userdata['created_by'], updated_by=userdata['updated_by'])
                                                except: leavepolicyassign_flag = False
                                            if not classOBJpackage['Leavesummary'].objects.filter(user=userdata['instance'], leavepolicy=leavepolicy).exists():
                                                if leavepolicyassign_flag:
                                                    try: classOBJpackage['Leavesummary'].objects.create(
                                                            user=userdata['instance'],
                                                            leavepolicy=leavepolicy,
                                                            fiscal_year=fiscalyear_response['fiscalyear'],
                                                            total_allocation=leavepolicy.allocation_days,
                                                            total_consumed=0,
                                                            total_left=leavepolicy.allocation_days
                                                        )
                                                    except:
                                                        classOBJpackage['Leavepolicyassign'].objects.filter(user=userdata['instance'], leavepolicy=leavepolicy).delete()
                                                        response_message.append(f'couldn\'t assign {leavepolicy.name} leavepolicy({id})!')
                                                else:
                                                    classOBJpackage['Leavepolicyassign'].objects.filter(user=userdata['instance'], leavepolicy=leavepolicy).delete()
                                                    response_message.append(f'couldn\'t assign {leavepolicy.name} leavepolicy({id})!')
                                        else: response_message.append('leavepolicy doesn\'t exist!')
                                else: response_message.append('leavepolicy type should be list!')
                            else: response_message.append('leavepolicy should not be empty!')
                        else: response_message.extend(fiscalyear_response['message'])
                    else: response_message.append('Leavesummary Model is missing!')
                else: response_message.append('Leavepolicyassign Model is missing!')
            else: response_message.append('Leavepolicy Model is missing!')
        else: response_message.append('Generalsettings Model is missing!')
        return response_message