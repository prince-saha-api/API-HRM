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
    
    def getEmployeeWorkingDatesIdealCase(self, Offday, customuser, daysinmonth, year, month):
        employeeworkingdates = []
        applicableholidays = self.getApplicableHolidayDates(customuser)
        for day in range(1, daysinmonth+1):
            if self.isWorkingDayAccordingToOfficeOffDay(Offday, year, month, day):
                date = self.convert_STR_STR_y_m_d(year, month, day)
                if date not in applicableholidays:
                    employeeworkingdates.append(date)
        return employeeworkingdates

    def generateAttendanceReport(self, Workingminutesperday, Latefineforfewdays, total_working_days_ideal, employeeworkingdates_idealcase, employeeworkingdates_reality, attendances):
        attendance_report = self.generateOBJAttendanceReport(total_working_days_ideal)
        latefineforfewdays = self.getFirstObjectIfExistOrNot(Latefineforfewdays)
        cost_in_days = latefineforfewdays.cost_in_days
        consecutive = latefineforfewdays.consecutive
        
        if cost_in_days == 0:
            for employeeworkingdate_idealcase in employeeworkingdates_idealcase:
                if employeeworkingdate_idealcase in employeeworkingdates_reality:

                    attendance = attendances.get(date=employeeworkingdate_idealcase)

                    attendance_report['attendance']['attendance_count'] += 1
                    if attendance.late_in_based_on_buffertime>0:
                        in_a_row_late_details.update(self.prepareDetailsAttendanceReport(employeeworkingdate_idealcase, attendance))
                        attendance_report['late_attendance_based_on_buffer_count'] += 1
                    if isinstance(attendance.total_minutes, float):
                        attendance_report['total_minutes'] += attendance.total_minutes

                    attendance_report['attendance']['details'].update(self.prepareDetailsAttendanceReport(employeeworkingdate_idealcase, attendance))
                else: 
                    attendance_report['absent']['absent_count'] += 1
                    attendance_report['absent']['details'].append(employeeworkingdate_idealcase)

            workingminutesperday = self.getFirstObjectIfExistOrNot(Workingminutesperday)
            penalty = (attendance_report['total_minutes']-attendance_report['attendance']['attendance_count']*workingminutesperday.working_minutes_per_day)/workingminutesperday.working_minutes_per_day
            attendance_report['penalty_based_on_total_minutes'] = penalty if penalty>=0 else 0
        else:
            in_a_row_late = 0
            in_a_row_late_details = {}
            for employeeworkingdate_idealcase in employeeworkingdates_idealcase:
                if employeeworkingdate_idealcase in employeeworkingdates_reality:

                    attendance = attendances.get(date=employeeworkingdate_idealcase)

                    attendance_report['attendance']['attendance_count'] += 1
                    if attendance.late_in_based_on_buffertime>0:
                        in_a_row_late += 1
                        
                        in_a_row_late_details.update(self.prepareDetailsAttendanceReport(employeeworkingdate_idealcase, attendance))
                        attendance_report['late_attendance_based_on_buffer_count'] += 1
                    else:
                        if consecutive:
                            in_a_row_late = 0
                            in_a_row_late_details = {}
                    if in_a_row_late == cost_in_days:
                        attendance_report['late_entry_fine']['fine_in_days'] += 1
                        attendance_report['late_entry_fine']['details'].update({f"{attendance_report['late_entry_fine']['fine_in_days']}": in_a_row_late_details})
                        in_a_row_late = 0
                        in_a_row_late_details = {}
                    if isinstance(attendance.total_minutes, float):
                        attendance_report['total_minutes'] += attendance.total_minutes

                    attendance_report['attendance']['details'].update(self.prepareDetailsAttendanceReport(employeeworkingdate_idealcase, attendance))
                else: 
                    attendance_report['absent']['absent_count'] += 1
                    attendance_report['absent']['details'].append(employeeworkingdate_idealcase)

            workingminutesperday = self.getFirstObjectIfExistOrNot(Workingminutesperday)
            penalty = (attendance_report['total_minutes']-attendance_report['attendance']['attendance_count']*workingminutesperday.working_minutes_per_day)/workingminutesperday.working_minutes_per_day
            attendance_report['penalty_based_on_total_minutes'] = penalty if penalty>=0 else 0

        return attendance_report
    
    def getPerdaySalary(self, PerdaySalary, FixedWorkingdaysinamonth, response, key):
        days = self.getFirstObjectIfExistOrNot(FixedWorkingdaysinamonth).days
        perdaysalarys = PerdaySalary.objects.all()
        perdaysalary = response[key]/days
        if perdaysalarys:
            perdaysalary = response[perdaysalarys[0].calculation_based_on.name]/days
        return perdaysalary
    
    def partitionSalary(self, Salaryallocation, response, salary_info):
        salaryallocations = Salaryallocation.objects.all()
        if salaryallocations:
            for salaryallocation in salaryallocations:
                response.update({f'{salaryallocation.name}': (salaryallocation.percentage*salary_info.gross_salary)/100})
    
    def generateLeaveCost(self, leaves, leave_cost, per_day_salary, CALCULATION_TYPE):
        for leave in leaves:
            if leave.leave_policy:
                if leave.leave_policy.paying_type:
                    if leave.leave_policy.paying_type.percentage_flat.pay_type == CALCULATION_TYPE[0][1]:
                        company = leave.leave_policy.paying_type.percentage_flat.company
                        employee = leave.leave_policy.paying_type.percentage_flat.employee

                        leave_cost['per_day_cost'] = per_day_salary
                        if isinstance(leave.leave_policy.cost_per_day, float):
                            company_will_bare = (company*per_day_salary*leave.leave_policy.cost_per_day)/100
                            employee_will_bare = (employee*per_day_salary*leave.leave_policy.cost_per_day)/100
                        else:
                            company_will_bare = (company*per_day_salary)/100
                            employee_will_bare = (employee*per_day_salary)/100

                        leave_cost['total_cost_of_employee'] += employee_will_bare
                        leave_cost['total_cost_of_company'] += company_will_bare
                        leave_cost['total_leave_taken'] += 1
                        leave_cost['details'].append({
                            'name': leave.leave_policy.name,
                            'company_will_bare': company_will_bare,
                            'employee_will_bare': employee_will_bare
                        })
                    elif leave.leave_policy.paying_type.percentage_flat.pay_type == CALCULATION_TYPE[1][1]:
                        company_will_bare = leave.leave_policy.paying_type.percentage_flat.company
                        employee_will_bare = leave.leave_policy.paying_type.percentage_flat.employee

                        leave_cost['total_cost_of_employee'] += employee_will_bare
                        leave_cost['total_cost_of_company'] += company_will_bare
                        
                        leave_cost['total_leave_taken'] += 1
                        leave_cost['details'].append({
                            'name': leave.leave_policy.name,
                            'company_will_bare': company_will_bare,
                            'employee_will_bare': employee_will_bare
                        })
    
    def getLoggedinUserid(self, User, username):
        user = User.objects.filter(username=username)
        info = None
        if user.exists():
            user = user.first()
            if hasattr(user, 'customuser'):
                custom_user = user.customuser
                if custom_user.active:
                    info = custom_user.id
        return info
    
    def ifallrecordsexistornot(self, classOBJ, idlist): # New
        flag = True
        if idlist:
            for id in idlist:
                object = self.getobject(classOBJ, {'id': id})
                if object == None: flag = False
        return flag
    
    def getuserdetails(self, classOBJpackage, createdInstance,  personalDetails, officialDetails, salaryAndLeaves, created_by): # New
        response = {'flag': True, 'message': [], 'data': {}}

        addbankaccountdetails = None
        if 'bank_account' in salaryAndLeaves:
            addbankaccountdetails=self.addbankaccount(classOBJpackage, salaryAndLeaves['bank_account'], createdInstance)
            if not addbankaccountdetails['flag']:
                response['message'].extend([f'user\'s {each}' for each in addbankaccountdetails['message']])
                response['flag'] = False
                addbankaccountdetails = None
        
        presentaddressdetails = None
        if 'present_address' in personalDetails:
            presentaddressdetails=self.addaddress(classOBJpackage['Address'], personalDetails['present_address'], createdInstance)
            if not presentaddressdetails['flag']:
                response['message'].extend([f'user present address\'s {each}' for each in presentaddressdetails['message']])
                response['flag'] = False
                presentaddressdetails = None
        
        permanentaddressdetails = None
        if 'permanent_address' in personalDetails:
            permanentaddressdetails=self.addaddress(classOBJpackage['Address'], personalDetails.get('permanent_address'), createdInstance)
            if not permanentaddressdetails['flag']:
                response['message'].extend([f'user permanet address {each}' for each in permanentaddressdetails['message']])
                response['flag'] = False
                permanentaddressdetails = None

        if response['flag']:
            fields_to_prepare_details_obj = self.prepareUserObjInfo(personalDetails, officialDetails, salaryAndLeaves)
            for each in fields_to_prepare_details_obj:
                self.ifExistThanAddToDict(each['obj'], each['field'], each['replace'], response['data'])

            religion = self.getobject(classOBJpackage['Religion'], {'id': personalDetails.get('religion')})
            if religion: response['data'].update({'religion': religion})
            if presentaddressdetails: response['data'].update({'present_address': presentaddressdetails['instance']})
            if permanentaddressdetails: response['data'].update({'permanent_address': permanentaddressdetails['instance']})
            designation = self.getobject(classOBJpackage['Designation'], {'id': officialDetails.get('designation')})
            if designation: response['data'].update({'designation': designation})
            shift = self.getobject(classOBJpackage['Shift'], {'id': officialDetails.get('shift')})
            if shift: response['data'].update({'shift': shift})
            grade = self.getobject(classOBJpackage['Grade'], {'id': officialDetails.get('grade')})
            if grade: response['data'].update({'grade': grade})
            supervisor = self.getobject(classOBJpackage['User'], {'id': officialDetails.get('supervisor')})
            if supervisor: response['data'].update({'supervisor': supervisor})
            expense_approver = self.getobject(classOBJpackage['User'], {'id': officialDetails.get('expense_approver')})
            if expense_approver: response['data'].update({'expense_approver': expense_approver})
            leave_approver = self.getobject(classOBJpackage['User'], {'id': officialDetails.get('leave_approver')})
            if leave_approver: response['data'].update({'leave_approver': leave_approver})
            shift_request_approver = self.getobject(classOBJpackage['User'], {'id': officialDetails.get('shift_request_approver')})
            if shift_request_approver: response['data'].update({'shift_request_approver': shift_request_approver})
            if addbankaccountdetails: response['data'].update({'bank_account': addbankaccountdetails['instance']})
            response['data'].update({'created_by': created_by, 'updated_by': created_by})
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
                if isinstance(object[field['field']], list):
                    if len(object[field['field']])>=1:
                        if object[field['field']][0]:
                            if field['type'] == 'str': mainObj.update({field['field']: object[field['field']][0]})
                            elif field['type'] == 'int': mainObj.update({field['field']: int(object[field['field']][0])})
                            elif field['type'] == 'bool':
                                value = True if object[field['field']][0].lower() == 'true' else False if object[field['field']][0].lower() == 'false' else None
                                if value != None: mainObj.update({field['field']: value})
                            elif field['type'] == 'list-int':
                                subList = []
                                for each in object[field['field']]:
                                    if each.isnumeric():
                                        if each not in subList: subList.append(int(each))
                                if subList: mainObj.update({field['field']: subList})
                            elif field['type'] == 'list-str':
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
                                if isinstance(object[nestedfield['field']][field['field']], list):
                                    if len(object[nestedfield['field']][field['field']])>=1:
                                        if object[nestedfield['field']][field['field']][0]:
                                            if field['type'] == 'str': subObj.update({field['field']: object[nestedfield['field']][field['field']][0]})
                                            elif field['type'] == 'int': subObj.update({field['field']: int(object[nestedfield['field']][field['field']][0])})
                                            elif field['type'] == 'bool':
                                                value = True if object[nestedfield['field']][field['field']][0].lower() == 'true' else False if object[nestedfield['field']][field['field']][0].lower() == 'false' else None
                                                if value != None: mainObj.update({field['field']: value})
                                            elif field['type'] == 'list-int':
                                                subList = []
                                                for each in object[nestedfield['field']][field['field']]:
                                                    if each.isnumeric():
                                                        if each not in subList: subList.append(int(each))
                                                if subList: mainObj.update({field['field']: subList})
                                            elif field['type'] == 'list-str':
                                                subList = []
                                                for each in object[nestedfield['field']][field['field']]:
                                                    if each:
                                                        if each not in subList: subList.append(each)
                                                if subList: mainObj.update({field['field']: subList})
                    if subObj: mainObj.update({nestedfield['field']: subObj})
        return mainObj if mainObj else None