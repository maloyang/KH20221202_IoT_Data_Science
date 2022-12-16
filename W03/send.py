import requests

def line_send_image2(message, img_url, token = 'rpHUQIIMkArQh6EtQpqfjK6hjPN2jjNxh0zDbcFVoD2'):
    url = "https://notify-api.line.me/api/notify"  # --> 不支援http, 只能用https
    headers = {"Authorization" : "Bearer "+ token}

    payload = {"message" :  message}

    r = requests.get(img_url)
    files = {'imageFile': r.content}

    r = requests.post(url, headers = headers, params = payload, files = files)

line_send_image2('test', 'https://github.com/maloyang/KH20210925_Python_Data_Science/blob/main/W02/dog.png?raw=true')
