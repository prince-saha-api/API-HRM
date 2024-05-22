import random
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
    
    # def getEmployeeWorkingDatesIdealCase(self, Holiday, Offday, customuser, daysinmonth, year, month):
    #     employeeworkingdates = []
    #     applicableholidays = self.getApplicableHolidayDates(Holiday, customuser)
    #     for day in range(1, daysinmonth+1):
    #         if self.isWorkingDayAccordingToOfficeOffDay(Offday, year, month, day):
    #             date = self.convert_STR_STR_y_m_d(year, month, day)
    #             if date not in applicableholidays:
    #                 employeeworkingdates.append(date)
    #     return employeeworkingdates
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
                object = self.getobject(classOBJ, id)
                if object == None: flag = False
        return flag
    
    def getuserdetails(self, classOBJpackage, personalDetails, officialDetails, salaryAndLeaves): # New
        return {
            'first_name_personalDetails': personalDetails.get('first_name'),
            'last_name_personalDetails': personalDetails.get('last_name'),
            'gender_personalDetails': personalDetails.get('gender'),
            'dob_personalDetails': personalDetails.get('dob'),
            'blood_group_personalDetails': personalDetails.get('blood_group'),
            'fathers_name_personalDetails': personalDetails.get('fathers_name'),
            'mothers_name_personalDetails': personalDetails.get('mothers_name'),
            'marital_status_personalDetails': personalDetails.get('marital_status'),
            'spouse_name_personalDetails': personalDetails.get('spouse_name'),
            'nationality_personalDetails': personalDetails.get('nationality'),
            'religion_personalDetails': self.getobject(classOBJpackage['Religion'], personalDetails.get('religion')),
            'personal_email_personalDetails': personalDetails.get('personal_email'),
            'personal_phone_personalDetails': personalDetails.get('personal_phone'),
            'nid_passport_no_personalDetails': personalDetails.get('nid_passport_no'),
            'tin_no_personalDetails': personalDetails.get('tin_no'),
            'present_address_personalDetails': self.addaddress(classOBJpackage['Address'], personalDetails.get('present_address')),
            'permanent_address_personalDetails': self.addaddress(classOBJpackage['Address'], personalDetails.get('permanent_address')),
            'official_id_officialDetails': officialDetails.get('official_id'),
            'official_email_officialDetails': officialDetails.get('official_email'),
            'official_phone_officialDetails': officialDetails.get('official_phone'),
            'password_officialDetails': officialDetails.get('password'),
            'employee_type_officialDetails': officialDetails.get('employee_type'),
            'designation_officialDetails': self.getobject(classOBJpackage['Designation'], officialDetails.get('designation')),
            'shift_officialDetails': self.getobject(classOBJpackage['Shift'], officialDetails.get('shift')),
            'grade_officialDetails': self.getobject(classOBJpackage['Grade'], officialDetails.get('grade')),
            'official_note_officialDetails': officialDetails.get('official_note'),
            'joining_date_officialDetails': officialDetails.get('joining_date'),
            'supervisor_officialDetails': self.getobject(classOBJpackage['User'], officialDetails.get('supervisor')),
            'expense_approver_officialDetails': self.getobject(classOBJpackage['User'], officialDetails.get('expense_approver')),
            'leave_approver_officialDetails': self.getobject(classOBJpackage['User'], officialDetails.get('leave_approver')),
            'shift_request_approver_officialDetails': self.getobject(classOBJpackage['User'], officialDetails.get('shift_request_approver')),
            'payment_in_salaryAndLeaves': salaryAndLeaves.get('payment_in'),
            'bank_account_salaryAndLeaves': self.addbankaccount(classOBJpackage, salaryAndLeaves.get('bank_account')),
            'gross_salary_salaryAndLeaves': salaryAndLeaves.get('gross_salary')
        }
    
    def createuserinstance(self, User, details): # New
        userinstance = User()
        userinstance.username=details['official_id_officialDetails']
        if details['first_name_personalDetails']: userinstance.first_name=details['first_name_personalDetails']
        if details['last_name_personalDetails']: userinstance.last_name=details['last_name_personalDetails']
        if details['gender_personalDetails']: userinstance.gender=details['gender_personalDetails']
        if details['dob_personalDetails']: userinstance.dob=details['dob_personalDetails']
        if details['blood_group_personalDetails']: userinstance.blood_group=details['blood_group_personalDetails']
        if details['fathers_name_personalDetails']: userinstance.fathers_name=details['fathers_name_personalDetails']
        if details['mothers_name_personalDetails']: userinstance.mothers_name=details['mothers_name_personalDetails']
        if details['marital_status_personalDetails']: userinstance.marital_status=details['marital_status_personalDetails']
        if details['spouse_name_personalDetails']: userinstance.spouse_name=details['spouse_name_personalDetails']
        if details['nationality_personalDetails']: userinstance.nationality=details['nationality_personalDetails']
        if details['religion_personalDetails']: userinstance.religion=details['religion_personalDetails']
        if details['personal_email_personalDetails']: userinstance.personal_email=details['personal_email_personalDetails']
        if details['personal_phone_personalDetails']: userinstance.personal_phone=details['personal_phone_personalDetails']
        if details['nid_passport_no_personalDetails']: userinstance.nid_passport_no=details['nid_passport_no_personalDetails']
        if details['tin_no_personalDetails']: userinstance.tin_no=details['tin_no_personalDetails']
        if details['present_address_personalDetails']: userinstance.present_address=details['present_address_personalDetails']
        if details['permanent_address_personalDetails']: userinstance.permanent_address=details['permanent_address_personalDetails']
        userinstance.dummy_salary=random.randint(5000,300000)
        if details['official_id_officialDetails']: userinstance.official_id=details['official_id_officialDetails']
        if details['official_email_officialDetails']: userinstance.official_email=details['official_email_officialDetails']
        if details['official_phone_officialDetails']: userinstance.official_phone=details['official_phone_officialDetails']
        if details['password_officialDetails']: userinstance.password=details['password_officialDetails']
        if details['employee_type_officialDetails']: userinstance.employee_type=details['employee_type_officialDetails']
        if details['designation_officialDetails']: userinstance.designation=details['designation_officialDetails']
        if details['shift_officialDetails']: userinstance.shift=details['shift_officialDetails']
        if details['grade_officialDetails']: userinstance.grade=details['grade_officialDetails']
        if details['official_note_officialDetails']: userinstance.official_note=details['official_note_officialDetails']
        if details['joining_date_officialDetails']: userinstance.joining_date=details['joining_date_officialDetails']
        if details['supervisor_officialDetails']: userinstance.supervisor=details['supervisor_officialDetails']
        if details['expense_approver_officialDetails']: userinstance.expense_approver=details['expense_approver_officialDetails']
        if details['leave_approver_officialDetails']: userinstance.leave_approver=details['leave_approver_officialDetails']
        if details['shift_request_approver_officialDetails']: userinstance.shift_request_approver=details['shift_request_approver_officialDetails']
        if details['payment_in_salaryAndLeaves']: userinstance.payment_in=details['payment_in_salaryAndLeaves']
        if details['bank_account_salaryAndLeaves']: userinstance.bank_account=details['bank_account_salaryAndLeaves']
        if details['gross_salary_salaryAndLeaves']: userinstance.gross_salary=details['gross_salary_salaryAndLeaves']
        userinstance.save()

        return userinstance