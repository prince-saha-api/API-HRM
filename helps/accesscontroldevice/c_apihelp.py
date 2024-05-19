from requests.auth import HTTPDigestAuth
import requests

from helps.accesscontroldevice.d_apihelp import Apihelpsd

class Apihelpsc(Apihelpsd):
    
    def deleteusr(self, deviceip, employee_id, deviceusername, devicepassword):
        response = { 'flag': False, 'message': 'couldn\'t delete user!(deleteusr)' }
        record_response = self.get_record_number(deviceip, employee_id, deviceusername, devicepassword)
        if record_response['flag']:
            record_number=int(record_response['data'])
            url=f"http://{deviceip}/cgi-bin/recordUpdater.cgi?action=remove&name=AccessControlCard&recno={record_number}"
            try:
                requests_response = requests.get(url,auth=HTTPDigestAuth(deviceusername, devicepassword))
                if requests_response.status_code>=200 and requests_response.status_code<299:
                    response['flag'] = True
                    response['message'] = 'user deleted!'
            except: pass
        else: response['message'] = record_response['message']
            
        return response