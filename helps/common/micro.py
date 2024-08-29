from rest_framework import status
from helps.common.nano import Nanohelps
from datetime import datetime, timedelta
from helps.device.a_device import A_device as DEVICE
import os

class Microhelps(Nanohelps):

    def checkrequiredfiels(self, fields_tobe_checked): # New
        for index, item in enumerate(fields_tobe_checked):
            response_message = []
            data = item.get('data')
            if isinstance(data, dict):
                if data:
                    preparedata = data.copy()
                    if 'required_fields' in item:
                        required_fields = item['required_fields']
                        if isinstance(required_fields, list):
                            self.filterRequiredFields(required_fields, preparedata, response_message)
                            if 'to_be_apply' in item:
                                if isinstance(item['to_be_apply'], list):
                                    for field in item['to_be_apply']:
                                        if isinstance(item[field], list):
                                            if field == 'fields_regex': self.filterRegexFields(item[field], preparedata, response_message)
                                            elif field == 'choice_fields': self.filterChoiceFields(item[field], preparedata, response_message)
                                        else: response_message.append(f'index {index}\'s {item[field]} should be list!')
                                else: response_message.append(f'index {index}\'s to_be_apply should be list!')
                        else: response_message.append(f'index {index}\'s required_fields should be list!')
                    else: response_message.append(f'index {index}\'s required_fields is required!')
                else: response_message.append(f'index {index}\'s data shouldn\'t be empty!')
            else: response_message.append(f'index {index}\'s data type should be dict!')
            return response_message

    def addtocolass(self, classOBJ=None, Serializer=None, data=None, allowed_fields='__all__', unique_fields=[], required_fields=[], extra_fields={}, choice_fields=[], fields_regex=[]): # New
        response_data = {}
        response_message = []
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        if classOBJ:
            if Serializer:
                if data:
                    preparedata = {}
                    self.filterAllowedFields(allowed_fields, data, preparedata)
                    self.filterUniqueFields(classOBJ, unique_fields, preparedata, response_message)
                    preparedata.update(extra_fields)
                    self.filterChoiceFields(choice_fields, preparedata, response_message)
                    self.filterRequiredFields(required_fields, preparedata, response_message)
                    self.filterRegexFields(fields_regex, preparedata, response_message)
                    if not response_message:
                        serializer = Serializer(data=preparedata, many=False)
                        if serializer.is_valid():
                            try:    
                                serializer.save()
                                response_data = serializer
                                response_successflag = 'success'
                                response_status = status.HTTP_201_CREATED
                            except:
                                print(serializer)
                                response_message.append('unique combination is already exist!')
                        else:
                            print(serializer.errors)
                            try:
                                for field_name in serializer.errors.keys():
                                    for error in serializer.errors.get(field_name):
                                        response_message.append(error)
                            except: response_message.append('something went wrong!')
                else: response_message.append('please provide data!')
            else: response_message.append('provide serializer!')
        else: response_message.append('please provide a Model!')
        return response_data, response_message, response_successflag, response_status
    
    def updaterecord(self, classOBJ=None, Serializer=None, id=None, data={}, allowed_fields='__all__', unique_fields=[], freez_update=[], continue_update=[], extra_fields={}, choice_fields=[], fields_regex=[], static_fields=[]): # New
        response_data = {}
        response_message = []
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        
        if classOBJ:
            if Serializer:
                if id:
                    if data:
                        classobj = classOBJ.objects.filter(id=id)
                        if classobj.exists():
                            preparedata = {}
                            self.filterAllowedFields(allowed_fields, data, preparedata)
                            self.filterUniqueFields(classOBJ, unique_fields, preparedata, response_message, recordid=classobj.first().id)
                            if extra_fields: preparedata.update(extra_fields)
                            self.filterFreezFields(classobj, freez_update, response_message)
                            self.filterContinueFields(classobj, continue_update, response_message)
                            self.filterChoiceFields(choice_fields, preparedata, response_message)
                            self.filterRegexFields(fields_regex, preparedata, response_message)
                            if not response_message:
                                serializer = Serializer(instance=classobj.first(), data=preparedata, partial=True)
                                if serializer.is_valid():
                                    try:
                                        for static_field in static_fields:
                                            self.removeFile(classobj.first(), static_field)
                                        serializer.save()

                                        response_data = serializer
                                        response_successflag = 'success'
                                        response_status = status.HTTP_200_OK
                                    except: response_message.append('unique combination is already exist!')
                                else:
                                    print(serializer.errors)
                                    response_message.append('Something Went wrong!')
                        else: response_message.append('doesn\'t exist!')
                    else: response_message.append('please provide data!')
                else: response_message.append('please provide an id!')
            else: response_message.append('provide serializer!')
        else: response_message.append('please provide a Model!')
        return response_data, response_message, response_successflag, response_status
    
    def deleterecord(self, classOBJ=None, id=None, classOBJpackage_tocheck_assciaativity=[], delete_associate_records = [], freez_delete=[], continue_delete=[]): # New
        response_data = {}
        response_message = []
        response_successflag = 'error'
        response_status = status.HTTP_409_CONFLICT
        
        if classOBJ:
            if id:
                classobj = classOBJ.objects.filter(id=id)
                if classobj.exists():
                    for classOBJpackage in classOBJpackage_tocheck_assciaativity:
                        for field in classOBJpackage['fields']:
                            if field['relation'] == 'onetoonefield':
                                if classOBJpackage['model'].objects.filter(**{field['field']: classobj.first()}).exists():
                                    response_message.append(f"can\'t delete, associated to {classOBJpackage['model'].__name__} class and exist record!")
                            if field['relation'] == 'foreignkey':
                                if classOBJpackage['model'].objects.filter(**{field['field']: classobj.first()}).exists():
                                    response_message.append(f"can\'t delete, associated to {classOBJpackage['model'].__name__} class and exist record!")
                            if field['relation'] == 'manytomanyfield':
                                if field['records']: response_message.append(f"can\'t delete, associated to {classOBJpackage['model'].__name__} class and exist record!")
                    
                    self.filterFreezFields(classobj, freez_delete, response_message)
                    self.filterContinueFields(classobj, continue_delete, response_message)
                    if not response_message:
                        try:
                            for fields in delete_associate_records:
                                if fields:
                                    record = getattr(classobj.first(), fields.pop(0))
                                    for field in fields: record = getattr(record, field)
                                    if record: record.delete()
                            classobj.delete()
                            response_successflag = 'success'
                            response_status = status.HTTP_202_ACCEPTED
                        except: response_message.append('something went wrong!')
                else: response_message.append('doesn\'t exist!')
            else: response_message.append('please provide an id!')
        else: response_message.append('please provide a Model!')
       
        return response_data, response_message, response_successflag, response_status

    def addbankaccount(self, classOBJpackage, serializerOBJpackage, data, createdInstance=None): # New
        response = {'flag': False, 'message': [], 'instance': {}}
        if data:
            if 'address' in data:
                if isinstance(data['address'], dict):
                    if data['address']:
                        required_fields = ['address', 'city', 'state_division', 'country']
                        responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                            classOBJ=classOBJpackage['Address'],
                            Serializer=serializerOBJpackage['Address'],
                            data=data['address'],
                            required_fields=required_fields
                        )
                        if responsesuccessflag == 'success':
                            data.update({'address': responsedata.instance.id})
                            if isinstance(createdInstance, list): createdInstance.append(responsedata.instance)
                        elif responsesuccessflag == 'error':
                            response['message'].extend([f'bank account address\'s {each}' for each in responsemessage])
                            del data['address']
                    else: del data['address']
                else: response['message'].append('bank aocount address\'s type should be dict!')
            if not response['flag']:
                required_fields = ['bank_name', 'branch_name', 'account_type', 'account_no', 'routing_no']
                responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                    classOBJ=classOBJpackage['Bankaccount'],
                    Serializer=serializerOBJpackage['Bankaccount'],
                    data=data,
                    required_fields=required_fields
                )
                if responsesuccessflag == 'success':
                    response['instance'] = responsedata.instance
                    response['flag'] = True
                    if isinstance(createdInstance, list): createdInstance.append(responsedata.instance)
                elif responsesuccessflag == 'error':
                    response['message'].extend([f'bank account\'s {each}' for each in responsemessage])
        return response
    
    def nestedObjectPrepare(self, details): # New
        response = {'flag': False, 'message': [], 'data': {}}
        if details: 
            if isinstance(details, dict):
                if 'order' in details:
                    if isinstance(details['order'], list):
                        
                        success = True
                        createdInstances = []
                        order_list = details['order'].copy()
                        last_staged_data = None
                        while order_list:
                            data = details['data'].copy()
                            complete = True
                            for key in order_list:
                                if key in data:
                                    last_staged_data = data
                                    data = data[key]
                                else:
                                    response['message'].append('order keys are not in order!')
                                    complete = False
                                    break
                            last_key = order_list.pop()
                            if complete:
                                allowed_fields = details['info'][last_key]['allowed_fields'] if 'allowed_fields' in details['info'][last_key] else '__all__'
                                unique_fields = details['info'][last_key]['unique_fields'] if 'unique_fields' in details['info'][last_key] else []
                                required_fields = details['info'][last_key]['required_fields'] if 'required_fields' in details['info'][last_key] else []
                                extra_fields = details['info'][last_key]['extra_fields'] if 'extra_fields' in details['info'][last_key] else {}
                                choice_fields = details['info'][last_key]['choice_fields'] if 'choice_fields' in details['info'][last_key] else []
                                fields_regex = details['info'][last_key]['fields_regex'] if 'fields_regex' in details['info'][last_key] else []
                                responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                                    classOBJ=details['info'][last_key]['model'],
                                    Serializer=details['info'][last_key]['serializer'],
                                    data=data,
                                    allowed_fields=allowed_fields,
                                    unique_fields=unique_fields,
                                    required_fields=required_fields,
                                    extra_fields=extra_fields,
                                    choice_fields=choice_fields,
                                    fields_regex=fields_regex,
                                )
                                if responsesuccessflag == 'success':
                                    last_staged_data[last_key] = responsedata.instance.id
                                    createdInstances.append(responsedata.instance)
                                elif responsesuccessflag == 'error':
                                    response['message'].extend([f'{last_key}\'s {each}' for each in responsemessage])
                                    success = False
                                    break
                            else:
                                success = False
                                break
                        if success:
                            response['data'] = last_staged_data
                            response['flag'] = True
                        else:
                            for createdInstance in createdInstances: createdInstance.delete()
                    else: response['message'].append('order should be list type!')
                else: response['message'].append('order is required!')
            else: response['message'].append('details should be dict type!')
        return response
        


    
    def validateprofilepic(self, image):
      response = {'flag': False, 'message': []}
      if image != None:
         image_name = image._name
         if '.jpg' in image_name[len(image_name)-4:]:
               if image.size <= 99999: response['flag'] = True
               else: response['message'].append('provide an image within 100kb!')
         else: response['message'].append('image should be jpg format!')
      else: response['message'].append('no image provided!')
      return response
    
    def getInfoOfUserToRemoveFromDevice(self, Devicegroup, Userdevicegroup, devicegroupid): # New
        remove_info_from_device = []
        devicegroup = Devicegroup.objects.filter(id=devicegroupid)
        if devicegroup.exists():
            
            deviceid = devicegroup.first().device.id
            ip = devicegroup.first().device.deviceip
            uname = devicegroup.first().device.username
            pword = devicegroup.first().device.password
            device_name = devicegroup.first().device.title
            info_for_device = {'ip': ip, 'uname': uname, 'pword': pword, 'device_name': device_name}
            userdevicegroups = Userdevicegroup.objects.filter(group=devicegroup.first().group.id)
            for userdevicegroup in userdevicegroups:
                id_user = userdevicegroup.user.id
                userid = userdevicegroup.user.official_id
                assgned_user_devicegroup = Userdevicegroup.objects.filter(user=id_user).exclude(id=userdevicegroup.id)
                groupids = [each.group.id for each in assgned_user_devicegroup]
                assigned_devices = [each.device.id for each in Devicegroup.objects.filter(group__in=groupids)]
                
                if deviceid not in assigned_devices:
                    full_name = userdevicegroup.user.get_full_name()
                    group_name = userdevicegroup.group.title
                    info_for_device.update({'userid': userid, 'full_name': full_name, 'group_name': group_name})
                    remove_info_from_device.append(info_for_device)
        return remove_info_from_device
    
    # def addUserToDevice(self, user, device): # New
    #     response = {'flag': False, 'message': []}

    #     ip = device.deviceip
    #     uname = device.username
    #     pword = device.password

    #     userid = user.first().official_id
    #     name = user.first().get_full_name()
    #     cardno = user.first().uniqueid
    #     reg_date = user.first().joining_date

    #     if cardno == None:
    #         uniqueid_flag = False
    #         while not uniqueid_flag:
    #             try:
    #                 cardno = self.generateUniqueCode()
    #                 user.update(uniqueid=cardno)
    #                 uniqueid_flag = True
    #             except: pass
        
    #     if userid: response['message'].append('official_id is missing, this user can\'t register to device without official_id!')
    #     if reg_date: response['message'].append('joining_date is missing, this user can\'t register to device without joining_date!')
    #     if name: response['message'].append('either first_name or last_name is required!')
        
    #     if not response['message']:
    #         password = userid
    #         valid_date = reg_date + timedelta(days=3650)
    #         reg_date = f'{reg_date}'.replace('-', '')
    #         valid_date = f'{valid_date}'.replace('-', '')

    #         if user.first().photo:
    #             if user.first().photo.path:
    #                 if os.path.exists(user.first().photo.path):
    #                     image_paths = [user.first().photo.path]
    #                     existance_response = DEVICE().existanceofuser(ip, userid, uname, pword)
    #                     if existance_response['flag']:
    #                         DEVICE().deleteusrallimg(ip, userid, uname, pword)
    #                         if DEVICE().addphototouser(ip, name, userid, image_paths, uname, pword):
    #                             response['message'].append(f'successfully {name} added to the device({ip})')
    #                         else: response['message'].append(f'created user({name}) instance at device({ip}) but couldn\'t add image!')
    #                         response['flag'] = True
    #                     else:
    #                         user_train_and_add_image = DEVICE().createUserAndTrainImage(ip, name, cardno, userid, image_paths, password, reg_date,  valid_date, uname, pword)
    #                         if user_train_and_add_image['flag']:
    #                             response['message'].append(f'successfully {name} added to the device({ip}).')
    #                             response['flag'] = True
    #                         else: response['message'].extend(user_train_and_add_image['message'])
    #                 else:
    #                     existance_response = DEVICE().existanceofuser(ip, userid, uname, pword)
    #                     if existance_response['flag']:
    #                         DEVICE().deleteusrallimg(ip, userid, uname, pword)
    #                         response['message'].append(f'already {name} exist in this device({ip}).')
    #                         response['flag'] = True
    #                     else:
    #                         withoutimg_response = DEVICE().insertusrwithoutimg(ip, name, cardno, userid, password, reg_date,  valid_date, uname, pword)
    #                         if withoutimg_response['flag']:
    #                             response['message'].append(f'successfully {name} added to the device({ip}), without image(No image in database).')
    #                             response['flag'] = True
    #                         else: response['message'].extend(withoutimg_response['message'])
    #             else:
    #                 existance_response = DEVICE().existanceofuser(ip, userid, uname, pword)
    #                 if existance_response['flag']:
    #                     DEVICE().deleteusrallimg(ip, userid, uname, pword)
    #                     response['message'].append(f'already {name} exist in this device({ip}).')
    #                     response['flag'] = True
    #                 else:
    #                     withoutimg_response = DEVICE().insertusrwithoutimg(ip, name, cardno, userid, password, reg_date,  valid_date, uname, pword)
    #                     if withoutimg_response['flag']:
    #                         response['message'].append(f'successfully {name} added to the device({ip}), without image(No image in database).')
    #                         response['flag'] = True
    #                     else: response['message'].extend(withoutimg_response['message'])
    #         else:
    #             existance_response = DEVICE().existanceofuser(ip, userid, uname, pword)
    #             if existance_response['flag']:
    #                 DEVICE().deleteusrallimg(ip, userid, uname, pword)
    #                 response['message'].append(f'already {name} exist in this device({ip}).')
    #                 response['flag'] = True
    #             else:
    #                 withoutimg_response = DEVICE().insertusrwithoutimg(ip, name, cardno, userid, password, reg_date,  valid_date, uname, pword)
    #                 if withoutimg_response['flag']:
    #                     response['message'].append(f'successfully {name} added to the device({ip}), without image(No image in database).')
    #                     response['flag'] = True
    #                 else: response['message'].extend(withoutimg_response['message'])
    #     return response
    
    def registerUserToDevice(self, user_info): # New
        response = {'flag': False, 'message': []}
        for info in user_info:
            if 'image_paths' in info:
                existance_response = DEVICE().existanceofuser(info['ip'], info['userid'], info['uname'], info['pword'])
                if existance_response['flag']:
                    DEVICE().deleteusrallimg(info['ip'], info['userid'], info['uname'], info['pword'])
                    if DEVICE().addphototouser(info['ip'], info['name'], info['userid'], info['image_paths'], info['uname'], info['pword']):
                        response['message'].append(f'successfully {info["name"]} added to the device({info["ip"]})')
                    else: response['message'].append(f'created user({info["name"]}) instance at device({info["ip"]}) but couldn\'t add image!')
                    response['flag'] = True
                else:
                    user_train_and_add_image = DEVICE().createUserAndTrainImage(info['ip'], info['name'], info['cardno'], info['userid'], info['image_paths'], info['password'], info['reg_date'],  info['valid_date'], info['uname'], info['pword'])
                    if user_train_and_add_image['flag']:
                        response['message'].append(f'successfully {info["name"]} added to the device({info["ip"]}).')
                        response['flag'] = True
                    else: response['message'].extend(user_train_and_add_image['message'])
            else:
                existance_response = DEVICE().existanceofuser(info['ip'], info['userid'], info['uname'], info['pword'])
                if existance_response['flag']:
                    DEVICE().deleteusrallimg(info['ip'], info['userid'], info['uname'], info['pword'])
                    response['message'].append(f'already {info["name"]} exist in this device({info["ip"]}).')
                    response['flag'] = True
                else:
                    withoutimg_response = DEVICE().insertusrwithoutimg(info['ip'], info['name'], info['cardno'], info['userid'], info['password'], info['reg_date'],  info['valid_date'], info['uname'], info['pword'])
                    if withoutimg_response['flag']:
                        response['message'].append(f'successfully {info["name"]} added to the device({info["ip"]}), without image(No image in database).')
                        response['flag'] = True
                    else: response['message'].extend(withoutimg_response['message'])
        return response