from helps.device.d_device import D_device
from requests.auth import HTTPDigestAuth
import requests

class C_device(D_device):
    
    def getPhotoData(self, image_paths):
        PhotoData = []
        for image_path in image_paths:
            self.resize_image(image_path,image_path,80)
            with open(image_path,"rb") as image:
                PhotoData.append(self.convertImgTobase64(image))
        return PhotoData
    
    def deleteusr(self, ip, userid, uname, pword):
        response = {'flag': False, 'message': []}
        record_response=self.get_record_number(ip, userid, uname, pword)
        if record_response['flag']:
            record_number = record_response['value']
            url=f"http://{ip}/cgi-bin/recordUpdater.cgi?action=remove&name=AccessControlCard&recno={record_number}"
            resp = requests.get(url,auth=HTTPDigestAuth(uname, pword))
            if resp.status_code==200: response['flag'] = True
        else: response['message'].extend(record_response['message'])
        return response

    # def existanceofuserfromalldevices(self, GroupDevice, Devices, employee_id, groupid, devices = None):
    #     response = {'device_blank': False , 'flag': False, 'active':[], 'inactive': []}
    #     if devices == None: devices = GroupDevice.objects.filter(group_id=groupid).values_list('device_id', flat=True)
    #     response.update({'devices': devices})

    #     if devices:
    #         for device in devices:
    #             _, _, deviceip, deviceusername, devicepassword, deviceactivity = self.getDeviceIpUsernamePassword(Devices, device)
    #             if deviceactivity and self.is_device_active(deviceip):
    #                 if self.existanceofuser(deviceip, employee_id, deviceusername, devicepassword): response['flag'] = True
    #                 response['active'].append({'deviceip': deviceip, 'deviceusername': deviceusername, 'devicepassword': devicepassword, 'deviceactivity': deviceactivity})
    #             else: response['inactive'].append({'deviceip': deviceip, 'deviceusername': deviceusername, 'devicepassword': devicepassword, 'deviceactivity': deviceactivity})
    #     else: response['device_blank'] = True
    #     return response

    # def trainemployeewithoutimg(self, employee, devices):
    #     response = {'flag': False, 'train': False, 'details': {}}
    #     username = employee['username']
    #     cardno = employee['cardNo']
    #     employee_id = employee['employee_id']
    #     password = employee['password']
    #     reg_date = f"{employee['registration_date']}".replace('-', '')
    #     valid_date = employee['validity_date'].replace('-', '')
    #     for device in devices['active']:
    #         deviceip = device['deviceip']
    #         deviceusername = device['deviceusername']
    #         devicepassword = device['devicepassword']
    #         if self.insertusrwithoutimg(deviceip, username, cardno, employee_id, password, reg_date,  valid_date, deviceusername, devicepassword):
    #             response['flag'] = True
    #             response['train'] = True
    #             response['details'].update({deviceip: {'deviceip': deviceip, 'addeduser': True, 'addedimg': False}})
    #         else: response['details'].update({deviceip: {'deviceip': deviceip, 'addeduser': False, 'addedimg': False}})
    #     return response
    
    # def if_device_is_active(self, GroupDevice, Devices, groupid):
    #     flag = False
    #     devices = GroupDevice.objects.filter(group_id=groupid).values_list('device_id', flat=True)
    #     for device in devices:
    #         _, _, deviceip, deviceusername, devicepassword, deviceactivity = self.getDeviceIpUsernamePassword(Devices, device)
    #         if deviceactivity and self.is_device_active(deviceip): flag = True
    #     return devices, flag

    # def getLogsValueAndEndtime(self, deviceip, starttime, endtime, count, deviceusername, devicepassword):
    #     CreateTime = ''
    #     logs = self.getLogsValue(deviceip, starttime, endtime, count, deviceusername, devicepassword)
    #     if logs: CreateTime = logs[-1].get('CreateTime')
    #     return logs, CreateTime