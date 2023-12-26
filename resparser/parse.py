import requests
import json 
from django.conf import settings

AFFINDA_API_KEY=settings.AFFINDA_API_KEY
AFFINDA_URL=settings.AFFINDA_URL
AFFINDA_WORKSPACE=settings.AFFINDA_WORKSPACE


def extract_data(file):
    # files = { "file": (f'media/documents/{file}', open(f'media/documents/{file}', "rb"), "application/pdf") }
    # payload = {
    #     "wait": "true",
    #     "workspace": AFFINDA_WORKSPACE
    # }
    # headers = {
    #     "accept": "application/json",
    #     "authorization": "Bearer "+str(AFFINDA_API_KEY)
    # }

    # response = requests.post(AFFINDA_URL, data=payload, files=files, headers=headers)
    # print(response.text)
    # if response.status_code==200:
    #     data=json.loads(response.text)['data']
    #     print(data)
    # else:
    #     print(f"Error: {response.status_code} - {response.text}")

    with open("test_data/Resumes-CRORxbcW.json") as json_file:
        data = json.load(json_file)
        data=data['data']
        print(data)

    return data
