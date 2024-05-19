from helps.common.generic import Generichelps as ghelp
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

from helps.accesscontroldevice.b_devicehelp import Decicehelpsb

class Decicehelps(Decicehelpsb):
    
    def existanceofuserfromalldevices(self, GroupDevice, Devices, employee_id, groupid, devices = None):
        response = { 'flag': False, 'device_blank': False , 'active':[], 'inactive': [] }
        if devices == None: devices = GroupDevice.objects.filter(group_id=groupid).values_list('device_id', flat=True)
        response.update({'devices': devices})

        if devices:
            for device in devices:
                device_response = self.getDeviceIpUsernamePassword(Devices, device)
                if device_response['flag']:
                    if device_response['data']['deviceactivity'] and self.is_device_active(device_response['data']['deviceip']):
                        if self.existanceofuser(device_response['data']['deviceip'], employee_id, device_response['data']['deviceusername'], device_response['data']['devicepassword']): response['flag'] = True
                        response['active'].append({'deviceip': device_response['data']['deviceip'], 'deviceusername': device_response['data']['deviceusername'], 'devicepassword': device_response['data']['devicepassword'], 'deviceactivity': device_response['data']['deviceactivity']})
                    else: response['inactive'].append({'deviceip': device_response['data']['deviceip'], 'deviceusername': device_response['data']['deviceusername'], 'devicepassword': device_response['data']['devicepassword'], 'deviceactivity': device_response['data']['deviceactivity']})
        else: response['device_blank'] = True
        return response
    
    def trainemployeewithoutimg(self, employee, devices):
        response = {'flag': False, 'train': False, 'details': {}}
        username = employee['username']
        cardno = employee['cardNo']
        employee_id = employee['employee_id']
        password = employee['password']
        reg_date = f"{employee['registration_date']}".replace('-', '')
        valid_date = employee['validity_date'].replace('-', '')
        for device in devices['active']:
            deviceip = device['deviceip']
            deviceusername = device['deviceusername']
            devicepassword = device['devicepassword']
            if self.insertusrwithoutimg(deviceip, username, cardno, employee_id, password, reg_date,  valid_date, deviceusername, devicepassword):
                response['flag'] = True
                response['train'] = True
                response['details'].update({deviceip: {'deviceip': deviceip, 'addeduser': True, 'addedimg': False}})
            else: response['details'].update({deviceip: {'deviceip': deviceip, 'addeduser': False, 'addedimg': False}})
        return response
    
    def trainemployeewithimg(self, employee, devices):
        response = {'flag': False, 'train': False, 'details': {}}
        username = employee['username']
        cardno = employee['cardNo']
        employee_id = employee['employee_id']
        password = employee['password']
        reg_date = f"{employee['registration_date']}".replace('-', '')
        valid_date = employee['validity_date'].replace('-', '')
        image_paths = [self.getimagepath(employee['image'])]

        for device in devices['active']:
            deviceip = device['deviceip']
            deviceusername = device['deviceusername']
            devicepassword = device['devicepassword']
            if self.insertusrwithoutimg(deviceip, username, cardno, employee_id, password, reg_date,  valid_date, deviceusername, devicepassword):
                response['flag'] = True
                response['train'] = True
                response['details'].update({deviceip: {'deviceip': deviceip, 'addeduser': True, 'addedimg': False}})
                if self.addphototouser(image_paths, deviceip, employee_id, username, deviceusername, devicepassword)['flag']:
                    response['details'][deviceip]['addedimg'] = True
                else:
                    self.deleteusr(deviceip, employee_id, deviceusername, devicepassword)
                    response['flag'] = False
                    response['train'] = False
                    response['details'][deviceip]['addeduser'] = False
            else: response['details'].update({deviceip: {'deviceip': deviceip, 'addeduser': False, 'addedimg': False}})
        return response

    def getAllLogs(self, device, starttime, endtime, count, usernames, logs = {}):
        raw_logs = []
        first = True
        previousstarttime = -1
        while previousstarttime != starttime:
            previousstarttime = starttime
            new_logs, starttime = self.getLogsValueAndEndtime(device, starttime, endtime, count)
            if first:
                raw_logs.extend(new_logs)
                count += 1
                first = False
            else: raw_logs.extend(new_logs[1:])

        self.filterLogs(raw_logs, usernames, logs)