from helps.device.e_device import E_device
from requests.auth import HTTPDigestAuth
from django.conf import settings
from pythonping import ping
from pathlib import Path
from PIL import Image
import requests
import base64
import os
import re

class D_device(E_device):

    # def getDeviceIpUsernamePassword(self, Classobject, deviceid):
    #     device_id = ''
    #     device_name = ''
    #     ip = '0.0.0.0'
    #     username = 'admin'
    #     password = 'admin'
    #     activity = False
    #     objects = Classobject.objects.filter(id=deviceid)

    #     if objects.exists():
    #         object = objects.values("device_ip", "device_id", "device_name", "username", "password", "is_active").first()
    #         device_id = object.get('device_id', '')
    #         device_name = object.get('device_name', '')
    #         ip = object.get('device_ip', '0.0.0.0')
    #         username = object.get('username', 'admin')
    #         password = object.get('password', 'admin')
    #         activity = object.get('is_active', False)
    #     return device_id, device_name, ip, username, password, activity

    #############
    def is_device_active(self, ip):
        try:
            result = ping(ip, count=2)
            return result.success()
        except: return False
    
    def resize_image(self, input_path, output_path, max_size_kb):
        try:
            with Image.open(input_path) as img:
                original_size = os.path.getsize(input_path)
                original_width, original_height = img.size
                target_size_bytes = max_size_kb * 1024
                scale_factor = 1.0
                if original_size > target_size_bytes:
                    scale_factor = (target_size_bytes / original_size) ** 0.5
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                resized_img.thumbnail((230, 230))
                resized_img.save(output_path, optimize=True, quality=100)
        except MemoryError as e: pass

    def convertImgTobase64(self, image):
        img=image.read()
        base64_img=base64.b64encode(img)
        return base64_img.decode("utf-8")
    
    #############
    def get_record_number(self, ip, userid, uname, pword):
        response = {'flag': False, 'message': [], 'value': None}
        url=f"http://{ip}/cgi-bin/recordFinder.cgi?action=find&name=AccessControlCard&condition.UserID={userid}"
        try:
            DEVICE_RAW_RESPONSE=requests.get(url, auth=HTTPDigestAuth(uname, pword))
            matched_list = re.findall('RecNo=[0-9][0-9]*', DEVICE_RAW_RESPONSE.text)
            if matched_list:
                response['value'] = int(matched_list[0].split('=')[1])
                response['flag'] = True
            else: response['message'].append(f'no record_no founded, userid({userid}), device({ip})')
        except: response['message'].append(f'might be device({ip}) is switched off!')
        return response
    
    #############
    def existanceofuser(self, ip, userid, uname, pword):
        response = {'flag': False, 'message': []}
        url=f"http://{ip}/cgi-bin/recordFinder.cgi?action=find&name=AccessControlCard&condition.UserID={userid}"
        try:
            DEVICE_RAW_RESPONSE=requests.get(url, auth=HTTPDigestAuth(uname, pword))
            if True if re.search(f'UserID={userid}', DEVICE_RAW_RESPONSE.text) else False:
                response['flag'] = True
            else: response['message'].append(f'user({userid}) doesn\'t exist in this device({ip})!')
        except: response['message'].append(f'might be device({ip}) is switched off!')
        return response
    
    #############
    def deleteusrallimg(self, ip, userid, uname, pword):
        response = {'flag': False, 'message': []}
        url = f'http://{ip}/cgi-bin/FaceInfoManager.cgi?action=remove&UserID={userid}'
        try:
            requests.get(url,auth=HTTPDigestAuth(uname, pword))
            response['flag'] = True
        except: response['message'].append(f'might be device({ip}) is switched off!')
        return response
    
    #############
    def insertusrwithoutimg(self, ip, name, cardno, userid, password, reg_date,  valid_date, uname, pword):
        response = {'flag': False, 'message': []}
        url = f'http://{ip}/cgi-bin/recordUpdater.cgi?action=insert&name=AccessControlCard&CardName={name}&CardNo={cardno}&UserID={userid}&CardStatus=0&CardType=0&Password={password}&Doors[{0}]=0&VTOPosition=01018001&ValidDateStart={reg_date}%20093811&ValidDateEnd={valid_date}%20093811'
        try:
            DEVICE_RAW_RESPONSE = requests.get(url, auth=HTTPDigestAuth(uname, pword))
            if DEVICE_RAW_RESPONSE.status_code == 200: response['flag'] = True
            else: response['message'].append(f'couldn\'t create user({name}) to device({ip})!')
        except: response['message'].append(f'might be device({ip}) is switched off!')
        return response
    
    # def getimagepath(self, img_path):
    #     base_path = str(Path(settings.MEDIA_ROOT)).replace('\\','/')
    #     img_path = img_path.replace('/media','')
    #     return base_path+img_path
    
    def getLogsValue(self, device, starttime, endtime, count):
        response = { 'flag': False, 'message': 'Couldn\'t get logs!(getLogsValue)', 'data': [] }
        url = f"http://{device.deviceip}/cgi-bin/recordFinder.cgi?action=find&name=AccessControlCardRec&StartTime={starttime}&EndTime={endtime}&count={count}"
        
        try:
            DEVICE_RAW_RESPONSE=requests.get(url,auth=HTTPDigestAuth(device.username, device.password))
            records = []
            lines = [line for line in DEVICE_RAW_RESPONSE.text.split('\n') if line.strip()]

            current_index = None
            current_record = {}

            for line in lines:
                match = re.match(r'records\[(\d+)\]\.(.*?)=(.*)', line)
                if match:
                    index = int(match.group(1))
                    field_name = match.group(2)
                    value = match.group(3)

                    if index != current_index:
                        if current_record: records.append(current_record)
                        current_index = index
                        current_record = {}
                    current_record[field_name] = value

            if current_record: records.append(current_record)
                
            for record in records:
                modifiedrecord = {}
                for key in record.keys():
                    if '\r' in record[key]: modifiedrecord.update({key: record[key].split('\r')[0]})
                response['data'].append(modifiedrecord)
            response['flag'] = True
            response['message'] = 'logs found'
        except: response['message'].append(f'might be device({device.deviceip}) is switched off!')
        
        return response