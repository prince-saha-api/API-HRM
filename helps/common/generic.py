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
    
    def getattendancedetails(self, Offday, shift, date, actual_in_time, actual_out_time): # New

        shiftandactualinoutdetails = self.getshiftandactualinoutdetails(shift, actual_in_time, actual_out_time)
        flag_details = self.claculateinoutflag(shiftandactualinoutdetails)
        entranceexitdetails = self.claculateentranceexitdetails(flag_details, shiftandactualinoutdetails)
        ateattendancedetails = self.claculateattendancedetails(entranceexitdetails)

        offday = self.getofficeoffday(Offday, date)
        
        total_minutes = ((shiftandactualinoutdetails['actual_out_time']-shiftandactualinoutdetails['actual_in_time']).total_seconds())/60
        total_minutes -=ateattendancedetails['in_positive_minutes']
        total_minutes -=ateattendancedetails['out_positive_minutes']

        return {
            'in_negative_minutes': ateattendancedetails['in_negative_minutes'],
            'in_positive_minutes': ateattendancedetails['in_positive_minutes'],
            'out_negative_minutes': ateattendancedetails['out_negative_minutes'],
            'out_positive_minutes': ateattendancedetails['out_positive_minutes'],
            'total_minutes': total_minutes,
            'office_off_day': offday
        }
    
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
                {'name': 'blood_group', 'values': [item[1] for item in CHOICE.BLOOD_GROUP]},
                {'name': 'marital_status', 'values': [item[1] for item in CHOICE.MARITAL_STATUS]},
                {'name': 'gender', 'values': [item[1] for item in CHOICE.GENDER]},
                {'name': 'employee_type', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
                {'name': 'payment_in', 'values': [item[1] for item in CHOICE.PAYMENT_IN]},
                {'name': 'job_status', 'values': [item[1] for item in CHOICE.JOB_STATUS]}
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