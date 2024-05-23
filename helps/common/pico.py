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
    
    def prepareuserobject(self):
        return {
                    "personalDetails":{
                        "first_name": None,
                        "last_name": None,
                        "gender": None,
                        "dob": None,
                        "blood_group": None,
                        "fathers_name": None,
                        "mothers_name": None,
                        "marital_status": None,
                        "spouse_name": None,
                        "nationality": None,
                        "religion": None,
                        "personal_email": None,
                        "personal_phone": None,
                        "nid_passport_no": None,
                        "tin_no": None,
                        "present_address":{
                            "city": None,
                            "state_division": None,
                            "post_zip_code": None,
                            "country": None,
                            "address": None
                        },
                        "permanent_address":{
                            "city": None,
                            "state_division": None,
                            "post_zip_code": None,
                            "country": None,
                            "address": None
                        }
                },
                "officialDetails":{
                    "official_id": None,
                    "official_email": None,
                    "official_phone": None,
                    "password": None,
                    "employee_type": None,
                    "company": None,
                    "branch": None,
                    "department": None,
                    "designation": None,
                    "shift": None,
                    "grade": None,
                    "role_permission": None,
                    "official_note": None,
                    "ethnic_group": None,
                    "joining_date": None,
                    "supervisor": None,
                    "expense_approver": None,
                    "leave_approver": None,
                    "shift_request_approver": None
                },
                "salaryAndLeaves":{
                    "payment_in":"Cash",
                    "bank_account":{
                        "bank_name":"Prime Bank",
                        "branch_name":"Banani",
                        "account_type":1,
                        "account_no":"126521460000525",
                        "routing_no":"98541222220540",
                        "swift_bic":"AAAA-BB-CC-123",
                        "address":{
                            "city":"Dhaka",
                            "state_division":"Dhaka",
                            "post_zip_code":"1213",
                            "country":"Bangladesh",
                            "address":"62 Block - E, Kemal Ataturk Avenue, Banani, Dhaka 1213"
                        }
                    },
                    "gross_salary":10000,
                    "leavepolicy": [1]
                },
                "emergencyContact":[
                        {
                            "name":"Joynal Hossain",
                            "age":50,
                            "phone_no":"01745625578",
                            "email":"",
                            "address":{
                                "city":"Faridpur",
                                "state_division":"Dhaka",
                                "post_zip_code":"5607",
                                "country":"Bangladesh",
                                "address":"Kalamridha, Sardar Bari"
                            },
                            "relation":"Father"
                        },
                        {
                            "name":"Jakir Hossain",
                            "age":20,
                            "phone_no":"01745625588",
                            "email":"jakir@jakir.com",
                            "address":{
                                "city":"Faridpur",
                                "state_division":"Dhaka",
                                "post_zip_code":"5607",
                                "country":"Bangladesh",
                                "address":"Kalamridha, Sardar Bari"
                            },
                            "relation":"Brother"
                        }
                ],
                "academicRecord":[
                        {
                            "certification":"Secondary School Certificate",
                            "board_institute_name":"Faridpur Zila High School",
                            "level":"SSC",
                            "score_grade":"5.00",
                            "year_of_passing":2014
                        },
                        {
                            "certification":"Higher Secondary Certificate",
                            "board_institute_name":"KM College",
                            "level":"HSC",
                            "score_grade":"4.60",
                            "year_of_passing":2016
                        },
                        {
                            "certification":"Bachelor of Science in Computer Science and Engineering",
                            "board_institute_name":"Green University",
                            "level":"B.Sc",
                            "score_grade":"3.14",
                            "year_of_passing":2020
                        }
                ],
                "previousExperience":[
                        {
                            "company_name":"5 minutes solutions ltd",
                            "designation":"Intern Frontend Develover",
                            "address":"Jatrabari, Hujur Bari Gate",
                            "from_date":"2020-02-01",
                            "to_date":"2020-05-01"
                        }
                ],
                "uploadDocuments": [
                        {
                            "title": "nid",
                            "attachment": "nid File"
                        },
                        {
                            "title": "cv",
                            "attachment": "cv File"
                        },
                        {
                            "title": "appointmentLetter",
                            "attachment": "appointmentLetter File"
                        },
                        {
                            "title": "photo",
                            "attachment": "photo File"
                        }
                ]
                }