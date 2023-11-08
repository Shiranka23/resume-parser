import requests
import json 
url = "https://api.affinda.com/v3/documents"
from django.conf import settings

AFFINDA_API_KEY=settings.AFFINDA_API_KEY
AFFINDA_URL=settings.AFFINDA_URL
AFFINDA_WORKSPACE=settings.AFFINDA_WORKSPACE


def extract_data(file):
    files = { "file": (f'media/documents/{file}', open(f'media/documents/{file}', "rb"), "application/pdf") }
    payload = {
        "wait": "true",
        "workspace": AFFINDA_WORKSPACE
    }
    headers = {
        "accept": "application/json",
        "authorization": "Bearer "+str(AFFINDA_API_KEY)
    }

    response = requests.post(url, data=payload, files=files, headers=headers)
    data=json.loads(response.text)['data']
    # print(response.text)

    # with open("response.json") as json_file:
    #     data = json.load(json_file)
    #     # print(data['data'])
    # data=data['data']

    return data
