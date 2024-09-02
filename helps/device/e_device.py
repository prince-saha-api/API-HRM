from datetime import datetime, date, timedelta
import pytz

class E_device:

    def convert_STR_int_datetime_y_m_d_h_m_s_six(self, strdatetime):
      strdatetime = datetime.utcfromtimestamp(int(strdatetime))
      strdatetime = pytz.timezone('UTC').localize(strdatetime)
      return strdatetime.astimezone(pytz.timezone('Asia/Dhaka'))