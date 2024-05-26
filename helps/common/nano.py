from helps.common.pico import Picohelps

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
    
    def claculatebuffertime(self, GlobalBufferTime, entranceexitdetails):
        globalbuffertime = GlobalBufferTime.objects.all()
        if globalbuffertime.count() == 0: GlobalBufferTime.objects.create()
        globalbuffertime = GlobalBufferTime.objects.filter(is_active=True).first()

        late_in_based_on_buffertime = 0
        if entranceexitdetails['late_entrance']>globalbuffertime.buffer_time_for_enter_minutes:
            late_in_based_on_buffertime = (entranceexitdetails['late_entrance']-globalbuffertime.buffer_time_for_enter_minutes)/60

        early_leave_based_on_buffertime = 0
        if entranceexitdetails['early_exit']>globalbuffertime.buffer_time_for_leave_minutes:
            early_leave_based_on_buffertime = (entranceexitdetails['early_exit']-globalbuffertime.buffer_time_for_leave_minutes)/60

        buffer_time_minutes = f'{globalbuffertime.buffer_time_for_enter_minutes} - {globalbuffertime.buffer_time_for_leave_minutes}'
        
        return {
            'late_in_based_on_buffertime': late_in_based_on_buffertime,
            'early_leave_based_on_buffertime': early_leave_based_on_buffertime,
            'buffer_time_minutes': buffer_time_minutes
        }
    
    def getofficeoffday(self, Offday, date):
        date = self.convert_STR_datetime_date(date)
        offday = Offday.objects.filter(day=self.convert_y_m_d_STR_day(date), is_active=True)

        return offday.first() if offday.exists() else None
    
    def removedoublequotation(self, string):
        if string:
            if string[0] == '"':
                if string[len(string)-1] == '"':
                    string = string[1:len(string)]
                    string = string[0:len(string)-1]
        return string
    
    def addaddress(self, Address, data): # New
        response = {
            'flag': True,
            'message': [],
            'instance': {}
        }
        # name = data.get('name')
        # if name == None:
        #     response['message'].append('name is required!')
        #     response['flag'] = False

        city = data.get('city')
        if city == None:
            response['message'].append('city is required!')
            response['flag'] = False

        state_division = data.get('state_division')
        if state_division == None:
            response['message'].append('state_division is required!')
            response['flag'] = False

        post_zip_code = data.get('post_zip_code')

        country = data.get('country')
        if country == None:
            response['message'].append('country is required!')
            response['flag'] = False

        address = data.get('address')
        if address == None:
            response['message'].append('address is required!')
            response['flag'] = False
        
        if response['flag']:
            addressinstance = Address()
            if city: addressinstance.city=city
            if state_division: addressinstance.state_division=state_division
            if post_zip_code: addressinstance.post_zip_code=post_zip_code
            if country: addressinstance.country=country
            if address: addressinstance.address=address
            addressinstance.save()
            response['instance'] = addressinstance
        return response
    
    def addacademicrecord(self, Employeeacademichistory, userinstance, academicRecord): # New
        response = {
            'flag': False,
            'failed': [],
            'message': ''
        }
        if isinstance(academicRecord, list):
            for details in academicRecord:
                create_flag = True
                reasons = []

                certification = details.get('certification')
                if certification == None:
                    reasons.append('certification field is required!')
                    create_flag = False

                board_institute_name = details.get('board_institute_name')
                if board_institute_name == None:
                    reasons.append('board_institute_name field is required!')
                    create_flag = False

                level = details.get('level')
                if level == None:
                    reasons.append('level field is required!')
                    create_flag = False

                score_grade = details.get('score_grade')
                if score_grade == None:
                    reasons.append('score_grade field is required!')
                    create_flag = False

                year_of_passing = details.get('year_of_passing')
                if year_of_passing == None:
                    reasons.append('year_of_passing field is required!')
                    create_flag = False

                if create_flag:
                    response['flag'] = True
                    employeeacademichistoryinstance = Employeeacademichistory()
                    employeeacademichistoryinstance.user=userinstance
                    if certification: employeeacademichistoryinstance.certification=certification
                    if board_institute_name: employeeacademichistoryinstance.board_institute_name=board_institute_name
                    if level: employeeacademichistoryinstance.level=level
                    if score_grade: employeeacademichistoryinstance.score_grade=score_grade
                    if year_of_passing: employeeacademichistoryinstance.year_of_passing=year_of_passing
                    employeeacademichistoryinstance.save()
                else: response['failed'].append({'data': details, 'message': reasons})
        else: response['message'] = 'academicrecord is not list type!'
        return response


    def addpreviousexperience(self, Employeeexperiencehistory, userinstance, previousExperience): # New
        response = {
            'flag': False,
            'failed': [],
            'message': ''
        }
        if isinstance(previousExperience, list):
            for details in previousExperience:
                create_flag = True
                reasons = []

                company_name = details.get('company_name')
                if company_name == None:
                    reasons.append('company_name field is required!')
                    create_flag = False

                designation = details.get('designation')
                if designation == None:
                    reasons.append('designation field is required!')
                    create_flag = False

                address = details.get('address')

                from_date = details.get('from_date')
                if from_date == None:
                    reasons.append('from_date field is required!')
                    create_flag = False

                to_date = details.get('to_date')
                if to_date == None:
                    reasons.append('to_date field is required!')
                    create_flag = False

                if create_flag:
                    response['flag'] = True
                    employeeexperiencehistoryinstance = Employeeexperiencehistory()
                    employeeexperiencehistoryinstance.user=userinstance
                    if company_name: employeeexperiencehistoryinstance.company_name=company_name
                    if designation: employeeexperiencehistoryinstance.designation=designation
                    if address: employeeexperiencehistoryinstance.address=address
                    if from_date: employeeexperiencehistoryinstance.from_date=from_date
                    if to_date: employeeexperiencehistoryinstance.to_date=to_date
                    employeeexperiencehistoryinstance.save()
                else: response['failed'].append({'data': details, 'message': reasons})
        else: response['message'] = 'previousexperience is not list type!'
        return response

    def getobject(self, classOBJ, id): # New
        object = None
        if id != None:
            try: object = classOBJ.objects.get(id=id)
            except: pass
        return object