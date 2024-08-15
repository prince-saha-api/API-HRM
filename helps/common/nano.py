from helps.common.pico import Picohelps
from datetime import datetime, timedelta
from hrm.settings import BASE_DIR
# import cv2
import os
import re

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

        actual_in_time = self.convert_STR_y_m_d_h_m_s_Dateformat(f'2010-1-1 {actual_in_time}')
        actual_out_time = self.convert_STR_y_m_d_h_m_s_Dateformat(f'2010-1-1 {actual_out_time}')
        
        return {
            'shift_beginning': shift_beginning,
            'shift_ending': shift_ending,
            'actual_in_time': actual_in_time,
            'actual_out_time': actual_out_time
        }
    
    def claculateentranceexitdetails(self, flag_details, shiftandactualinoutdetails):
        early_entrance = 0
        late_entrance = 0
        early_exit = 0
        late_exit = 0

        if flag_details['in_flag'] and flag_details['out_flag']:
            early_entrance = flag_details['in_diff']
            late_exit = flag_details['out_diff']
        if flag_details['in_flag'] and not flag_details['out_flag']:
            early_entrance = flag_details['in_diff']
            early_exit = (shiftandactualinoutdetails['shift_ending']-shiftandactualinoutdetails['actual_out_time']).total_seconds()
        if not flag_details['in_flag'] and flag_details['out_flag']:
            late_entrance = (shiftandactualinoutdetails['actual_in_time']-shiftandactualinoutdetails['shift_beginning']).total_seconds()
            late_exit = flag_details['out_diff']
        if not flag_details['in_flag'] and not flag_details['out_flag']:
            late_entrance = (shiftandactualinoutdetails['actual_in_time']-shiftandactualinoutdetails['shift_beginning']).total_seconds()
            early_exit = (shiftandactualinoutdetails['shift_ending']-shiftandactualinoutdetails['actual_out_time']).total_seconds()
        
        return {
            'early_entrance': early_entrance,
            'early_exit': early_exit,
            'late_entrance': late_entrance,
            'late_exit': late_exit
        }
    
    def claculateattendancedetails(self, entranceexitdetails):
        if entranceexitdetails['late_entrance']:
            in_positive_minutes=0
            in_negative_minutes=entranceexitdetails['late_entrance']/60
        if entranceexitdetails['early_entrance']:
            in_positive_minutes=entranceexitdetails['early_entrance']/60
            in_negative_minutes=0

        if entranceexitdetails['early_exit']:
            out_negative_minutes=entranceexitdetails['early_exit']/60
            out_positive_minutes = 0
        if entranceexitdetails['late_exit']:
            out_negative_minutes=0
            out_positive_minutes = entranceexitdetails['late_exit']/60
        
        return {
            'in_positive_minutes': in_positive_minutes,
            'in_negative_minutes': in_negative_minutes,
            'out_positive_minutes': out_positive_minutes,
            'out_negative_minutes': out_negative_minutes
        }
    
    def claculateinoutflag(self, shiftandactualinoutdetails):
        in_flag = False
        in_diff = (shiftandactualinoutdetails['shift_beginning']-shiftandactualinoutdetails['actual_in_time']).total_seconds()
        in_flag = True if in_diff>=0 else False

        out_flag = False
        out_diff = (shiftandactualinoutdetails['actual_out_time']-shiftandactualinoutdetails['shift_ending']).total_seconds()
        out_flag = True if out_diff>=0 else False
        
        return {
            'in_flag': in_flag,
            'in_diff': in_diff,
            'out_flag': out_flag,
            'out_diff': out_diff
        }
    
    def getofficeoffday(self, Offday, date):
        date = self.convert_STR_datetime_date(date)
        offday = Offday.objects.filter(day=self.convert_y_m_d_STR_day(date), is_active=True)

        return offday.first() if offday.exists() else None
    
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
            if choice_field['name'] in preparedata:
                if preparedata[choice_field['name']] not in choice_field['values']: response_message.append(f'{choice_field["name"]} fields\'s allowed values are {", ".join(choice_field["values"])}')

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

    # def countPersonInImage(self, bytesio_image): # New
    #     response = {'person_count': 0, 'message': []}
    #     face_detector_path = BASE_DIR / 'static/face_detector_file/haarcascade_frontalface_default.xml'
    #     if os.path.exists(face_detector_path):
    #         image_response = self.convert_bytesio_ndarray(bytesio_image)
    #         if image_response['flag']:
    #             facedetect = cv2.CascadeClassifier(face_detector_path)
    #             faces = facedetect.detectMultiScale(image_response['image'], 1.3, 5)
    #             response['person_count'] = len(faces)
    #         else:
    #             response['message'].extend(image_response['message'])
    #     else: response['message'].append('face_detector_file\'s path doesn\'t exist!')
    #     return response
    
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