from helps.device.b_device import B_device

class A_device(B_device):

    def getAllLogs(self, device, starttime, endtime, count, officialids, logs = {}):
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
        self.filterLogs(raw_logs, officialids, logs)

    def createUserAndTrainImage(self, ip, name, cardno, userid, image_paths, password, reg_date,  valid_date, uname, pword):
        response = {'flag': False, 'message': []}
        DEVICE_RESPONSE = self.insertusrwithoutimg(ip, name, cardno, userid, password, reg_date,  valid_date, uname, pword)
        if DEVICE_RESPONSE['flag']:        
            if not self.addphototouser(ip, name, userid, image_paths, uname, pword):
                response['message'].append(f'created user({name}) instance at device({ip}) but couldn\'t add image!')
            response['flag'] = True
        else: response['message'].extend(DEVICE_RESPONSE['message'])
        return response
    
#     def trainemployeewithimg(self, employee, devices):
#         response = {'flag': False, 'train': False, 'details': {}}
#         username = employee['username']
#         cardno = employee['cardNo']
#         employee_id = employee['employee_id']
#         password = employee['password']
#         reg_date = f"{employee['registration_date']}".replace('-', '')
#         valid_date = employee['validity_date'].replace('-', '')
#         image_paths = [self.getimagepath(employee['image'])]

#         for device in devices['active']:
#             deviceip = device['deviceip']
#             deviceusername = device['deviceusername']
#             devicepassword = device['devicepassword']
#             if self.insertusrwithoutimg(deviceip, username, cardno, employee_id, password, reg_date,  valid_date, deviceusername, devicepassword):
#                 response['flag'] = True
#                 response['train'] = True
#                 response['details'].update({deviceip: {'deviceip': deviceip, 'addeduser': True, 'addedimg': False}})
#                 if self.addphototouser(image_paths, deviceip, employee_id, username, deviceusername, devicepassword):
#                     response['details'][deviceip]['addedimg'] = True
#                 else:
#                     self.deleteusr(deviceip, employee_id, deviceusername, devicepassword)
#                     response['flag'] = False
#                     response['train'] = False
#                     response['details'][deviceip]['addeduser'] = False
#             else: response['details'].update({deviceip: {'deviceip': deviceip, 'addeduser': False, 'addedimg': False}})
#         return response
    
#     def change_group_image(self, GroupDevice, Devices, previousgroupid, newgroupid, newdevices, employee_details):
#         flag = False
#         if previousgroupid != newgroupid:

#             username = employee_details.username
#             cardNo = employee_details.cardNo
#             employee_id = employee_details.employee_id
#             password = employee_details.password
#             reg_date = f'{employee_details.registration_date}'.replace('-', '')
#             valid_date = employee_details.validity_date.replace('-', '')

#             previousdevices= GroupDevice.objects.filter(group_id=previousgroupid).values_list('device_id', flat=True)
#             for device in previousdevices:
#                 _, _, deviceip, deviceusername, devicepassword, deviceactivity = self.getDeviceIpUsernamePassword(Devices, device)
#                 if deviceactivity and self.is_device_active(deviceip):
#                     if self.existanceofuser(deviceip, employee_id, deviceusername, devicepassword):
#                         self.deleteusr(deviceip, employee_id, deviceusername, devicepassword)

#             for newdevice in newdevices:
#                 _, _, deviceip, deviceusername, devicepassword, deviceactivity = self.getDeviceIpUsernamePassword(Devices, newdevice)
#                 if deviceactivity and self.is_device_active(deviceip):

#                     if self.insertusrwithoutimg(deviceip, username, cardNo, employee_id, password, reg_date, valid_date, deviceusername, devicepassword):
#                         if employee_details.image:
#                             if os.path.exists(employee_details.image.path):
#                                 image_paths = [employee_details.image.path]
#                                 flag_ = self.addphototouser(image_paths, deviceip, employee_id, username, deviceusername, devicepassword)
#                                 if flag_: flag = True
#                                 print('Changed Group')
#         else:
#             username = employee_details.username
#             employee_id = employee_details.employee_id
#             devices= GroupDevice.objects.filter(group_id=newgroupid).values_list('device_id', flat=True)

#             for device in devices:
#                 _, _, deviceip, deviceusername, devicepassword, deviceactivity = self.getDeviceIpUsernamePassword(Devices, device)
#                 if deviceactivity and self.is_device_active(deviceip):
#                     if self.existanceofuser(deviceip, employee_id, deviceusername, devicepassword):
#                         if self.deleteusrallimg(deviceip, employee_id, deviceusername, devicepassword)['flag']:
#                             if employee_details.image:
#                                 if os.path.exists(employee_details.image.path):
#                                     image_paths = [employee_details.image.path]
#                                     flag_ = self.addphototouser(image_paths, deviceip, employee_id, username, deviceusername, devicepassword)
#                                     if flag_: flag = True
#                                     print('Changed Image')
#         return flag