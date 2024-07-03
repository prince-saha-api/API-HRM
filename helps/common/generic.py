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
    
    def prepareData(self, objects, fieldsname):
        preparedData = []

        if fieldsname == 'personal': fields = self.getPresonalData()
        elif fieldsname == 'office': fields = self.getOfficeData()
        elif fieldsname == 'salaryleaves': fields = self.getSalaryLeavesData()
        elif fieldsname == 'emergencycontact': fields = self.getEmergencyContactData()
        elif fieldsname == 'academicrecord': fields = self.getAcademicRecordData()
        elif fieldsname == 'previousexperience': fields = self.getPreviousExperienceData()

        if isinstance(objects, dict):
            preparedData.append(self.getOBJDetails(objects, fields))

        if isinstance(objects, list):
            carrierList = []
            for object in objects:
                preparedObj = self.getOBJDetails(object, fields)
                if preparedObj: carrierList.append(preparedObj)
            if carrierList: preparedData.append(carrierList)

        return preparedData[0] if preparedData else None
    
    def preparesalaryAndLeaves(self, salaryAndLeaves):
        if 'payment_in' in salaryAndLeaves: salaryAndLeaves['payment_in'] = salaryAndLeaves['payment_in'][0]
        if 'gross_salary' in salaryAndLeaves: salaryAndLeaves['gross_salary'] = salaryAndLeaves['gross_salary'][0]
        if 'leavepolicy' in salaryAndLeaves:
            leaves = []
            for leave in salaryAndLeaves['leavepolicy']:
                if leave.isnumeric(): leaves.append(int(leave))
            if leaves: salaryAndLeaves['leavepolicy'] = leaves
            else: salaryAndLeaves['leavepolicy'] = None
            

        if 'bank_account' in salaryAndLeaves:
            if 'bank_name' in salaryAndLeaves['bank_account']: salaryAndLeaves['bank_account']['bank_name'] = salaryAndLeaves['bank_account']['bank_name'][0]
            if 'branch_name' in salaryAndLeaves['bank_account']: salaryAndLeaves['bank_account']['branch_name'] = salaryAndLeaves['bank_account']['branch_name'][0]
            if 'account_type' in salaryAndLeaves['bank_account']: salaryAndLeaves['bank_account']['account_type'] = salaryAndLeaves['bank_account']['account_type'][0]
            if 'account_no' in salaryAndLeaves['bank_account']: salaryAndLeaves['bank_account']['account_no'] = salaryAndLeaves['bank_account']['account_no'][0]
            if 'routing_no' in salaryAndLeaves['bank_account']: salaryAndLeaves['bank_account']['routing_no'] = salaryAndLeaves['bank_account']['routing_no'][0]
            if 'swift_bic' in salaryAndLeaves['bank_account']: salaryAndLeaves['bank_account']['swift_bic'] = salaryAndLeaves['bank_account']['swift_bic'][0]
            if 'address' in salaryAndLeaves['bank_account']:
                if 'city' in salaryAndLeaves['bank_account']['address']: salaryAndLeaves['bank_account']['address']['city'] = salaryAndLeaves['bank_account']['address']['city'][0]
                if 'state_division' in salaryAndLeaves['bank_account']['address']: salaryAndLeaves['bank_account']['address']['state_division'] = salaryAndLeaves['bank_account']['address']['state_division'][0]
                if 'post_zip_code' in salaryAndLeaves['bank_account']['address']: salaryAndLeaves['bank_account']['address']['post_zip_code'] = salaryAndLeaves['bank_account']['address']['post_zip_code'][0]
                if 'country' in salaryAndLeaves['bank_account']['address']: salaryAndLeaves['bank_account']['address']['country'] = salaryAndLeaves['bank_account']['address']['country'][0]
                if 'address' in salaryAndLeaves['bank_account']['address']: salaryAndLeaves['bank_account']['address']['address'] = salaryAndLeaves['bank_account']['address']['address'][0]


    def createuser(self, classOBJpackage, serializerOBJpackage, createdInstance, personalDetails, officialDetails, salaryAndLeaves, photo, usermodelsuniquefields, required_fields, created_by):
        response = {'flag': True, 'message': []}
        details = self.getuserdetails(classOBJpackage, serializerOBJpackage, createdInstance, personalDetails, officialDetails, salaryAndLeaves, created_by)
        if not details['flag']:
            response['message'].extend(details['message'])
            response['flag'] = False
        # required fields are checking
        for required_field in required_fields:
            if required_field in details['data']:
                if not bool(details['data'][required_field]):
                    response['message'].append(f'user\'s {required_field} field is required!')
                    response['flag'] = False
            else:
                response['message'].append(f'user\'s {required_field} field is required!')
                response['flag'] = False
        
        # unique fields are checking
        uniquefiels = self.isuniquefielsexist(classOBJpackage['User'], details['data'], usermodelsuniquefields)
        if uniquefiels['flag']:
            response['message'].extend([f'user\'s {each}' for each in uniquefiels['message']])
            response['flag'] = False

        if response['flag']:
            userinstance_response = self.createuserinstance(classOBJpackage['User'], details['data'], photo)
            if userinstance_response['flag']: response.update({'userinstance': userinstance_response['instance']})
            else:
                response['flag'] = False
                response['message'].append('couldn\'t create user instance, something went wrong!')
        return response
    
    def generateuserobject(self, data):
        datakeys = data.keys()
        userdetails = {
            'personalDetails': {},
            'officialDetails': {},
            'salaryAndLeaves': {},
            'emergencyContact': {},
            'academicRecord': {},
            'previousExperience': {},
            'uploadDocuments': {}
        }
        for key in datakeys:
            if 'personalDetails' in key:
                userdetails['personalDetails'].update({key.replace('personalDetails', ''): data[key]})
            elif 'officialDetails' in key:
                userdetails['officialDetails'].update({key.replace('officialDetails', ''): data[key]})
            elif 'salaryAndLeaves' in key:
                userdetails['salaryAndLeaves'].update({key.replace('salaryAndLeaves', ''): data[key]})
            elif 'emergencyContact' in key:
                userdetails['emergencyContact'].update({key.replace('emergencyContact', ''): data[key]})
            elif 'academicRecord' in key:
                userdetails['academicRecord'].update({key.replace('academicRecord', ''): data[key]})
            elif 'previousExperience' in key:
                userdetails['previousExperience'].update({key.replace('previousExperience', ''): data[key]})
            elif 'uploadDocuments' in key:
                userdetails['uploadDocuments'].update({key.replace('uploadDocuments', ''): data[key]})

        return userdetails