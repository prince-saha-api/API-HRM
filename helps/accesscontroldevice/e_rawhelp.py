from helps.accesscontroldevice.f_rawhelp import Rawhelpsf

class Rawhelpse(Rawhelpsf):
    
    def getPhotoData(self, image_paths):
        response = { 'flag': False, 'message': 'couldn\'t get Photo Data!', 'success': [], 'failed': [] }
        for image_path in image_paths:
            resizeimage_response = self.resize_image(image_path, image_path, 80)
            if resizeimage_response['flag']:
                with open(image_path,"rb") as image:
                    convertImgTobase_response = self.convertImgTobase64(image)
                    if convertImgTobase_response['flag']:
                        response['flag'] = True
                        response['message'] = 'successfully converted to base64 image'
                        response['success'].append(convertImgTobase_response['data'])
                    else: response['failed'].append({'path': image_path, 'reason': 'couldn\'t convert base64!'})
            else: response['failed'].append({'path': image_path, 'reason': 'couldn\'t resize image!'})
        return response