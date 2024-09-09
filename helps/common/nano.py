from helps.common.pico import Picohelps
from datetime import datetime, timedelta
import re
import os

class Nanohelps(Picohelps):
    def is_date_in_range(self, date, start_date, end_date):
        return start_date <= date <= end_date
    
    def getFirstObjectIfExistOrNot(self, ClassObject, kwargs=None):
        if kwargs == None:
            if not ClassObject.objects.all(): ClassObject.objects.create()
            return ClassObject.objects.all().first()
        else:
            if not ClassObject.objects.filter(**kwargs): ClassObject.objects.create()
            return ClassObject.objects.filter(**kwargs).first()
    
    def generateUniqueCode(self, pattern):
        # CMPTP-20240114123559618137
        return f'{pattern}-{self.getUniqueCodePattern()}'
    
    def getshiftandactualinoutdetails(self, shift, actual_in_time, actual_out_time):
        shift_beginning = self.convert_STR_y_m_d_h_m_s_Dateformat(f'2010-1-1 {shift.in_time}')
        shift_ending = self.convert_STR_y_m_d_h_m_s_Dateformat(f'2010-1-1 {shift.out_time}')
        if shift_beginning>shift_ending: shift_ending = shift_ending + timedelta(days=1)

        if actual_in_time:
            actual_in_time = self.convert_STR_y_m_d_h_m_s_Dateformat(f'2010-1-1 {actual_in_time}')
            if actual_out_time:
                actual_out_time = self.convert_STR_y_m_d_h_m_s_Dateformat(f'2010-1-1 {actual_out_time}')
                if actual_in_time>actual_out_time: actual_out_time = actual_out_time + timedelta(days=1)
            else: actual_out_time = None
        else:
            actual_in_time = None
            actual_out_time = None

        return {
            'shift_beginning': shift_beginning,
            'shift_ending': shift_ending,
            'actual_in_time': actual_in_time,
            'actual_out_time': actual_out_time
        }
    
    def claculateentranceexitdetails(self, flag_details):
        early_entrance = 0
        late_entrance = 0
        early_exit = 0
        late_exit = 0

        if flag_details['in_flag'] and flag_details['out_flag']:
            early_entrance = flag_details['in_diff']
            late_exit = flag_details['out_diff']
        if flag_details['in_flag'] and not flag_details['out_flag']:
            early_entrance = flag_details['in_diff']
            early_exit = flag_details['out_diff']*(-1) if flag_details['out_diff'] else None
        if not flag_details['in_flag'] and flag_details['out_flag']:
            late_entrance = flag_details['in_diff']*(-1) if flag_details['in_diff'] else None
            late_exit = flag_details['out_diff']
        if not flag_details['in_flag'] and not flag_details['out_flag']:
            late_entrance = flag_details['in_diff']*(-1) if flag_details['in_diff'] else None
            early_exit = flag_details['out_diff']*(-1) if flag_details['out_diff'] else None
        
        return {
            'early_entrance': early_entrance,
            'early_exit': early_exit,
            'late_entrance': late_entrance,
            'late_exit': late_exit
        }
    
    def claculateworkingminutes(self, shiftandactualinoutdetails, entranceexitdetails):
        working_minutes = None
        if entranceexitdetails['late_entrance'] != None and entranceexitdetails['early_exit'] != None:
            shift_beginning = shiftandactualinoutdetails['shift_beginning']
            shift_ending = shiftandactualinoutdetails['shift_ending']

            working_minutes = ((shift_ending-shift_beginning).total_seconds())/60
            working_minutes -= entranceexitdetails['late_entrance']
            working_minutes -= entranceexitdetails['early_exit']
        return working_minutes
    
    def claculateinoutflag(self, shiftandactualinoutdetails):
        in_flag = False
        in_diff = None
        if shiftandactualinoutdetails['actual_in_time'] != None:
            in_diff = ((shiftandactualinoutdetails['shift_beginning']-shiftandactualinoutdetails['actual_in_time']).total_seconds())/60
            in_flag = True if in_diff>=0 else False

        out_flag = False
        out_diff = None
        if shiftandactualinoutdetails['actual_out_time'] != None:
            out_diff = ((shiftandactualinoutdetails['actual_out_time']-shiftandactualinoutdetails['shift_ending']).total_seconds())/60
            out_flag = True if out_diff>=0 else False

        return {
            'in_flag': in_flag,
            'in_diff': in_diff,
            'out_flag': out_flag,
            'out_diff': out_diff
        }
    
    def is_date_holiday_for_this_user(self, Holiday, employee, date):
        holiday = Holiday.objects.filter(date=date, is_active=True)
        if holiday.exists():
            if holiday.first().employee_grade:
                if employee.grade:
                    if holiday.first().employee_grade == employee.grade: return holiday.first()
                    else: return None
                else: return None
            else: return holiday.first()
        else: return None
    
    def filterAllowedFields(self, allowed_fields, data, preparedata): # New
        if isinstance(allowed_fields, str):
            if allowed_fields == '__all__':
                for datakey in data.keys():
                    if data[datakey]: preparedata.update(data)
        elif isinstance(allowed_fields, list):
            for field in allowed_fields:
                fieldvalue = data.get(field)
                if fieldvalue != None: preparedata.update({field: fieldvalue})

    def filterUniqueFields(self, classOBJ, unique_fields, preparedata, response_message, recordid=None): # New
        uniquekeyvalue = {}
        for field in unique_fields:
            uniquevalue = preparedata.get(field)
            if uniquevalue: uniquekeyvalue.update({field: uniquevalue})
        for key, value in uniquekeyvalue.items():
            classobj = classOBJ.objects.filter(**{key:value})
            if classobj.exists():
                if recordid:
                    if classobj.first().id != recordid:
                        response_message.append(f'{key}({value}) is already exist!')
                else: response_message.append(f'{key}({value}) is already exist!')

    def filterChoiceFields(self, choice_fields, preparedata, response_message): # New
        for choice_field in choice_fields:
            if 'type' in choice_field:
                if choice_field['type'] == 'single-string':
                    if choice_field['name'] in preparedata:
                        if preparedata[choice_field['name']] not in choice_field['values']: response_message.append(f'{choice_field["name"]} fields\'s allowed values are {", ".join(choice_field["values"])}')
                elif choice_field['type'] == 'list-string':
                    if choice_field['name'] in preparedata:
                        if preparedata[choice_field['name']]:
                            if isinstance(preparedata[choice_field['name']], list):
                                for field_value in preparedata[choice_field['name']]:
                                    if field_value not in choice_field['values']:
                                        response_message.append(f'{choice_field["name"]} fields\'s allowed values are {", ".join(choice_field["values"])}')
                                        break

    def filterRequiredFields(self, required_fields, preparedata, response_message): # New
        for required_field in required_fields:
            if required_field not in preparedata: response_message.append(f'{required_field} is required!')

    def filterRegexFields(self, fields_regex, preparedata, response_message): # New
        for field_regex in fields_regex:
            if field_regex['field'] in preparedata:
                regexObj= self.getregex(field_regex['type'])
                if re.search(regexObj['regex'], preparedata[field_regex['field']]):
                    if field_regex['type'] == 'date':
                        year, month, date = [int(each) for each in preparedata[field_regex['field']].split('-')]
                        if not self.checkValidDate(year, month, date): response_message.append(f'{field_regex["field"]} field\'s format is {regexObj["format"]}!')
                    if field_regex['type'] == 'time':
                        hour, minute, second = [int(each) for each in preparedata[field_regex['field']].split(':')]
                        if not self.checkValidTime(hour, minute, second): response_message.append(f'{field_regex["field"]} field\'s format is {regexObj["format"]}!')
                    if field_regex['type'] == 'datetime':
                        str_date, str_time = preparedata[field_regex['field']].split(' ')
                        year, month, date = [int(each) for each in str_date.split('-')]
                        hour, minute, second = [int(each) for each in str_time.split(':')]
                        if not self.checkValidTime(year, month, date, hour, minute, second): response_message.append(f'{field_regex["field"]} field\'s format is {regexObj["format"]}!')
                else: response_message.append(f'{field_regex["field"]} field\'s format is {regexObj["format"]}!')

    def filterFreezFields(self, classobj, freez_update, response_message): # New
        for FREEZ in freez_update:
            if FREEZ:
                for key, value in FREEZ.items():
                    objvalue = getattr(classobj.first(), key, '')
                    if objvalue in value:
                        response_message.append(f'{key} (it\'s already {objvalue}.)')

    def filterContinueFields(self, classobj, continue_update, response_message): # New
        for CONTINUE in continue_update:
            if CONTINUE:
                for key, value in CONTINUE.items():
                    objvalue = getattr(classobj.first(), key, '')
                    if objvalue not in value: response_message.append(f'{key} (it\'s already {objvalue}.)')

    def findFiscalyear(self, Generalsettings): # New
        response_message = []
        fiscalyear = None
        generalsettings = self.findGeneralsettings(Generalsettings)
        if generalsettings:
            if generalsettings.fiscalyear: fiscalyear = generalsettings.fiscalyear
            else: response_message.append('fiscalyear is missing!')
        else: response_message.append('general-settings is missing!')
        return {
            'fiscalyear': fiscalyear,
            'message': response_message
        }

    def getFiscalyearBoundary(self, month, monthdict): # New
        month = monthdict.get(month)
        if month:
            from_date = datetime(self.getYear(), month, 1).date()
            to_date = from_date + timedelta(days=364)
            return from_date, to_date
        else: return None, None
    
    def getBasicSalary(self, Generalsettings, salary): # New
        response = {'flag': False, 'basic_salary': 0, 'message': []}
        generalsettings = None
        if salary:
            try:
                salary = float(salary)
                generalsettings = self.findGeneralsettings(Generalsettings)
                if generalsettings:
                    basic_salary_percentage = generalsettings.basic_salary_percentage
                    if basic_salary_percentage:
                        response['basic_salary'] = (salary*basic_salary_percentage)/100
                        response['flag'] = True
                    else: response['message'].append('basic_salary_percentage is missing in generalsettings!')
                else: response['message'].append('generalsettings is missing!')
            except: response['message'].append('salary is missing!')
        return response
    

    def getUsersInfoToRegisterIntoDevice(self, User, Userdevicegroup, device, groupid): # New
        response = {'data': [], 'user_count': 0,'message': []}
        for user in [each.user for each in Userdevicegroup.objects.filter(group=groupid)]:
            user_register_info = self.getUserInfoToRegisterIntoDevice(User, user, device)
            if user_register_info['flag']: response['data'].append(user_register_info['data'])
            else: response['message'].extend(user_register_info['message'])
            response['user_count'] += 1
        return response
    
    def getUsersWhoWillGetNotice(self, Branch, Department, User, Noticeboardserializer, noticeboards, many=True): # New
        noticeboardserializers = []
        if many: noticeboardserializers = Noticeboardserializer(noticeboards, many=True).data
        else: noticeboardserializers.append(Noticeboardserializer(noticeboards, many=False).data)
        
        for each in noticeboardserializers:
            users_to_preview = {}

            noticeboardcompanys = each['noticeboardcompany_noticeboard']
            companyid_list = []
            if noticeboardcompanys:
                for noticeboardcompany in noticeboardcompanys:
                    companyid_list.append(noticeboardcompany['company']['id'])
            branchid_list = [each.id for each in Branch.objects.filter(company__in=companyid_list)]
            departments = Department.objects.filter(branch__in=branchid_list).distinct('id')
            for department in departments:
                user_list = department.user.all()
                for user in user_list:
                    if user.id not in users_to_preview:
                        users_to_preview.update({str(user.id): {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}})

            noticeboardbranchs = each['noticeboardbranch_noticeboard']
            branchid_list = []
            if noticeboardbranchs:
                for noticeboardbranch in noticeboardbranchs:
                    branchid_list.append(noticeboardbranch['branch']['id'])
            departments = Department.objects.filter(branch__in=branchid_list).distinct('id')
            for department in departments:
                user_list = department.user.all()
                for user in user_list:
                    if user.id not in users_to_preview:
                        users_to_preview.update({str(user.id): {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}})

            noticeboarddepartments = each['noticeboarddepartment_noticeboard']
            departmentid_list = []
            if noticeboarddepartments:
                for noticeboarddepartment in noticeboarddepartments:
                    departmentid_list.append(noticeboarddepartment['department']['id'])
            departments = Department.objects.filter(id__in=departmentid_list).distinct('id')
            for department in departments:
                user_list = department.user.all()
                for user in user_list:
                    if user.id not in users_to_preview:
                        users_to_preview.update({str(user.id): {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}})

            noticeboardemployees = each['noticeboardemployee_noticeboard']
            employeeid_list = []
            if noticeboardemployees:
                for noticeboardemployee in noticeboardemployees:
                    employeeid_list.append(noticeboardemployee['user']['id'])
            user_list = User.objects.filter(id__in=employeeid_list).distinct('id')
            for user in user_list:
                if user.id not in users_to_preview:
                    users_to_preview.update({str(user.id): {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}})

            each.update({'users_to_preview': [users_to_preview[each] for each in users_to_preview.keys()]})
        return noticeboardserializers if many else noticeboardserializers[0]