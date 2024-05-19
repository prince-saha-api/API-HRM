from helps.common.generic import Generichelps as ghelp
from requests.auth import HTTPDigestAuth
from django.conf import settings
from pythonping import ping
from pathlib import Path
from PIL import Image
import requests
import base64
import os
import re

from helps.accesscontroldevice.c_apihelp import Apihelpsc

class Decicehelpsb(Apihelpsc):
    def getLogsValueAndEndtime(self, device, starttime, endtime, count):
        CreateTime = ''
        log_response = self.getLogsValue(device, starttime, endtime, count)
        if log_response['data']: CreateTime = log_response['data'][-1].get('CreateTime')
        return log_response['data'], CreateTime
    
    def filterLogs(self, raw_logs, usernames, logs, usernamesonly=True):
        for raw_log in raw_logs:
            CardName = raw_log['CardName']
            CreateTime = f"{ghelp().convert_STR_int_datetime_y_m_d_h_m_s_six(raw_log['CreateTime'])}"
            datetime = CreateTime.split(' ')
            date = datetime[0]
            time = datetime[1].split('+')[0]

            if usernamesonly:
                if CardName in usernames:
                    if CardName not in logs: logs.update({CardName: {}})
                    if date not in logs[CardName]: logs[CardName].update({date: []})
                    if time not in logs[CardName][date]: logs[CardName][date].append(time)
            else:
                if CardName:
                    if CardName not in logs: logs.update({CardName: {}})
                    if date not in logs[CardName]: logs[CardName].update({date: []})
                    if time not in logs[CardName][date]: logs[CardName][date].append(time) 