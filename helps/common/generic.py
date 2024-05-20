from rest_framework import status

from helps.common.mini import Minihelps
import calendar

class Generichelps(Minihelps):

    def getPermissionsList(self, User, username, permissions, all=False, active=False, inactive=False):
        if all + active + inactive == 1:
            user = User.objects.filter(username=username)
            if user.exists():
                user = user.first()
                if user.is_active:
                    if all: self.getPermissionsListIfAll(permissions, user)
                    elif active: self.getPermissionsListIfActiveOrInactive(permissions, user, True)
                    else: self.getPermissionsListIfActiveOrInactive(permissions, user, False)

    def filterClass(self, Object, request, extra_conditions={}):
        kwargs={}
        for key in request.GET.keys():
            if request.GET[key]:
                if key in extra_conditions: kwargs.update({'{0}__{1}'.format(key, extra_conditions[key]): request.GET[key]})
                else: kwargs.update({'{0}'.format(key): request.GET[key]})
        objects = Object.objects.filter(**kwargs)
        return objects
    
    def getHoliday(self, Holiday, date, employee):
        holiday = Holiday.objects.filter(date=date, is_active=True, priority=True)
        if employee.religion:
            if holiday:
                if holiday[0].only_aplicable_for.all():
                    if not holiday[0].only_aplicable_for.filter(name=employee.religion.name): holiday = None
            else: holiday = None
        else:
            if holiday[0].only_aplicable_for.all(): holiday = None
        return holiday

    def calculateDynamicCost(self, Costtitle, applicable_deduction, response, salary_info):
        for deduction in applicable_deduction:
            costtitle = Costtitle.objects.filter(id=deduction, is_active=True)
            if costtitle.exists():
                costtitle = costtitle.first()
                subcosttitles = costtitle.subcosttitle_set.all()
                if subcosttitles:
                    if subcosttitles.count() == 1:
                        response['deduction'].update({costtitle.title.replace(' ', '_').lower(): subcosttitles.first().cost})
                        response['payable_salary'] -= subcosttitles.first().cost
                    else:
                        # range_start <= salary_info.gross_salary <= range_end
                        subcosttitle = subcosttitles.filter(range_start__lte=salary_info.gross_salary, range_end__gte=salary_info.gross_salary).first()
                        if not bool(subcosttitle):
                            subcosttitle = subcosttitles.filter(range_start__gte=salary_info.gross_salary, range_end__gte=salary_info.gross_salary).order_by('range_end')
                            if not bool(subcosttitle):
                                subcosttitle = subcosttitles.order_by('-range_end').first()
                        if subcosttitle.cost:
                            response['deduction'].update({costtitle.title.replace(' ', '_').lower(): subcosttitle.cost})
                            response['payable_salary'] -= subcosttitle.cost

    def calculateLeaveCost(self, Leave, LeaveConfig, FixedWorkingdaysinamonth, salary_info, response, CALCULATION_TYPE, id):
        leaves = Leave.objects.filter(custom_user__id=id)
        leave_cost = self.generateOBJLeaveCost()

        if leaves:
            leaveconfig = LeaveConfig.objects.all()
            days = self.getFirstObjectIfExistOrNot(FixedWorkingdaysinamonth).days
            if leaveconfig:
                per_day_salary = response.get(leaveconfig[0].calculation_based_on.name)/days
                self.generateLeaveCost(leaves, leave_cost, per_day_salary, CALCULATION_TYPE)
            else:
                per_day_salary = salary_info.gross_salary/days
                self.generateLeaveCost(leaves, leave_cost, per_day_salary, CALCULATION_TYPE)
        response['deduction']['leave_cost'] = leave_cost
        response['payable_salary'] -= response['deduction']['leave_cost']['total_cost_of_employee']
    
    # def calculateAttendanceCost(self, Attendance, Holiday, Offday, PerdaySalary, FixedWorkingdaysinamonth, Workingminutesperday, Latefineforfewdays, response, customuser, year, month, id):
    #     flag = False
    #     first_day_index, daysinmonth = calendar.monthrange(year, month)
    #     attendances = Attendance.objects.filter(employee__id=id, date__gte=f'{year}-{month}-{first_day_index+1}', date__lte=f'{year}-{month}-{daysinmonth}').order_by('date')
    #     if attendances:
    #         employeeworkingdates_idealcase = self.getEmployeeWorkingDatesIdealCase(Holiday, Offday, customuser, daysinmonth, year, month)
    #         employeeworkingdates_reality = [self.convertDateformat_STR_y_m_d(attendance.date) for attendance in attendances]
    #         attendance_report = self.generateAttendanceReport(Workingminutesperday, Latefineforfewdays, len(employeeworkingdates_idealcase), employeeworkingdates_idealcase, employeeworkingdates_reality, attendances)
    #         perdaysalary = self.getPerdaySalary(PerdaySalary, FixedWorkingdaysinamonth, response, 'gross_salary')

    #         response['deduction']['attendance_cost']['cost'] = (attendance_report['penalty_based_on_total_minutes']+attendance_report['absent']['absent_count']+attendance_report['late_entry_fine']['fine_in_days'])*perdaysalary
    #         response['deduction']['attendance_cost']['penalty_based_on_total_minutes'] = attendance_report['penalty_based_on_total_minutes']
    #         response['deduction']['attendance_cost']['absent']['absent_count'] = attendance_report['absent']['absent_count']
    #         response['deduction']['attendance_cost']['absent']['details'] = attendance_report['absent']['details']
    #         response['deduction']['attendance_cost']['fine_in_days']['fine_count'] = attendance_report['late_entry_fine']['fine_in_days']
    #         response['deduction']['attendance_cost']['fine_in_days']['details'] = attendance_report['late_entry_fine']['details']
    #         response['payable_salary'] -= response['deduction']['attendance_cost']['cost']
    #         flag = True
    #     return flag

    def calculateAttendanceCost(self, Attendance, Offday, PerdaySalary, FixedWorkingdaysinamonth, Workingminutesperday, Latefineforfewdays, response, customuser, year, month, id):
        flag = False
        first_day_index, daysinmonth = calendar.monthrange(year, month)
        attendances = Attendance.objects.filter(employee__id=id, date__gte=f'{year}-{month}-{first_day_index+1}', date__lte=f'{year}-{month}-{daysinmonth}').order_by('date')
        if attendances:
            employeeworkingdates_idealcase = self.getEmployeeWorkingDatesIdealCase(Offday, customuser, daysinmonth, year, month)
            employeeworkingdates_reality = [self.convertDateformat_STR_y_m_d(attendance.date) for attendance in attendances]
            attendance_report = self.generateAttendanceReport(Workingminutesperday, Latefineforfewdays, len(employeeworkingdates_idealcase), employeeworkingdates_idealcase, employeeworkingdates_reality, attendances)
            perdaysalary = self.getPerdaySalary(PerdaySalary, FixedWorkingdaysinamonth, response, 'gross_salary')

            response['deduction']['attendance_cost']['cost'] = (attendance_report['penalty_based_on_total_minutes']+attendance_report['absent']['absent_count']+attendance_report['late_entry_fine']['fine_in_days'])*perdaysalary
            response['deduction']['attendance_cost']['penalty_based_on_total_minutes'] = attendance_report['penalty_based_on_total_minutes']
            response['deduction']['attendance_cost']['absent']['absent_count'] = attendance_report['absent']['absent_count']
            response['deduction']['attendance_cost']['absent']['details'] = attendance_report['absent']['details']
            response['deduction']['attendance_cost']['fine_in_days']['fine_count'] = attendance_report['late_entry_fine']['fine_in_days']
            response['deduction']['attendance_cost']['fine_in_days']['details'] = attendance_report['late_entry_fine']['details']
            response['payable_salary'] -= response['deduction']['attendance_cost']['cost']
            flag = True
        return flag
    
    def calculateBonus(self, Bonus, id, response, year, month):
        bonuses = Bonus.objects.filter(custom_user__id=id, year=year, month=month, is_active=True)
        amount = 0
        bonus_details = []
        if bonuses:
            for bonus in bonuses:
                bonus_details.append({
                    'title': bonus.title,
                    'type': bonus.type,
                    'percentage': bonus.percentage,
                    'amount': bonus.amount,
                    'reason': bonus.reason,
                    'year': bonus.year,
                    'month': bonus.month
                })
                amount += bonus.amount
        response['earnings'].update({'bonus': bonus_details})
        response['earnings']['total_earnings'] += amount
        response['payable_salary'] += response['earnings']['total_earnings']
    
    def storepaymentrecord(self, Paymentrecord, User, username, response, user, year, month):
        flag=True
        if not Paymentrecord.objects.filter(salary_year=year,salary_month=month,salary_pay_to=user).exists():
            created_by = self.getLoggedinUserid(User, username)
            Paymentrecord.objects.create(
                salary_year=year,
                salary_month=month,
                salary_gross=response['gross_salary'],
                salary_paid=response['payable_salary'],
                salary_deduction=response['gross_salary'] - response['payable_salary'],
                salary_pay_to=user,
                created_by=created_by,
                updated_by=created_by,
                details=response
                )
        else: flag=False
        return flag

    def set_settings(self, ConfigClass, BackupClass, code):
        will_be_deleted_after_nth_records = self.getFirstObjectIfExistOrNot(ConfigClass).backup_will_be_deleted_after_nth_records
        backupclass = BackupClass.objects.filter(code=code).order_by('-id')
        if backupclass.count()>will_be_deleted_after_nth_records-1:
            objects_to_keep = backupclass[:will_be_deleted_after_nth_records-1]
            backupclass.exclude(pk__in=objects_to_keep).delete()
        return code
    
    def getattendancedetails(self, GlobalBufferTime, Offday, shift, date, actual_in_time, actual_out_time):

        shiftandactualinoutdetails = self.getshiftandactualinoutdetails(shift, actual_in_time, actual_out_time)
        flag_details = self.claculateinoutflag(shiftandactualinoutdetails)
        entranceexitdetails = self.claculateentranceexitdetails(flag_details, shiftandactualinoutdetails)
        ateattendancedetails = self.claculateattendancedetails(entranceexitdetails)
        bufferdetails = self.claculatebuffertime(GlobalBufferTime, entranceexitdetails)

        offday = self.getofficeoffday(Offday, date)
        
        total_minutes = ((shiftandactualinoutdetails['actual_out_time']-shiftandactualinoutdetails['actual_in_time']).total_seconds())/60
        total_minutes -=ateattendancedetails['in_positive_minutes']
        total_minutes -=ateattendancedetails['out_positive_minutes']

        return {
            'in_negative_minutes': ateattendancedetails['in_negative_minutes'],
            'in_positive_minutes': ateattendancedetails['in_positive_minutes'],
            'out_negative_minutes': ateattendancedetails['out_negative_minutes'],
            'out_positive_minutes': ateattendancedetails['out_positive_minutes'],
            'late_in_based_on_buffertime': bufferdetails['late_in_based_on_buffertime'],
            'early_leave_based_on_buffertime': bufferdetails['early_leave_based_on_buffertime'],
            'buffer_time_minutes': bufferdetails['buffer_time_minutes'],
            'total_minutes': total_minutes,
            'office_off_day': offday
        } 
    
    def addtocolass(self, classOBJ, classSrializer, data, unique):
        unique_value = data.get(unique)
        response_data = {}
        response_message = ''
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        if unique_value:
            if not classOBJ.objects.filter(**{unique:unique_value}).exists():
                classsrializer = classSrializer(data=data, many=False)
                if classsrializer.is_valid():
                    classsrializer.save()
                    response_data = classsrializer.data
                    response_successflag = 'success'
                    response_status = status.HTTP_201_CREATED
            else: response_message = f'this {unique_value} already exist!'
        else: response_message = f'{unique_value} is required!'

        return response_data, response_message, response_successflag, response_status
