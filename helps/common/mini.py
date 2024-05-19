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