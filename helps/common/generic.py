from helps.common.mini import Minihelps
from datetime import datetime, date, timedelta
from helps.choice import common as CHOICE
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
    
    def prepareData(self, objects, fieldsname): # New
        preparedData = []

        if fieldsname == 'personal': fields = self.getPresonalData()
        elif fieldsname == 'office': fields = self.getOfficeData()
        elif fieldsname == 'salaryleaves': fields = self.getSalaryLeavesData()
        elif fieldsname == 'emergencycontact': fields = self.getEmergencyContactData()
        elif fieldsname == 'academicrecord': fields = self.getAcademicRecordData()
        elif fieldsname == 'previousexperience': fields = self.getPreviousExperienceData()
        elif fieldsname == 'basicinfo': fields = self.getBasicInfoData()
        elif fieldsname == 'userdocument': fields = self.getUserDocumentData()
        elif fieldsname == 'noticeboard': fields = self.getNoticeBoardData()

        if isinstance(objects, dict):
            preparedData.append(self.getOBJDetails(objects, fields))

        if isinstance(objects, list):
            carrierList = []
            for object in objects:
                preparedObj = self.getOBJDetails(object, fields)
                if preparedObj: carrierList.append(preparedObj)
            if carrierList: preparedData.append(carrierList)

        return preparedData[0] if preparedData else None
    
    def preparesalaryAndLeaves(self, salaryAndLeaves): # New
        if salaryAndLeaves:
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


    def createuser(self, classOBJpackage, serializerOBJpackage, createdInstance, personalDetails, officialDetails, salaryAndLeaves, photo, created_by): # New
        response = {'flag': True, 'message': []}
        
        details = self.getuserdetails(classOBJpackage, serializerOBJpackage, createdInstance, personalDetails, officialDetails, salaryAndLeaves, photo, created_by)
        if not details['flag']: response['flag'] = False
        response['message'].extend(details['message'])

        if response['flag']:
            required_fields = ['username', 'password', 'first_name', 'official_id']
            unique_fields = ['personal_email', 'personal_phone', 'nid_passport_no', 'tin_no', 'official_id', 'official_email', 'official_phone', 'rfid']
            choice_fields = [
                {'name': 'blood_group', 'type': 'single-string', 'values': [item[1] for item in CHOICE.BLOOD_GROUP]},
                {'name': 'marital_status', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MARITAL_STATUS]},
                {'name': 'gender', 'type': 'single-string', 'values': [item[1] for item in CHOICE.GENDER]},
                {'name': 'employee_type', 'type': 'single-string', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
                {'name': 'payment_in', 'type': 'single-string', 'values': [item[1] for item in CHOICE.PAYMENT_IN]},
                {'name': 'job_status', 'type': 'single-string', 'values': [item[1] for item in CHOICE.JOB_STATUS]}
            ]
            fields_regex = [
                {'field': 'dob', 'type': 'date'},
                {'field': 'personal_email', 'type': 'email'},
                {'field': 'personal_phone', 'type': 'phonenumber'},
                {'field': 'official_id', 'type': 'employeeid'},
                {'field': 'official_email', 'type': 'email'},
                {'field': 'official_phone', 'type': 'phonenumber'},
                {'field': 'joining_date', 'type': 'date'}
            ]
            responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                classOBJ=classOBJpackage['User'],
                Serializer=serializerOBJpackage['User'],
                data=details['data'],
                required_fields=required_fields,
                unique_fields=unique_fields,
                choice_fields=choice_fields,
                fields_regex=fields_regex
            )
            if responsesuccessflag == 'error':
                response['flag'] = False
                response['message'].extend(responsemessage)
                response['message'].append('couldn\'t create user instance, something went wrong!')
            if responsesuccessflag == 'success':
                response['message'].extend(responsemessage)
                response.update({'userinstance': responsedata.instance})
        return response
    

    def getWorkingDates(self, Generalsettings, Holiday, user, leavepolicy, leavesummary, from_date, to_date): # New
        response = {'message': [], 'dates': []}

        fiscal_year_from_date = leavesummary.fiscal_year.from_date
        fiscal_year_to_date = leavesummary.fiscal_year.to_date

        daycount = (to_date - from_date).days + 1
        if leavepolicy.is_calendar_day:
            for day in range(daycount):
                date = from_date + timedelta(day)
                if self.is_date_in_range(date, fiscal_year_from_date, fiscal_year_to_date): response['dates'].append(date)
                else: response['message'].append(f'applied date is not in this fiscal year!({fiscal_year_from_date} - {fiscal_year_to_date})')
        else:
            for day in range(daycount):
                date = from_date + timedelta(day)
                generalsettings = Generalsettings.objects.filter(fiscalyear=leavesummary.fiscal_year.id)
                if generalsettings.exists():
                    offdays = [each.day for each in generalsettings.first().weekly_holiday.day.all()]
                    if date.strftime("%A") not in offdays:
                        holidays = [each.date for each in Holiday.objects.filter(date=date, employee_grade=user.grade)]
                        if date not in holidays:
                            if self.is_date_in_range(date, fiscal_year_from_date, fiscal_year_to_date): response['dates'].append(date)
                            else: response['message'].append(f'applied date is not in this fiscal year!({fiscal_year_from_date} - {fiscal_year_to_date})')
                else: response['message'].append('please add general settings first!')
        return response
    

    def assignBulkUserToBulkLeavepolicy(self, classOBJpackage, leavepolicylist, userlist, manipulate_info): # New
        response = {'flag': False, 'message': [], 'backend_message': []}
        
        if 'Generalsettings' in classOBJpackage:
            if 'Leavepolicy' in classOBJpackage:
                if 'Leavepolicyassign' in classOBJpackage:
                    if 'Leavesummary' in classOBJpackage:
                        if 'User' in classOBJpackage:
                            fiscalyear_response = self.findFiscalyear(classOBJpackage['Generalsettings'])
                            fiscalyear = fiscalyear_response['fiscalyear']
                            if fiscalyear:
                                if leavepolicylist:
                                    if isinstance(leavepolicylist, list):
                                        for leavepolicyid in leavepolicylist:
                                            assign_leavepolicy_response = self.assignLeavepolicyToBulkUser(classOBJpackage, userlist, leavepolicyid, fiscalyear, manipulate_info)
                                            if assign_leavepolicy_response['flag']:
                                                response['flag'] = True
                                                response['message'].extend(assign_leavepolicy_response['message'])
                                            else: response['message'].extend(assign_leavepolicy_response['message'])
                                    else: response['message'].append('leavepolicy type should be list!')
                                else: response['message'].append('leavepolicy should not be empty!')
                            else: response['message'].extend(fiscalyear_response['message'])
                        else: response['backend_message'].append('User Model is missing!')
                    else: response['backend_message'].append('Leavesummary Model is missing!')
                else: response['backend_message'].append('Leavepolicyassign Model is missing!')
            else: response['backend_message'].append('Leavepolicy Model is missing!')
        else: response['backend_message'].append('Generalsettings Model is missing!')
        return response
    

    def assignBulkUserToBulkGroup(self, classOBJpackage, grouplist, userlist): # New
        response = {'flag': False, 'message': [], 'backend_message': []}

        if 'User' in classOBJpackage:
            if 'Group' in classOBJpackage:
                if 'Userdevicegroup' in classOBJpackage:
                    if 'Devicegroup' in classOBJpackage:

                        if grouplist:
                            if isinstance(grouplist, list):
                                for groupid in grouplist:
                                    assign_leavepolicy_response = self.assignGroupToBulkUser(classOBJpackage, userlist, groupid)
                                    if assign_leavepolicy_response['flag']: response['flag'] = True
                                    response['message'].extend(assign_leavepolicy_response['message'])
                            else: response['message'].append('leavepolicy type should be list!')
                        else: response['message'].append('group should not be empty!')

                    else: response['backend_message'].append('Devicegroup Model is missing!')
                else: response['backend_message'].append('Userdevicegroup Model is missing!')
            else: response['backend_message'].append('Group Model is missing!')
        else: response['backend_message'].append('User Model is missing!')
        return response

    
    def addGenarelSettings(self, classOBJ, Serializer, requestdata=None):
        response = {'flag': False, 'data': None, 'message': [], 'backend_message': []}
        
        if 'Weekdays' in classOBJ:
            if 'Weeklyholiday' in classOBJ:
                if 'Fiscalyear' in classOBJ:
                    if 'Generalsettings' in classOBJ:
                        if 'Fiscalyear' in Serializer:
                            if 'Generalsettings' in Serializer:
                                generalsettings = classOBJ['Generalsettings'].objects.all()
                                if not generalsettings.exists():
                                    if requestdata == None: requestdata = {}
                                    
                                    day_list = [each[1] for each in CHOICE.DAYS]
                                    for day in day_list:
                                        if not classOBJ['Weekdays'].objects.filter(day=day).exists():
                                            is_created = False
                                            while not is_created:
                                                try:
                                                    classOBJ['Weekdays'].objects.create(day=day)
                                                    is_created = True
                                                except: pass
                                    weekly_holiday = requestdata['weekly_holiday'] if isinstance(requestdata.get('weekly_holiday', False), list) else ['Friday', 'Saturday']
                                    weekly_holiday_id = []
                                    weekly_holiday_day = []
                                    for value in weekly_holiday:
                                        if value:
                                            if isinstance(value, str):
                                                if value.isnumeric(): weekly_holiday_id.append(int(value))
                                                else:
                                                    capitalize_day = value.capitalize()
                                                    if capitalize_day in day_list: weekly_holiday_day.append(capitalize_day)    
                                            elif isinstance(value, int): weekly_holiday_id.append(value)
                                    weekdaysinstance = classOBJ['Weekdays'].objects.filter(id__in=weekly_holiday_id) if classOBJ['Weekdays'].objects.filter(id__in=weekly_holiday_id) else classOBJ['Weekdays'].objects.filter(day__in=weekly_holiday_day)

                                    delete_instances = []
                                    weeklyholiday = classOBJ['Weeklyholiday'].objects.create()
                                    weeklyholiday.day.set(weekdaysinstance)
                                    requestdata.update({'weekly_holiday': weeklyholiday.id})
                                    delete_instances.append(weeklyholiday)

                                    fiscalyear_month = requestdata['fiscalyear_month'] if isinstance(requestdata.get('fiscalyear_month', False), str) else "January"
                                    requestdata.update({'fiscalyear_month': fiscalyear_month})
                                    from_date, to_date = self.getFiscalyearBoundary(fiscalyear_month, CHOICE.MONTHS_D)
                                    if from_date:
                                        required_fields = ['from_month', 'from_year', 'to_month', 'to_year', 'from_date', 'to_date']
                                        fields_regex = [{'field': 'from_date', 'type': 'date'}, {'field': 'to_date', 'type': 'date'}]
                                        choice_fields = [
                                            {'name': 'from_month', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MONTHS]},
                                            {'name': 'to_month', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MONTHS]},
                                        ]
                                        from_datesplit = [int(each) for each in f'{from_date}'.split('-')]
                                        to_datesplit = [int(each) for each in f'{to_date}'.split('-')]
                                        fiscalyeardata = {
                                            'from_month': CHOICE.MONTHS_DR[f'{from_datesplit[1]}'],
                                            'from_year': from_datesplit[0],
                                            'to_month': CHOICE.MONTHS_DR[f'{to_datesplit[1]}'],
                                            'to_year': to_datesplit[0],
                                            'from_date': f'{from_date}',
                                            'to_date': f'{to_date}'
                                        } 
                                        responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                                            classOBJ=classOBJ['Fiscalyear'], 
                                            Serializer=Serializer['Fiscalyear'], 
                                            data=fiscalyeardata, 
                                            required_fields=required_fields,
                                            fields_regex=fields_regex,
                                            choice_fields=choice_fields
                                        )
                                        if responsesuccessflag == 'success':
                                            requestdata.update({'fiscalyear': responsedata.data['id']})
                                            delete_instances.append(responsedata.instance)


                                    None if requestdata.get('workingday_starts_at') else requestdata.update({'workingday_starts_at': '09:00:00'})
                                    None if requestdata.get('consider_attendance_on_holidays') else requestdata.update({'consider_attendance_on_holidays': CHOICE.ATTENDANCE_OVERTIME[1][1]})

                                    
                                    required_fields = ['fiscalyear_month', 'fiscalyear', 'weekly_holiday', 'workingday_starts_at', 'consider_attendance_on_holidays']
                                    fields_regex = [{'field': 'workingday_starts_at', 'type': 'time'}]
                                    choice_fields = [
                                        {'name': 'fiscalyear_month', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MONTHS]},
                                        {'name': 'consider_attendance_on_holidays', 'type': 'single-string', 'values': [item[1] for item in CHOICE.ATTENDANCE_OVERTIME]},
                                    ]
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                                        classOBJ=classOBJ['Generalsettings'],
                                        Serializer=Serializer['Generalsettings'],
                                        data=requestdata,
                                        required_fields=required_fields,
                                        fields_regex=fields_regex,
                                        choice_fields=choice_fields
                                    )
                                    if responsesuccessflag == 'success':
                                        response['data']=responsedata
                                        response['flag'] = True
                                        classOBJ['Generalsettings'].objects.exclude(id=responsedata.data['id']).delete()
                                    elif responsesuccessflag == 'error':
                                        response['message'].extend(responsemessage)
                                        for delete_instance in delete_instances:
                                            delete_instance.delete()
                                else: response['message'].append('Generalsettings is already exist!')
                            else: response['backend_message'].append('Generalsettings model is missing in Serializer!')
                        else: response['backend_message'].append('Fiscalyear model is missing in Serializer!')
                    else: response['backend_message'].append('Generalsettings model is missing in classOBJ!')
                else: response['backend_message'].append('Fiscalyear model is missing in classOBJ!')
            else: response['backend_message'].append('Weeklyholiday model is missing in classOBJ!')
        else: response['backend_message'].append('Weekdays model is missing in classOBJ!')
        return response
    
    def calculateAttendance(self, data, User, Shiftchangelog, Generalsettings, Employeejobhistory, attendance_mode):
        response = {'data': {}, 'employee': None, 'generalsettings': None, 'message': []}
        
        date = data.get('date')
        if date:
            _year, _month, _date = [int(each) for each in date.split('-')]
            if not self.checkValidDate(_year, _month, _date): response['message'].append('date is not valid!')
        else: response['message'].append('date field is required!')

        employee = data.get('employee')
        if employee:
            employee = User.objects.filter(id=employee)
            if employee.exists(): response['employee'] = employee.first()
            else: response['message'].append('employee is not valid!')
        else: response['message'].append('employee field is required!')

        in_time = data.get('in_time')
        if in_time:
            hour, minute, second = [int(each) for each in in_time.split(':')]
            if not self.checkValidTime(hour, minute, second): response['message'].append('in_time is not valid!')
        # else: response_message.append('in_time field is required!')

        out_time = data.get('out_time')
        if out_time:
            hour, minute, second = [int(each) for each in out_time.split(':')]
            if not self.checkValidTime(hour, minute, second): response['message'].append('out_time is not valid!')
        # else: response_message.append('out_time field is required!')

        if not response['message']:
            shiftchangelog = Shiftchangelog.objects.filter(date=date, user=employee.first())
            shift = shiftchangelog.first().newshift if shiftchangelog.exists() else employee.first().shift
            if shift:
                generalsettings = self.findGeneralsettings(Generalsettings)
                if generalsettings:
                    response['generalsettings'] = generalsettings
                    response['data'].update(self.getattendancedetails(generalsettings, shift, in_time, out_time))
                    
                    designation = employee.first().designation
                    if designation: data.update({'designation': designation.id})

                    employeejobhistory = Employeejobhistory.objects.filter(user=employee.first().id).order_by('id')
                    if employeejobhistory.exists():
                        employeejobhistory = employeejobhistory.last()
                        while employeejobhistory != None:
                            if employeejobhistory.department:
                                response['data'].update({'department': employeejobhistory.department.id})
                                break
                            else: employeejobhistory = employeejobhistory.previous_id
                    response['data'].update({'attendance_mode': attendance_mode})
        return response