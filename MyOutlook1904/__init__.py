import logging

import azure.functions as func
import requests
import json
import datetime
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('code')
    code = name
    #code = 'OAQABAAIAAACQN9QBRU3jT6bcBQLZNUj7qBV60oAQ9oGUYN5qdk1T4wvhAiXI_R40VOiyTVj4u62LeuFp_lH3rx340j5piourAzMT_JpqQu022sRIxDt5w1XP54aaLXk8dBLquhwRtxg9VgAUL0FHX9t5h06EDHTfh9VoCtVtWxsjymanRJwb1h_TvTtTejFFROnTDl3w03xMIu5twHem9txAyUnrDz6jRwTKLPjAYLJkDFmxbkSsPp77VemcM7sm5xTNaORj52_14i6RLPbKZlIcVtPYPVSR-hmHGvq3QgeIPsJUo5qLaZL4vfvjmSk_XBAkyxyPfuOUCp4N7ud-4bc7-y7oa-syJ4JUBOWBjqoXTggcdu4r0byx8fy-SsaH_FGoO7ydMJLb0yg-4ZfS6J-AYfskMXKdLLqj62w4DFRYW3kkWZWmgy5U3nYsoOqnMK46Bw4-WGv2yg361yONaZCYBJ7ocdl9_xFZHyiyyanyUbRol8WnEKv9UYuCHnSPapc0QfvncxmJyloVkXrJ_VekZYX3lH_Zk5RhFh4IBqqFRsTGWF6NWrQoYCSfqoPm49b3SLYh1b19pC36SnfwABb3HOl_WGc5ZQQHl8g0ZHyic-joopmfCGsgTQIKKQivy2y6WN9GjVNCggXHLvGtgYdoOMzAdNjJZOYEqXHJSV6PIHpFOMe9ALdvF0GbU3zIoGicxfjAQqycI-F-ZiVMtnB5KiTggaOlgZs5IBxswJ-FKa1fyARxA8oSW57wtCoDRJjIxT6hPBkgAA'
    x_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'content-Type': 'application/x-www-form-urlencoded',
       }
    data_auth = {'grant_type':'authorization_code','client_id':'fa2924d5-8237-48f1-82ae-d9256243adef','code':code,'redirect_uri':'https://13.127.109.20/flask/token','client_secret':
'/KFT/KgBc752JPLFx6_B=lYOfzOvzaB2',}
    #name = req.params.get('name')
    email = req.params.get('email')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        r = requests.post(x_url,headers=header,data=data_auth)
        data_auth = json.loads(r.text)
        auth_token = data_auth['access_token']
        refresh_token = data_auth['id_token']
        #token = auth_token}
        calender = getCal(auth_token)
        return func.HttpResponse(calender)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

def getCal(auth_token):
    cal = 'https://graph.microsoft.com/v1.0/me/calendar/getSchedule'
    cal_header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Prefer': 'outlook.timezone="Pacific Standard Time"',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+auth_token,

        }
    cal_data = {  
    "schedules":[email],
    'startTime': {
        'dateTime': '2019-10-08T22:00:00',
        'timeZone': 'Pacific Standard Time',
    },
    'endTime': {
        'dateTime': '2019-10-09T06:00:00',
        'timeZone': 'Pacific Standard Time',
    },
    'availabilityViewInterval': 60
    
        } 
    c_data = json.dumps(cal_data) 
    r = requests.post(cal,headers=cal_header,data=c_data)
    if r.status_code != 200:
        return auth_code
    data_json = json.loads(r.text)
    values = data_json['value']
    email = values[0]['scheduleId']
    items = values[0]['scheduleItems']
    cal_data = {}
    cal_data['email'] = email
    values = []
    for item in items:
        value = {}
        value["status"] = item['status']
        value["subject"] = item['subject'].replace('"','')
        value["start_data"] = item['start']['dateTime']
        date_s = item['start']['dateTime']
        date_x = datetime.datetime.strptime(date_s.split('.')[0],'%Y-%m-%dT%H:%M:%S')
        start_day = date_x.strftime('%A')
        value["start_day"] = start_day
    
        value["end_date"] = item['end']['dateTime']
        date_e = item['end']['dateTime']
        date_y = datetime.datetime.strptime(date_e.split('.')[0],'%Y-%m-%dT%H:%M:%S')
        end_day = date_y.strftime('%A')
        value["end_day"] = end_day
    
        diff = (date_y-date_x).seconds/3600
        value["hrs"] = str(diff)
        values.append(value)
    cal_data["values"]=values
    cal_json = json.dumps(cal_data)
    return cal_json
