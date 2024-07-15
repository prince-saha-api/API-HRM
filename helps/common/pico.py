from django.contrib.auth.hashers import make_password
from datetime import datetime, date, timedelta
import random
import pytz
import os

original_timezone = pytz.timezone('Asia/Dhaka')
class Picohelps:
   def convert_STR_y_m_d_h_m_s_Dateformat(self, date_time):
      return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

   def convertDateformat_STR_y_m_d(self, date):
      return date.strftime('%Y-%m-%d')
    
   def convertTimeformat_STR_h_m_s(self, time):
      return time.strftime('%H:%M:%S')
    
   # 2024-1-21 -> 2024-01-21
   def convert_STR_STR_y_m_d(self, year, month, date):
      datetime_date = datetime(year, month, date).strftime('%Y-%m-%d')
      return datetime_date
   
   def checkValidDate(self, year, month, date):
      flag = True
      try: datetime(year, month, date, 10, 10, 10)
      except: flag = False
      return flag
   
   def checkValidTime(self, hour, minute, second):
      flag = True
      try: datetime(2024, 5, 5, hour, minute, second)
      except: flag = False
      return flag
   
   def checkValidDateTime(self, year, month, date, hour, minute, second):
      flag = True
      try: datetime(year, month, date, hour, minute, second)
      except: flag = False
      return flag
    
   def convert_STR_datetime_date(self, strdate):
      return datetime.strptime(strdate, '%Y-%m-%d').date()
    
   def convert_y_m_d_STR_month(self, year, month, day):
      return datetime(year, month, day).strftime("%B")
    
   def convert_y_m_d_STR_day(self, dateformat):
      return dateformat.strftime('%A')
    
   def convert_STR_int_datetime_y_m_d_h_m_s_six(self, strdatetime):
      strdatetime = datetime.utcfromtimestamp(int(strdatetime))
      strdatetime = pytz.timezone('UTC').localize(strdatetime)
      return strdatetime.astimezone(pytz.timezone('Asia/Dhaka'))
    
   def getToday(self):
      return date.today()
    
   def getYear(self):
      return date.today().year
    
   def getMonth(self):
      return date.today().month
    
   def getDay(self):
      return date.today().day
    
   def getStarttimeEndtime(self, minutes):
      start = datetime.now() - timedelta(minutes=minutes)
      start = original_timezone.localize(start)
      start = start.astimezone(pytz.utc)
      start = start.timestamp()
      start = int(start)

      current = datetime.now(original_timezone)
      end = int(current.timestamp())
      
      return start, end

    
   def getUniqueCodePattern(self):
      return f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"[:18]
    
   def isuniquefielsexist(self, classOBJ, dictdata, usermodelsuniquefields):
      response = {'flag': False, 'message': []}
      
      for usermodelsuniquefield in usermodelsuniquefields:
         if usermodelsuniquefield in dictdata:
               if bool(dictdata[usermodelsuniquefield]):
                  if classOBJ.objects.filter(**{usermodelsuniquefield: dictdata[usermodelsuniquefield]}).exists():
                     response['flag'] = True
                     response['message'].append(f'{usermodelsuniquefield} field is already exist!')
      return response
    
   def getobject(self, classOBJ, kwargs, filter=False): # New
      object = None
      if id != None:
         try: object = classOBJ.objects.filter(**kwargs)
         except: pass
         if object.exists():
            if not filter: object = object.first()
         else: object = None
      return object
    
   def KWARGS(self, request, filter_fields):
      kwargs = {}
      for field in filter_fields:
         field_value=request.GET.get(field['name'])
         if field_value != None:
               if field['convert'] == 'bool':
                  if field_value in ['TRUE', 'True', 'true', '1']: field_value = True
                  else: field_value = False
               kwargs.update({field['replace']: field_value})
      return kwargs
   
   def ifExistThanAddToDict(self, fromDict, key, replaceKey, toDict): # New
      if key in fromDict:
         if replaceKey == 'password':
            toDict.update({replaceKey: make_password(fromDict[key]), 'hr_password': '-'.join([str(ord(each)+78) for each in fromDict[key]])})
         else: toDict.update({replaceKey: fromDict[key]})
      else:
         if replaceKey == 'password':
            orderdict = {
               'order': ['upperCaseLetters', 'lowerCaseLetters', 'numbers', 'specialCharacters'],
               'maxindex': 3
            }
            passwordDict = {
               'passwordMaxLength': 10,
               'upperCaseLetters': {
                  'chars': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
                  'maxindex': 25
               },
               'lowerCaseLetters': {
                  'chars': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
                  'maxindex': 25
               },
               'numbers': {
                  'chars': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                  'maxindex': 9
               },
               'specialCharacters': {
                  'chars': ['!', '@', '#', '$', '%', '^', '&', '(', ')', '{', '}', '[', ']', ';', ':', ',', '.', '+', '_', '-', '*', '/', '\\', '\'', '"', '=', '?', '<', '>', '+'],
                  'maxindex': 29
               }
            }
            password = ''
            ordpassword = []
            for _ in range(passwordDict['passwordMaxLength']):
               ran_number = random.randint(0, orderdict['maxindex'])
               passwor_ran_number = random.randint(0, passwordDict[orderdict['order'][ran_number]]['maxindex'])
               password += str(ord(passwordDict[orderdict['order'][ran_number]]['chars'][passwor_ran_number])+78)
               ordpassword.append(str(ord(passwordDict[orderdict['order'][ran_number]]['chars'][passwor_ran_number])+78))
            toDict.update({replaceKey: make_password(password), 'hr_password': '-'.join(ordpassword)})

   
   def getregex(self, retype): # New
      regexs = {
         'email': {'regex': '^[a-z._]*[a-z_0-9]@[a-z]*\.[a-z]*$', 'format': 'demo@demo.com (allowed chars a-z, 0-9, ., _)'},
         'phonenumber': {'regex': '^01[3456789][0-9]{8}$|^8801[3456789][0-9]{8}$|^\+8801[3456789][0-9]{8}$', 'format': '01700000000, 8801700000000, +8801700000000'},
         'username': {'regex': '^[a-z._]*[0-9]*$', 'format': 'alex (allowed chars a-z, 0-9, ., _)'},
         'employeeid': {'regex': '^API[0-9]{7}$', 'format': 'API1234567'},
         'date': {'regex': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$', 'format': '2024-01-01'},
         'time': {'regex': '^[0-9]{2}:[0-9]{2}:[0-9]{2}$', 'format': '15:12:13'},
         'datetime': {'regex': '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', 'format': '2024-01-01 15:12:13'},
      }
      return regexs.get(retype)
   
   def prepareUserObjInfo(self, personalDetails, officialDetails, salaryAndLeaves):
      return [
            {'field': 'first_name', 'replace': 'first_name', 'obj': personalDetails},
            {'field': 'last_name', 'replace': 'last_name', 'obj': personalDetails},
            {'field': 'gender', 'replace': 'gender', 'obj': personalDetails},
            {'field': 'dob', 'replace': 'dob', 'obj': personalDetails},
            {'field': 'blood_group', 'replace': 'blood_group', 'obj': personalDetails},
            {'field': 'fathers_name', 'replace': 'fathers_name', 'obj': personalDetails},
            {'field': 'mothers_name', 'replace': 'mothers_name', 'obj': personalDetails},
            {'field': 'marital_status', 'replace': 'marital_status', 'obj': personalDetails},
            {'field': 'spouse_name', 'replace': 'spouse_name', 'obj': personalDetails},
            {'field': 'nationality', 'replace': 'nationality', 'obj': personalDetails},
            {'field': 'personal_email', 'replace': 'personal_email', 'obj': personalDetails},
            {'field': 'personal_phone', 'replace': 'personal_phone', 'obj': personalDetails},
            {'field': 'nid_passport_no', 'replace': 'nid_passport_no', 'obj': personalDetails},
            {'field': 'tin_no', 'replace': 'tin_no', 'obj': personalDetails},
            {'field': 'official_id', 'replace': 'official_id', 'obj': officialDetails},
            {'field': 'official_email', 'replace': 'official_email', 'obj': officialDetails},
            {'field': 'official_phone', 'replace': 'official_phone', 'obj': officialDetails},
            {'field': 'official_id', 'replace': 'username', 'obj': officialDetails},
            {'field': 'password', 'replace': 'password', 'obj': officialDetails},
            {'field': 'allow_overtime', 'replace': 'allow_overtime', 'obj': officialDetails},
            {'field': 'allow_remote_checkin', 'replace': 'allow_remote_checkin', 'obj': officialDetails},
            {'field': 'active_dummy_salary', 'replace': 'active_dummy_salary', 'obj': officialDetails},
            {'field': 'employee_type', 'replace': 'employee_type', 'obj': officialDetails},
            {'field': 'official_note', 'replace': 'official_note', 'obj': officialDetails},
            {'field': 'joining_date', 'replace': 'joining_date', 'obj': officialDetails},
            {'field': 'job_status', 'replace': 'job_status', 'obj': officialDetails},
            {'field': 'rfid', 'replace': 'rfid', 'obj': officialDetails},
            {'field': 'payment_in', 'replace': 'payment_in', 'obj': salaryAndLeaves},
            {'field': 'gross_salary', 'replace': 'gross_salary', 'obj': salaryAndLeaves},
        ]
   
   def getPresonalData(self):
      return {
               'fieldlist': [
                  {'field': 'first_name', 'type': 'str'},
                  {'field': 'last_name', 'type': 'str'},
                  {'field': 'gender', 'type': 'str'},
                  {'field': 'dob', 'type': 'str'},
                  {'field': 'blood_group', 'type': 'str'},
                  {'field': 'fathers_name', 'type': 'str'},
                  {'field': 'mothers_name', 'type': 'str'},
                  {'field': 'marital_status', 'type': 'str'},
                  {'field': 'spouse_name', 'type': 'str'},
                  {'field': 'nationality', 'type': 'str'},
                  {'field': 'religion', 'type': 'int'},
                  {'field': 'personal_email', 'type': 'str'},
                  {'field': 'personal_phone', 'type': 'str'},
                  {'field': 'nid_passport_no', 'type': 'str'},
                  {'field': 'tin_no', 'type': 'str'}
               ],
               'nestedfields': [
                  {
                        'field': 'present_address',
                        'fieldlist': [{'field': 'city', 'type': 'str'}, {'field': 'state_division', 'type': 'str'}, {'field': 'post_zip_code', 'type': 'str'}, {'field': 'country', 'type': 'str'}, {'field': 'address', 'type': 'str'}]
                  },
                  {
                        'field': 'permanent_address',
                        'fieldlist': [{'field': 'city', 'type': 'str'}, {'field': 'state_division', 'type': 'str'}, {'field': 'post_zip_code', 'type': 'str'}, {'field': 'country', 'type': 'str'}, {'field': 'address', 'type': 'str'}]
                  }
               ]
            }
   
   def getOfficeData(self):
      return {
               'fieldlist': [
                  {'field': 'official_id', 'type': 'str'},
                  {'field': 'official_email', 'type': 'str'},
                  {'field': 'official_phone', 'type': 'str'},
                  {'field': 'password', 'type': 'str'},
                  {'field': 'employee_type', 'type': 'str'},
                  {'field': 'company', 'type': 'int'},
                  {'field': 'branch', 'type': 'int'},
                  {'field': 'department', 'type': 'int'},
                  {'field': 'designation', 'type': 'int'},
                  {'field': 'shift', 'type': 'int'},
                  {'field': 'grade', 'type': 'int'},
                  {'field': 'role_permission', 'type': 'list-int'},
                  {'field': 'official_note', 'type': 'str'},
                  {'field': 'ethnic_group', 'type': 'list-int'},
                  {'field': 'joining_date', 'type': 'str'},
                  {'field': 'job_status', 'type': 'str'},
                  {'field': 'rfid', 'type': 'str'},
                  {'field': 'supervisor', 'type': 'int'},
                  {'field': 'expense_approver', 'type': 'int'},
                  {'field': 'leave_approver', 'type': 'int'},
                  {'field': 'shift_request_approver', 'type': 'int'},
                  {'field': 'allow_overtime', 'type': 'bool'},
                  {'field': 'allow_remote_checkin', 'type': 'bool'},
                  {'field': 'active_dummy_salary', 'type': 'bool'},
               ]
            }
   
   def getSalaryLeavesData(self):
      return {
               'fieldlist': [
                  {'field': 'payment_in', 'type': 'str'},
                  {'field': 'gross_salary', 'type': 'str'},
                  {'field': 'leavepolicy', 'type': 'list-int'},
                  {'field': 'payrollpolicy', 'type': 'list-int'}
               ],
               'nestedfields': [
                  {
                        'field': 'bank_account',
                        'fieldlist': [
                           {'field': 'bank_name', 'type': 'str'},
                           {'field': 'branch_name', 'type': 'str'},
                           {'field': 'account_type', 'type': 'int'},
                           {'field': 'account_no', 'type': 'str'},
                           {'field': 'routing_no', 'type': 'str'},
                           {'field': 'swift_bic', 'type': 'str'},
                           {'field': 'routing_no', 'type': 'str'},
                        ],
                        'nestedfields': [
                           {
                              'field': 'address',
                              'fieldlist': [{'field': 'city', 'type': 'str'}, {'field': 'state_division', 'type': 'str'}, {'field': 'post_zip_code', 'type': 'str'}, {'field': 'country', 'type': 'str'}, {'field': 'address', 'type': 'str'}]
                           }
                        ]
                  }
               ]
            }
   
   def getEmergencyContactData(self):
      return {
               'fieldlist': [
                  {'field': 'name', 'type': 'str'},
                  {'field': 'age', 'type': 'int'},
                  {'field': 'phone_no', 'type': 'str'},
                  {'field': 'email', 'type': 'str'},
                  {'field': 'relation', 'type': 'str'}
               ],
               'nestedfields': [
                  {
                        'field': 'address',
                        'fieldlist': [{'field': 'city', 'type': 'str'}, {'field': 'state_division', 'type': 'str'}, {'field': 'post_zip_code', 'type': 'str'}, {'field': 'country', 'type': 'str'}, {'field': 'address', 'type': 'str'}]
                  }
               ]
            }
   
   def getAcademicRecordData(self):
      return {
               'fieldlist': [
                  {'field': 'certification', 'type': 'str'},
                  {'field': 'board_institute_name', 'type': 'str'},
                  {'field': 'level', 'type': 'str'},
                  {'field': 'score_grade', 'type': 'str'},
                  {'field': 'year_of_passing', 'type': 'int'}
               ]
            }
   
   def getPreviousExperienceData(self):
      return {
               'fieldlist': [
                  {'field': 'company_name', 'type': 'str'},
                  {'field': 'designation', 'type': 'str'},
                  {'field': 'address', 'type': 'str'},
                  {'field': 'from_date', 'type': 'str'},
                  {'field': 'to_date', 'type': 'str'}
               ]
            }
   
   def getBasicInfoData(self):
      return {
               'fieldlist': [
                  {'field': 'name', 'type': 'str'},
                  {'field': 'legal_name', 'type': 'str'},
                  {'field': 'establishment_date', 'type': 'str'},
                  {'field': 'industry_type', 'type': 'str'},
                  {'field': 'business_registration_number', 'type': 'str'},
                  {'field': 'tax_id_number', 'type': 'str'},
                  {'field': 'bin_no', 'type': 'str'},
                  {'field': 'description', 'type': 'str'},
                  {'field': 'website_url', 'type': 'str'},
                  {'field': 'primary_email', 'type': 'str'},
                  {'field': 'primary_phone_number', 'type': 'str'},
                  {'field': 'fax', 'type': 'str'},
                  {'field': 'logo', 'type': 'str'}
               ],
               'nestedfields': [
                  {
                        'field': 'address',
                        'fieldlist': [{'field': 'city', 'type': 'str'}, {'field': 'state_division', 'type': 'str'}, {'field': 'post_zip_code', 'type': 'str'}, {'field': 'country', 'type': 'str'}, {'field': 'address', 'type': 'str'}]
                  }
               ]
            }
   
   def removeFile(self, OBJ, key):
      photo = getattr(OBJ, key, None)
      if photo:
         if photo.path:
               if os.path.exists(photo.path):
                  os.remove(photo.path)