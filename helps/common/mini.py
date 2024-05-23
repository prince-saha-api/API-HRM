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
            'first_name': personalDetails.get('first_name'),
            'last_name': personalDetails.get('last_name'),
            'gender': personalDetails.get('gender'),
            'dob': personalDetails.get('dob'),
            'blood_group': personalDetails.get('blood_group'),
            'fathers_name': personalDetails.get('fathers_name'),
            'mothers_name': personalDetails.get('mothers_name'),
            'marital_status': personalDetails.get('marital_status'),
            'spouse_name': personalDetails.get('spouse_name'),
            'nationality': personalDetails.get('nationality'),
            'religion': self.getobject(classOBJpackage['Religion'], personalDetails.get('religion')),
            'personal_email': personalDetails.get('personal_email'),
            'personal_phone': personalDetails.get('personal_phone'),
            'nid_passport_no': personalDetails.get('nid_passport_no'),
            'tin_no': personalDetails.get('tin_no'),
            'present_address': self.addaddress(classOBJpackage['Address'], personalDetails.get('present_address')),
            'permanent_address': self.addaddress(classOBJpackage['Address'], personalDetails.get('permanent_address')),
            'official_id': officialDetails.get('official_id'),
            'official_email': officialDetails.get('official_email'),
            'official_phone': officialDetails.get('official_phone'),
            'password': make_password(officialDetails.get('password')),
            'employee_type': officialDetails.get('employee_type'),
            'designation': self.getobject(classOBJpackage['Designation'], officialDetails.get('designation')),
            'shift': self.getobject(classOBJpackage['Shift'], officialDetails.get('shift')),
            'grade': self.getobject(classOBJpackage['Grade'], officialDetails.get('grade')),
            'official_note': officialDetails.get('official_note'),
            'joining_date': officialDetails.get('joining_date'),
            'supervisor': self.getobject(classOBJpackage['User'], officialDetails.get('supervisor')),
            'expense_approver': self.getobject(classOBJpackage['User'], officialDetails.get('expense_approver')),
            'leave_approver': self.getobject(classOBJpackage['User'], officialDetails.get('leave_approver')),
            'shift_request_approver': self.getobject(classOBJpackage['User'], officialDetails.get('shift_request_approver')),
            'payment_in': salaryAndLeaves.get('payment_in'),
            'bank_account': self.addbankaccount(classOBJpackage, salaryAndLeaves.get('bank_account')),
            'gross_salary': salaryAndLeaves.get('gross_salary')
        }
    
    def createuserinstance(self, User, details): # New
        userinstance = User()
        userinstance.username=details['official_id']
        if details['first_name']: userinstance.first_name=details['first_name']
        if details['last_name']: userinstance.last_name=details['last_name']
        if details['gender']: userinstance.gender=details['gender']
        if details['dob']: userinstance.dob=details['dob']
        if details['blood_group']: userinstance.blood_group=details['blood_group']
        if details['fathers_name']: userinstance.fathers_name=details['fathers_name']
        if details['mothers_name']: userinstance.mothers_name=details['mothers_name']
        if details['marital_status']: userinstance.marital_status=details['marital_status']
        if details['spouse_name']: userinstance.spouse_name=details['spouse_name']
        if details['nationality']: userinstance.nationality=details['nationality']
        if details['religion']: userinstance.religion=details['religion']
        if details['personal_email']: userinstance.personal_email=details['personal_email']
        if details['personal_phone']: userinstance.personal_phone=details['personal_phone']
        if details['nid_passport_no']: userinstance.nid_passport_no=details['nid_passport_no']
        if details['tin_no']: userinstance.tin_no=details['tin_no']
        if details['present_address']: userinstance.present_address=details['present_address']
        if details['permanent_address']: userinstance.permanent_address=details['permanent_address']
        userinstance.dummy_salary=random.randint(5000,300000)
        if details['official_id']: userinstance.official_id=details['official_id']
        if details['official_email']: userinstance.official_email=details['official_email']
        if details['official_phone']: userinstance.official_phone=details['official_phone']
        if details['password']: userinstance.password=details['password']
        if details['employee_type']: userinstance.employee_type=details['employee_type']
        if details['designation']: userinstance.designation=details['designation']
        if details['shift']: userinstance.shift=details['shift']
        if details['grade']: userinstance.grade=details['grade']
        if details['official_note']: userinstance.official_note=details['official_note']
        if details['joining_date']: userinstance.joining_date=details['joining_date']
        if details['supervisor']: userinstance.supervisor=details['supervisor']
        if details['expense_approver']: userinstance.expense_approver=details['expense_approver']
        if details['leave_approver']: userinstance.leave_approver=details['leave_approver']
        if details['shift_request_approver']: userinstance.shift_request_approver=details['shift_request_approver']
        if details['payment_in']: userinstance.payment_in=details['payment_in']
        if details['bank_account']: userinstance.bank_account=details['bank_account']
        if details['gross_salary']: userinstance.gross_salary=details['gross_salary']
        userinstance.save()

        return userinstance