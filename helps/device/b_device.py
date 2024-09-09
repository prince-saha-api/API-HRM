from helps.device.c_device import C_device
from requests.auth import HTTPDigestAuth
import requests

class B_device(C_device):

    def getLogsValueAndEndtime(self, device, starttime, endtime, count):
        CreateTime = ''
        DEVICE_RESPONSE = self.getLogsValue(device, starttime, endtime, count)
        if DEVICE_RESPONSE['data']: CreateTime = DEVICE_RESPONSE['data'][-1].get('CreateTime')
        return DEVICE_RESPONSE['data'], CreateTime
    
    def filterLogs(self, raw_logs, officialids, logs, officialidsonly=True):
        for raw_log in raw_logs:
            UserID = raw_log['UserID']
            CreateTime = f"{self.convert_STR_int_datetime_y_m_d_h_m_s_six(raw_log['CreateTime'])}"
            datetime = CreateTime.split(' ')
            date = datetime[0]
            time = datetime[1].split('+')[0]

            if officialidsonly:
                if UserID in officialids:
                    if UserID not in logs: logs.update({UserID: {}})
                    if date not in logs[UserID]: logs[UserID].update({date: []})
                    if time not in logs[UserID][date]: logs[UserID][date].append(time)
            else:
                if UserID:
                    if UserID not in logs: logs.update({UserID: {}})
                    if date not in logs[UserID]: logs[UserID].update({date: []})
                    if time not in logs[UserID][date]: logs[UserID][date].append(time) 
    
    def addphototouser(self, ip, name, userid, image_paths, uname, pword):
        response = {'flag': False, 'message': []}
        url=f"http://{ip}/cgi-bin/FaceInfoManager.cgi?action=add"
        data={
            "UserID": userid,
            "Info":{
                "UserName": name,
                "PhotoData": self.getPhotoData(image_paths)
            }
        }
        try:
            DEVICE_RAW_RESPONSE = requests.post(url, json=data, auth=HTTPDigestAuth(uname, pword), headers={"Content-Type":"application/json"})
            if DEVICE_RAW_RESPONSE.status_code == 200: response['flag'] = True
        except: response['message'].append(f'might be device({ip}) is switched off!')
        return response
    
#     def deleteusrcheckingexistance(self, GroupDevice, Devices, employee_id, group_id):
#         flag = False
#         devices = GroupDevice.objects.filter(group_id=group_id).values_list('device_id', flat=True)
#         for device in devices:
#             _, _, deviceip, deviceusername, devicepassword, deviceactivity = self.getDeviceIpUsernamePassword(Devices, device)
#             if deviceactivity and self.is_device_active(deviceip):
#                 if self.existanceofuser(deviceip, employee_id, deviceusername, devicepassword):
#                     if self.deleteusr(deviceip, employee_id, deviceusername, devicepassword): flag = True
#         return flag
    
#     def getAllLogs(self, deviceip, starttime, endtime, count, deviceusername, devicepassword):
#         raw_logs = []
#         first = True
#         previousstarttime = -1
#         while previousstarttime != starttime:
#             previousstarttime = starttime
#             logs, starttime = self.getLogsValueAndEndtime(deviceip, starttime, endtime, count, deviceusername, devicepassword)
#             if first:
#                 raw_logs.extend(logs)
#                 count += 1
#                 first = False
#             else: raw_logs.extend(logs[1:])
#         return raw_logs