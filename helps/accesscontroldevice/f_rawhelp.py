from django.conf import settings
from pythonping import ping
from pathlib import Path
from PIL import Image
import base64
import os

class Rawhelpsf:

    def getDeviceIpUsernamePassword(self, classOBJ, deviceid):
        response = { 'flag': False, 'data': {} }
        objects = classOBJ.objects.filter(device_id=deviceid)
        if objects.exists():
            object = objects.values("device_ip", "device_id", "device_name", "username", "password", "is_active").first()
            response['flag'] = True
            response['data'].update({'deviceid': object.get('device_id', '')})
            response['data'].update({'devicename': object.get('device_id', '')})
            response['data'].update({'deviceip': object.get('device_ip', '0.0.0.0')})
            response['data'].update({'deviceusername': object.get('username', 'admin')})
            response['data'].update({'devicepassword': object.get('password', 'admin1234')})
            response['data'].update({'deviceactivity': object.get('is_active', False)})

        return response

    def is_device_active(self, ipaddress):
        try: return ping(ipaddress, count=2).success()
        except Exception as e: return False
    
    def getimagepath(self, img_path):
        base_path = str(Path(settings.MEDIA_ROOT)).replace('\\','/')
        img_path = img_path.replace('/media','')
        return base_path+img_path
    
    def resize_image(self, input_path, output_path, max_size_kb):
        response = { 'flag': False, 'message': 'couldn\'n resize image' }
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
                response['flag'] = True
                response['message'] = 'successfully resized image'
        except MemoryError as e: pass

        return response
    
    def convertImgTobase64(self, image):
        response = { 'flag': False, 'message': 'couldn\'t convert image to base64!'}
        try:
            img=image.read()
            base64_img=base64.b64encode(img)
            response['flag'] = True
            response['message'] = 'successfully converted to base64 image'
            response.update({'data': base64_img.decode("utf-8")})
        except: pass
        return response