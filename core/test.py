import json 
with open('response.json','r') as respose:
    data=json.load(respose)
    key=data['data'].keys()
    data1=data['data']
    # print(data1['certifications'])

    for indices,extracted_data in enumerate(data1):
        print(extracted_data)
        # if extracted_data=='certifications':
        #     print(extracted_data)
        # for x in extracted_data:
        #     print(x)