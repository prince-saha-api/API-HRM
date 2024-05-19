from requests.auth import HTTPDigestAuth
from datetime import datetime, timedelta
from django.utils import timezone
import requests
import pytz
import re

from helps.accesscontroldevice.e_rawhelp import Rawhelpse

class Apihelpsd(Rawhelpse):
    
    def get_record_number(self, deviceip, employee_id, deviceusername, devicepassword):
        response = { 'flag': False, 'message': 'couldn\'t retrieve record number!(get_record_number)' }
        url=f"http://{deviceip}/cgi-bin/recordFinder.cgi?action=find&name=AccessControlCard&condition.UserID={employee_id}&count={8000}"
        
        try:
            requests_response = requests.get(url, auth=HTTPDigestAuth(deviceusername, devicepassword))
            records = []
            lines = requests_response.text.split('\n')
            lines = [line for line in lines if line.strip()]
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
            response.update({'data': records[0]['RecNo']})
        except: pass
        return response
    
    def existanceofuser(self, deviceip, employee_id, deviceusername, devicepassword):
        response = { 'flag': False, 'message': 'doesn\'t exist this user!(existanceofuser)' }

        url=f'http://{deviceip}/cgi-bin/recordFinder.cgi?action=find&name=AccessControlCard&condition.UserID={employee_id}&count={8000}'
        try:
            requests_response=requests.get(url, auth=HTTPDigestAuth(deviceusername, devicepassword))
            r=requests_response.text
            r=r.replace('found=','')
            response['flag'] = True if re.search('found=0', requests_response.text) == None else False
            response['flag'] = 'user exist'
        except: pass
        return response
    
    def insertusrwithoutimg(self, deviceip, username, cardno, employee_id, password, reg_date,  valid_date, deviceusername, devicepassword):
        response = { 'flag': False, 'message': 'couldn\'t add!(insertusrwithoutimg)' }
        url = f'http://{deviceip}/cgi-bin/recordUpdater.cgi?action=insert&name=AccessControlCard&CardName={username}&CardNo={cardno}&UserID={employee_id}&CardStatus=0&CardType=0&Password={password}&Doors[{0}]=0&VTOPosition=01018001&ValidDateStart={reg_date}%20093811&ValidDateEnd={valid_date}%20093811'
        try:
            requests_response = requests.get(url, auth=HTTPDigestAuth(deviceusername, devicepassword))
            if requests_response.status_code>=200 and requests_response.status_code<299:
                response['flag'] = True
                response['message'] = 'successfully added!'
        except: pass
        return response
    
    def addphototouser(self, image_paths, deviceip, employee_id, username, deviceusername, devicepassword, employeeserializer=None):
        response = { 'flag': False, 'message': 'couldn\'t add photo to user!(addphototouser)', 'failed': [] }

        if employeeserializer != None:
            image_paths = [self.getimagepath(employeeserializer['image'])]
            employee_id = employeeserializer['employee_id']
            username = employeeserializer['username']
        
        getPhotoData_response = self.getPhotoData(image_paths)
        response['failed'] = getPhotoData_response['failed']

        if getPhotoData_response['flag']:
            url=f"http://{deviceip}/cgi-bin/FaceInfoManager.cgi?action=add"
            data={
                'UserID': str(employee_id),
                'Info': { 'UserName': username, 'PhotoData': getPhotoData_response['success'] }
            }
            try:
                requests_response = requests.post(url, json=data, auth=HTTPDigestAuth(deviceusername, devicepassword), headers={"Content-Type":"application/json"})
                if requests_response.status_code>=200 and requests_response.status_code<=299:
                    response['flag'] = True
                    response['message'] = 'all the photos have been added to user'
                    if response['failed']: response['message'] = 'some of photo have been added to user'
            except: pass
        return response
    
    def deleteusrallimg(self, deviceip, employee_id, deviceusername, devicepassword):
        response = { 'flag': False, 'message': 'Couldn\'t delete!(deleteusrallimg)' }
        url = f'http://{deviceip}/cgi-bin/FaceInfoManager.cgi?action=remove&UserID={employee_id}'
        try:
            requests_response = requests.get(url, auth=HTTPDigestAuth(deviceusername, devicepassword))
            if requests_response.status_code>=200 and requests_response.status_code<299:
                response['flag'] = True
                response['message'] = 'Successfully Deleted!'
        except: pass
        return response
    

    def getLogsValue(self, device, starttime, endtime, count):
        response = { 'flag': False, 'message': 'Couldn\'t get logs!(getLogsValue)', 'data': [] }
        url = f"http://{device.deviceip}/cgi-bin/recordFinder.cgi?action=find&name=AccessControlCardRec&StartTime={starttime}&EndTime={endtime}&count={count}"
        
        try:
            requests_response=requests.get(url,auth=HTTPDigestAuth(device.username, device.password))
            records = []
            lines = [line for line in requests_response.text.split('\n') if line.strip()]

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
        except: pass
        
        return response