from datetime import datetime, date, timedelta
import pytz

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
    
    def generateOBJSalaryCalculation(self, salary_info):
        return {
            "gross_salary":salary_info.gross_salary,
            "payable_salary":salary_info.gross_salary,
            "deduction": {
                "leave_cost":{
                    "total_cost_of_employee":0,
                    "total_leave_taken":0,
                    "total_cost_of_company":0,
                    "per_day_cost":0,
                    "details":[
                            {
                                "name":"",
                                "company_will_bare":0,
                                "employee_will_bare":0
                            }
                    ]
                },
                "attendance_cost":{
                    "cost": 0,
                    "penalty_based_on_total_minutes": 0,
                    "absent": {
                        "absent_count": 0,
                        "details": []
                        },
                    "fine_in_days": {
                        "fine_count": 0,
                        "details": {}
                    }
                }
            },
            "earnings": {
                "total_earnings": 0,
            },
        }
    
    def generateOBJAttendanceReport(self, total_working_days_ideal):
        return {
            'total_working_days_ideal': total_working_days_ideal,
            'attendance': {
                'attendance_count': 0,
                'details': {}
            },
            'absent': {
                'absent_count': 0,
                'details': []
            },
            'late_attendance_based_on_buffer_count': 0,
            'total_minutes': 0,
            'penalty_based_on_total_minutes': 0,
            'late_entry_fine': {
                'fine_in_days': 0,
                'details': {}
            }
        }

    def prepareDetailsAttendanceReport(self, employeeworkingdate_idealcase, attendance):
        return {
            employeeworkingdate_idealcase: {
                'intime': self.convertTimeformat_STR_h_m_s(attendance.in_time),
                'outtime': self.convertTimeformat_STR_h_m_s(attendance.out_time),
                'total_minutes': attendance.total_minutes,
                'late_in_based_on_buffertime': attendance.late_in_based_on_buffertime,
                'shift': attendance.shift_time,
                'buffer_time': attendance.buffer_time_minutes
                }}
    
    def generateOBJLeaveCost(self):
        return {
            'total_cost_of_employee': 0,
            'total_leave_taken': 0,
            'total_cost_of_company': 0,
            'per_day_cost': 0,
            'details': []
        }
    
    def getUniqueCodePattern(self):
        return f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"[:18]
    
    def isuniquefielsexist(self, classOBJ, dictdata, usermodelsuniquefields):
        response = {
            'flag': False,
            'message': []
        }
        for usermodelsuniquefield in usermodelsuniquefields:
            if usermodelsuniquefield in dictdata:
                if classOBJ.objects.filter(**{usermodelsuniquefield: dictdata[usermodelsuniquefield]}).exists():
                    response['flag'] = True
                    response['message'].append(f'{usermodelsuniquefield} is already exist!')
        return response
    
    def getobject(self, classOBJ, kwargs, filter=False): # New
        object = None
        if id != None:
            try:
               if filter: object = classOBJ.objects.filter(**kwargs)
               else: object = classOBJ.objects.get(**kwargs)
            except: pass
        return object
    
    def requestdata(self):
        return {
                  "personalDetails[first_name]":[
                     "Nazmul"
                  ],
                  "personalDetails[last_name]":[
                     "Hussain"
                  ],
                  "personalDetails[gender]":[
                     "Female"
                  ],
                  "personalDetails[dob]":[
                     "1995-12-31"
                  ],
                  "personalDetails[blood_group]":[
                     "A-"
                  ],
                  "personalDetails[fathers_name]":[
                     "Md. Nurul Islam"
                  ],
                  "personalDetails[mothers_name]":[
                     "Ramesa Begum"
                  ],
                  "personalDetails[marital_status]":[
                     "Widowed"
                  ],
                  "personalDetails[spouse_name]":[
                     "Shamima Yasmin Eva"
                  ],
                  "personalDetails[nationality]":[
                     "Bangladeshi"
                  ],
                  "personalDetails[religion]":[
                     "5"
                  ],
                  "personalDetails[personal_email]":[
                     "gm@nazmulhussain.com"
                  ],
                  "personalDetails[personal_phone]":[
                     "01551761807"
                  ],
                  "personalDetails[nid_passport_no]":[
                     "4716444002516"
                  ],
                  "personalDetails[tin_no]":[
                     "542516"
                  ],
                  "personalDetails[present_address][city]":[
                     "Dhaka"
                  ],
                  "personalDetails[present_address][state_division]":[
                     "Dhaka"
                  ],
                  "personalDetails[present_address][post_zip_code]":[
                     "1216"
                  ],
                  "personalDetails[present_address][country]":[
                     "Bangladesh"
                  ],
                  "personalDetails[present_address][address]":[
                     "Mirpur 13"
                  ],
                  "personalDetails[permanent_address][city]":[
                     "Khulna"
                  ],
                  "personalDetails[permanent_address][state_division]":[
                     "Khulna"
                  ],
                  "personalDetails[permanent_address][post_zip_code]":[
                     "9280"
                  ],
                  "personalDetails[permanent_address][country]":[
                     "Bangladesh"
                  ],
                  "personalDetails[permanent_address][address]":[
                     "Protapkati, Paikgacha"
                  ],
                  "officialDetails[official_id]":[
                     "API230749"
                  ],
                  "officialDetails[official_email]":[
                     "nazmul.hussain@apisolutionsltd.com"
                  ],
                  "officialDetails[official_phone]":[
                     "01552451427"
                  ],
                  "officialDetails[password]":[
                     "Nazmul@1234"
                  ],
                  "officialDetails[employee_type]":[
                     "Permanent"
                  ],
                  "officialDetails[company]":[
                     "5"
                  ],
                  "officialDetails[branch]":[
                     "1"
                  ],
                  "officialDetails[department]":[
                     "5"
                  ],
                  "officialDetails[designation]":[
                     "1"
                  ],
                  "officialDetails[shift]":[
                     "5"
                  ],
                  "officialDetails[grade]":[
                     "5"
                  ],
                  "officialDetails[role_permission][0]":[
                     "5"
                  ],
                  "officialDetails[role_permission][1]":[
                     "5"
                  ],
                  "officialDetails[official_note]":[
                     ""
                  ],
                  "officialDetails[ethnic_group][0]":[
                     "1"
                  ],
                  "officialDetails[joining_date]":[
                     "2023-07-16"
                  ],
                  "officialDetails[supervisor]":[
                     "API230747"
                  ],
                  "officialDetails[expense_approver]":[
                     "API230747"
                  ],
                  "officialDetails[leave_approver]":[
                     "API230747"
                  ],
                  "officialDetails[shift_request_approver]":[
                     "API230747"
                  ],
                  "salaryAndLeaves[payment_in]":[
                     "Cash"
                  ],
                  "salaryAndLeaves[bank_account][bank_name]":[
                     "Islami Bank Bangladesh PLC"
                  ],
                  "salaryAndLeaves[bank_account][branch_name]":[
                     "Mirpur"
                  ],
                  "salaryAndLeaves[bank_account][account_type]":[
                     "1"
                  ],
                  "salaryAndLeaves[bank_account][account_no]":[
                     "25412523655"
                  ],
                  "salaryAndLeaves[bank_account][routing_no]":[
                     "254152"
                  ],
                  "salaryAndLeaves[bank_account][swift_bic]":[
                     "AAAA-BBBB-CCCC"
                  ],
                  "salaryAndLeaves[bank_account][address][city]":[
                     "Dhaka"
                  ],
                  "salaryAndLeaves[bank_account][address][state_division]":[
                     "Dhaka"
                  ],
                  "salaryAndLeaves[bank_account][address][post_zip_code]":[
                     "1202"
                  ],
                  "salaryAndLeaves[bank_account][address][country]":[
                     "Bangladesh"
                  ],
                  "salaryAndLeaves[bank_account][address][address]":[
                     "Mirpur 10"
                  ],
                  "salaryAndLeaves[gross_salary]":[
                     "25000"
                  ],
                  "salaryAndLeaves[leavepolicy][0]":[
                     "1"
                  ],
                  "emergencyContact[0][name]":[
                     "Nahida Akhter"
                  ],
                  "emergencyContact[0][age]":[
                     "25"
                  ],
                  "emergencyContact[0][phone_no]":[
                     "01552451425"
                  ],
                  "emergencyContact[0][email]":[
                     "nahida.mkt@gmail.com"
                  ],
                  "emergencyContact[0][address][city]":[
                     "Dhaka"
                  ],
                  "emergencyContact[0][address][state_division]":[
                     "Dhaka"
                  ],
                  "emergencyContact[0][address][post_zip_code]":[
                     "1204"
                  ],
                  "emergencyContact[0][address][country]":[
                     "Bangladesh"
                  ],
                  "emergencyContact[0][address][address]":[
                     "Mirpur"
                  ],
                  "emergencyContact[0][relation]":[
                     "Nahida Akhter"
                  ],
                  "academicRecord[0][certification]":[
                     "BSC"
                  ],
                  "academicRecord[0][board_institute_name]":[
                     "Daffodil International University"
                  ],
                  "academicRecord[0][level]":[
                     "Bachelor"
                  ],
                  "academicRecord[0][score_grade]":[
                     "3.75"
                  ],
                  "academicRecord[0][year_of_passing]":[
                     "2020"
                  ],
                  "academicRecord[1][certification]":[
                     "MSC"
                  ],
                  "academicRecord[1][board_institute_name]":[
                     "Daffodil International University"
                  ],
                  "academicRecord[1][level]":[
                     "Bachelor"
                  ],
                  "academicRecord[1][score_grade]":[
                     "3.75"
                  ],
                  "academicRecord[1][year_of_passing]":[
                     "2021"
                  ],
                  "previousExperience[0][company_name]":[
                     "Deeni Info Tech"
                  ],
                  "previousExperience[0][designation]":[
                     "Software Engineer"
                  ],
                  "previousExperience[0][from_date]":[
                     "2020-08-08"
                  ],
                  "previousExperience[0][to_date]":[
                     "2022-08-08"
                  ],
                  "previousExperience[0][address]":[
                     "Dhaka"
                  ],


                  
                  "uploadDocuments[0][title]":[
                     "NID/Passport"
                  ],
                  "uploadDocuments[1][title]":[
                     "Resume"
                  ],
                  "uploadDocuments[2][title]":[
                     "Appointment Letter"
                  ],
                  "uploadDocuments[2][attachment]":[
                     "null"
                  ],
                  "uploadDocuments[3][title]":[
                     "Photo"
                  ],
                  "uploadDocuments[0][attachment]":[
                    "employees.pdf (application/pdf)>"
                  ],
                  "uploadDocuments[1][attachment]":[
                     "employees.pdf (application/pdf)>"
                  ],
                  "uploadDocuments[3][attachment]":[
                     "ananta.jpg (image/jpeg)>"
                  ]
               }