from helps.device.c_device import C_device
from requests.auth import HTTPDigestAuth
import requests

class B_device(C_device):
    
    def addphototouser(self, ip, name, userid, image_paths, uname, pword):
        flag = False
        url=f"http://{ip}/cgi-bin/FaceInfoManager.cgi?action=add"
        data={
            "UserID": userid,
            "Info":{
                "UserName": name,
                "PhotoData": self.getPhotoData(image_paths)
            }
        }
        resp = requests.post(url, json=data, auth=HTTPDigestAuth(uname, pword), headers={"Content-Type":"application/json"})
        if resp.status_code == 200: flag = True
        return flag
    
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