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