import requests

class ImgurAPI():
    def __init__(self, client_id):
        self.client_id = client_id
        self.endpoit_upload_image = 'https://api.imgur.com/3/image'
    
    def upload_image_base64(self, img_base64):
        payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--' % (img_base64)
        headers = {
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
            'Authorization': 'Client-ID %s' % (self.client_id)
        }
        response = requests.request("POST", self.endpoit_upload_image, data=payload, headers=headers)
        response = response.json()
        if response['success'] == True:
            return {
                'link' : response['data']['link'],
                'error' : False
            }
        else:
            return {
                'error' : True
            }