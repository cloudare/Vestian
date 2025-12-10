import requests
import views.logWriter as lw
import config as sd

def ey_header_auth():
    header = {
        # "Accept" : "application/json",
        # "Content-Type" : "application/x-www-form-urlencoded",
        "username": sd.userName,
        "password": sd.password,
        "apiaccesskey": sd.apiaccesskey
    }
    return header

def ey_header_refresh():
    header = {
        "refreshToken" : sd.refresh_token_ey,
        "Content-Type" : "application/x-www-form-urlencoded",
        "apiaccesskey" : sd.apiaccesskey
        # "REQUEST_TYPE" : "ENC",
        # "applicationName" : "invoicemanager"
    }
    return header

def ey_header(auth):
    header = {
        "accessToken" : auth,
        # "Content-Type" : "application/x-www-form-urlencoded",
        "apiaccesskey" : sd.apiaccesskey
        # "REQUEST_TYPE" : "ENC",
        # "applicationName" : "invoicemanager"
    }
    return header

def getToken():
    try:
        lw.logBackUpRecord("Calling getToken API.")
        url = sd.ey_auth_url
        header = ey_header_auth()
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        # lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header)#, json=body, data=payload)
        print(response.json())
        # print(str(response.json().get("authenticated")))
        if str(response.json().get("status")) == 1 or str(response.json().get("status")) == '1':
            authorization = response.json().get("accessToken")
            refreshToken = response.json().get("refreshToken")
            lw.logBackUpRecord("Authorization Token is : " + str(authorization) + " and refreshtoken is: "+ str(refreshToken))
            return authorization,refreshToken
        else:
            lw.logRecord("Error in getToken: " + (response.json())['messages']['details'])
            return '',''
        
    except Exception as e:
        lw.logRecord("Error in getToken: " + str(e))

def purchase(body):
    try:
        auth, reftoken = getToken()
        lw.logBackUpRecord("Calling bulkInvoice API to send data to EY Portal.")
        url = sd.ey_purchase_url
        header = ey_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif response.status_code == 400:
            lw.logBackUpRecord("Bulk Invoice Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Invoice Data has been uploaded Successfully.")
        return response.json()
    except Exception as e:
        lw.logRecord("Error in bulkInvoice: " + str(e))

def sales(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling creditDebitNote API.")
        url = sd.ey_sales_url + "/creditDebitNote"
        header = ey_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif response.status_code == 400:
            lw.logBackUpRecord("credit /Debit Note Data has been uploaded with error.")
        else:    
            lw.logBackUpRecord("credit /Debit Note Data has been uploaded Successfully.")
        return response
    except Exception as e:
        lw.logRecord("Error in creditDebitNote: " + str(e))

def payments(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling payments  API.")
        url = sd.ey_api_url + "/payments"
        header = ey_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif response.status_code == 400:
            lw.logBackUpRecord("Payments Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Payments Data has been uploaded Successfully.")
        # print(response.json())
        return response
    except Exception as e:
        lw.logRecord("Error in payments : " + str(e))

def postingCreditDebitNote(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling postingCreditDebitNote  API.")
        url = sd.ey_api_url + "/postingCreditDebitNote"
        header = ey_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif response.status_code == 200:
            lw.logBackUpRecord("Credit/Debit Note has been posted Successfully.")
        else:
            lw.logBackUpRecord("Credit/Debit Note has been posted with error: " + str())
        # lw.logBackUpRecord("Credit/Debit Note has been posted Successfully.")
        return response.json()
    
    except Exception as e:
        lw.logRecord("Error in postingCreditDebitNote : " + str(e))

def postingAck(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling postingAck  API.")
        url = sd.ey_api_url + "/postingAck"
        header = ey_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)
        # print(response)
        # print(response.json())
        if response.status_code == 500 or response.status_code == 401: # or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif str((response.json())[0]['status']) == "Success":
            lw.logBackUpRecord("Acknowledgement from ERP System has been posted Successfully.")
        else:
            lw.logBackUpRecord("Acknowledgement from ERP System has been posted with error: " + str())
        
        return response.json()
    
    except Exception as e:
        lw.logRecord("Error in postingAck : " + str(e))

def uploadLocationMaster(body):
    try:
        auth = getToken()
        lw.logBackUpRecord("Calling uploadLocationMaster  API.")
        url = sd.ey_api_url + "/uploadLocationMaster"
        header = ey_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)

        if response.status_code == 500 or response.status_code == 401:# or response.status_code == 400:
            auth = getToken()
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
        elif str((response.json())[0]['status']) == "Success":
            lw.logBackUpRecord("Location Master has been uploaded Successfully.")
        else:
            lw.logBackUpRecord("Location Master has been uploaded with error: " + str())
    
    except Exception as e:
        lw.logRecord("Error in uploadLocationMaster : " + str(e))
