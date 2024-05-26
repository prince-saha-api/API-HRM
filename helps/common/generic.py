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
    
    def preparepersonalDetails(self, personalDetails):
        if 'first_name' in personalDetails: personalDetails['first_name'] = personalDetails['first_name'][0]
        if 'last_name' in personalDetails: personalDetails['last_name'] = personalDetails['last_name'][0]
        if 'gender' in personalDetails: personalDetails['gender'] = personalDetails['gender'][0]
        if 'dob' in personalDetails: personalDetails['dob'] = personalDetails['dob'][0]
        if 'blood_group' in personalDetails: personalDetails['blood_group'] = personalDetails['blood_group'][0]
        if 'fathers_name' in personalDetails: personalDetails['fathers_name'] = personalDetails['fathers_name'][0]
        if 'mothers_name' in personalDetails: personalDetails['mothers_name'] = personalDetails['mothers_name'][0]
        if 'marital_status' in personalDetails: personalDetails['marital_status'] = personalDetails['marital_status'][0]
        if 'spouse_name' in personalDetails: personalDetails['spouse_name'] = personalDetails['spouse_name'][0]
        if 'nationality' in personalDetails: personalDetails['nationality'] = personalDetails['nationality'][0]
        if 'religion' in personalDetails:
            if personalDetails['religion'][0].isnumeric(): personalDetails['religion'] = int(personalDetails['religion'][0])
            else: personalDetails['religion'] = None
        if 'personal_email' in personalDetails: personalDetails['personal_email'] = personalDetails['personal_email'][0]
        if 'personal_phone' in personalDetails: personalDetails['personal_phone'] = personalDetails['personal_phone'][0]
        if 'nid_passport_no' in personalDetails: personalDetails['nid_passport_no'] = personalDetails['nid_passport_no'][0]
        if 'tin_no' in personalDetails: personalDetails['tin_no'] = personalDetails['tin_no'][0]
        if 'present_address' in personalDetails:
            if 'city' in personalDetails['present_address']: personalDetails['present_address']['city'] = personalDetails['present_address']['city'][0]
            if 'state_division' in personalDetails['present_address']: personalDetails['present_address']['state_division'] = personalDetails['present_address']['state_division'][0]
            if 'post_zip_code' in personalDetails['present_address']: personalDetails['present_address']['post_zip_code'] = personalDetails['present_address']['post_zip_code'][0]
            if 'country' in personalDetails['present_address']: personalDetails['present_address']['country'] = personalDetails['present_address']['country'][0]
            if 'address' in personalDetails['present_address']: personalDetails['present_address']['address'] = personalDetails['present_address']['address'][0]

        if 'permanent_address' in personalDetails:
            if 'city' in personalDetails['permanent_address']: personalDetails['permanent_address']['city'] = personalDetails['permanent_address']['city'][0]
            if 'state_division' in personalDetails['permanent_address']: personalDetails['permanent_address']['state_division'] = personalDetails['permanent_address']['state_division'][0]
            if 'post_zip_code' in personalDetails['permanent_address']: personalDetails['permanent_address']['post_zip_code'] = personalDetails['permanent_address']['post_zip_code'][0]
            if 'country' in personalDetails['permanent_address']: personalDetails['permanent_address']['country'] = personalDetails['permanent_address']['country'][0]
            if 'address' in personalDetails['permanent_address']: personalDetails['permanent_address']['address'] = personalDetails['permanent_address']['address'][0]

    def prepareofficialDetails(self, officialDetails):
        if 'official_id' in officialDetails: officialDetails['official_id'] = officialDetails['official_id'][0]
        if 'official_email' in officialDetails: officialDetails['official_email'] = officialDetails['official_email'][0]
        if 'official_phone' in officialDetails: officialDetails['official_phone'] = officialDetails['official_phone'][0]
        if 'password' in officialDetails: officialDetails['password'] = officialDetails['password'][0] if officialDetails['password'][0] else '123456'
        if 'employee_type' in officialDetails: officialDetails['employee_type'] = officialDetails['employee_type'][0]
        if 'company' in officialDetails:
            if officialDetails['company'][0].isnumeric(): officialDetails['company'] = int(officialDetails['company'][0])
            else: officialDetails['company'] = None
        if 'branch' in officialDetails:
            if officialDetails['branch'][0].isnumeric(): officialDetails['branch'] = int(officialDetails['branch'][0])
            else: officialDetails['branch'] = None
            
        if 'department' in officialDetails:
            if officialDetails['department'][0].isnumeric(): officialDetails['department'] = int(officialDetails['department'][0])
            else: officialDetails['department'] = None
            
        if 'designation' in officialDetails:
            if officialDetails['designation'][0].isnumeric(): officialDetails['designation'] = int(officialDetails['designation'][0])
            else: officialDetails['designation'] = None
            
        if 'shift' in officialDetails:
            if officialDetails['shift'][0].isnumeric(): officialDetails['shift'] = int(officialDetails['shift'][0])
            else: officialDetails['shift'] = None
            
        if 'grade' in officialDetails:
            if officialDetails['grade'][0].isnumeric(): officialDetails['grade'] = int(officialDetails['grade'][0])
            else: officialDetails['grade'] = None
            
        if 'role_permission' in officialDetails:
            permissions = []
            for permission in officialDetails['role_permission']:
                if permission.isnumeric(): permissions.append(int(permission))
            if permissions: officialDetails['role_permission'] = permissions
            else: officialDetails['role_permission'] = None

        if 'official_note' in officialDetails: officialDetails['official_note'] = officialDetails['official_note'][0]
        if 'ethnic_group' in officialDetails:
            groups = []
            for group in officialDetails['ethnic_group']:
                if group.isnumeric(): groups.append(int(group))
            if groups: officialDetails['ethnic_group'] = groups
            else: officialDetails['ethnic_group'] = None
            
        if 'joining_date' in officialDetails: officialDetails['joining_date'] = officialDetails['joining_date'][0]
        if 'supervisor' in officialDetails:
            if officialDetails['supervisor'][0].isnumeric(): officialDetails['supervisor'] = int(officialDetails['supervisor'][0])
            else: officialDetails['supervisor'] = None
            
        if 'expense_approver' in officialDetails:
            if officialDetails['expense_approver'][0].isnumeric(): officialDetails['expense_approver'] = int(officialDetails['expense_approver'][0])
            else: officialDetails['expense_approver'] = None
            
        if 'leave_approver' in officialDetails:
            if officialDetails['leave_approver'][0].isnumeric(): officialDetails['leave_approver'] = int(officialDetails['leave_approver'][0])
            else: officialDetails['leave_approver'] = None
            
        if 'shift_request_approver' in officialDetails:
            if officialDetails['shift_request_approver'][0].isnumeric(): officialDetails['shift_request_approver'] = int(officialDetails['shift_request_approver'][0])
            else: officialDetails['shift_request_approver'] = None
            

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

    def prepareemergencyContact(self, emergencyContact):
        if emergencyContact:
            if isinstance(emergencyContact, list):
                for index, each in enumerate(emergencyContact):
                    if 'name' in each: emergencyContact[index]['name'] = each['name'][0]
                    if 'age' in each: emergencyContact[index]['age'] = each['age'][0]
                    if 'phone_no' in each: emergencyContact[index]['phone_no'] = each['phone_no'][0]
                    if 'email' in each: emergencyContact[index]['email'] = each['email'][0]
                    if 'address' in each:
                        if 'city' in each['address']: emergencyContact[index]['address']['city'] = each['address']['city'][0]
                        if 'state_division' in each['address']: emergencyContact[index]['address']['state_division'] = each['address']['state_division'][0]
                        if 'post_zip_code' in each['address']: emergencyContact[index]['address']['post_zip_code'] = each['address']['post_zip_code'][0]
                        if 'country' in each['address']: emergencyContact[index]['address']['country'] = each['address']['country'][0]
                        if 'address' in each['address']: emergencyContact[index]['address']['address'] = each['address']['address'][0]

    def prepareacademicRecord(self, academicRecord):
        if academicRecord:
            if isinstance(academicRecord, list):
                for index, each in enumerate(academicRecord):
                    if 'certification' in each: academicRecord[index]['certification'] = each['certification'][0]
                    if 'board_institute_name' in each: academicRecord[index]['board_institute_name'] = each['board_institute_name'][0]
                    if 'level' in each: academicRecord[index]['level'] = each['level'][0]
                    if 'score_grade' in each: academicRecord[index]['score_grade'] = each['score_grade'][0]
                    if 'year_of_passing' in each: academicRecord[index]['year_of_passing'] = each['year_of_passing'][0]

    def preparepreviousExperience(self, previousExperience):
        if previousExperience:
            if isinstance(previousExperience, list):
                for index, each in enumerate(previousExperience):
                    if 'company_name' in each: previousExperience[index]['company_name'] = each['company_name'][0]
                    if 'designation' in each: previousExperience[index]['designation'] = each['designation'][0]
                    if 'address' in each: previousExperience[index]['address'] = each['address'][0]
                    if 'from_date' in each: previousExperience[index]['from_date'] = each['from_date'][0]
                    if 'to_date' in each: previousExperience[index]['to_date'] = each['to_date'][0]


    def createuser(self, classOBJpackage, personalDetails, officialDetails, salaryAndLeaves, modelsuniquefields):
        response = {
            'flag': True,
            'message': []
        }
        details = self.getuserdetails(classOBJpackage, personalDetails, officialDetails, salaryAndLeaves)
        if not details['flag']:
            response['message'].extend([f'user - {each}' for each in details['message']])
            response['flag'] = False
        
        uniquefiels = self.isuniquefielsexist(classOBJpackage['User'], details['data'], modelsuniquefields)
        if uniquefiels['flag']:
            response['message'].extend(uniquefiels['message'])
            response['flag'] = False

        if response['flag']: response.update({'userinstance': self.createuserinstance(classOBJpackage['User'], details['data'])})

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