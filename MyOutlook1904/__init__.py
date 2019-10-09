import logging

import azure.functions as func
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    code = 'OAQABAAIAAACQN9QBRU3jT6bcBQLZNUj7KlKC6x8f2XJvnUuRaVO3BD2FzE5hcrc3ohUqiaS8r-foygGatO1qwXsaNGmD-FT1jCy9LPV09i9UwKHdqfRrQmC_86J4uSL-Jj8v-r2XagEXukR_olVOsJLUkeGB-6uzsnW5eG2pivYsKKF1kFhB4T8WYJ9UWgbj0aY6I-kcDSM-jIZEQ3XfHVBIkJsRBKkfKwAZ6ac-PIvPl7XWRDRDD8r8ZGsmzLvVfPsamRe7VDazzl2AMcSyBlw_UFTNLPdtxDD1doFIL_bTpUDENbItfz47ZFLSOdhR7VQnnUtNvPqZA8jkzueKoRD3WEZ6y7Oehu3azExWeg4q9fMcqEN8Lnhxv_v1ZE9XgooPrSwGjIipWFi2WkTd6KNZdWdjPKsqxbdoFLCX9SiSkWfALe8UUOwBUSjg3068jTegEUQmPn7VBlc1wACVPDK7VQHjM_o0PoJYWMd_nGd8WVOtxxDR7LgZIyC2KAY5_UwPDLhZlLNBeupk7YY98bdVky9tEsI2afjVHZlmMmH9B2iu0swDdKc1JZ_4Uor0hkHXpzuevH3FlU1zsEoB5oT677rUOzE8nzd4b_U5C0XYuLoWJecYDvI6mmRrK7zWuFW4A7OoJP7Q-5h4LAi9q8kzFqkULG3DiMYtjng-8HeLHrylzEPlpo7fzqEnwJlTL5LB7NTutB-V7kyYn1RGKQ6fWLWzfVZcWCC21gzR1uANt4zBPFvrIS75iMOV8Y-QSM9LK6-LCiwgAA'

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
	x_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
	data_auth = {
                        'grant_type':'authorization_code',
                        'client_id':'fa2924d5-8237-48f1-82ae-d9256243adef',
                        'code':code,
                        'redirect_uri':'http://localhost:8080/token',
                        'client_secret':'/KFT/KgBc752JPLFx6_B=lYOfzOvzaB2',
                        }
	header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'content-Type': 'application/x-www-form-urlencoded',                 
        }
	r = requests.post(x_url,headers=header,data=data_auth)

        return func.HttpResponse(r.text)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
