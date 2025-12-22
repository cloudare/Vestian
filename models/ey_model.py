import requests
import views.logWriter as lw
import config as sd
import time
access_token = ''

def ey_header_auth():
    header = {
        "username": sd.userName,
        "password": sd.password,
        "apiaccesskey": sd.apiaccesskey
    }
    return header

def ey_header_status(auth, ack):
    header = {
        "accessToken" : auth,
        "X-EAckNo" : ack,
        "apiaccesskey" : sd.apiaccesskey
    }
    return header

def ey_header(auth):
    header = {
        "accessToken" : auth,
        "apiaccesskey" : sd.apiaccesskey
    }
    return header

def getToken():
    try:
        global access_token
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
            access_token = authorization
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
        # auth, reftoken = getToken()
        global access_token
        auth = access_token
        lw.logBackUpRecord("Calling purchase API to send data to EY Portal.")
        url = sd.ey_purchase_url
        header = ey_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)
        response = response.json()
        print(response)
        if response['status'] == 0:# or response.status_code == 400:
            auth, refreshToken = getToken()
            header = ey_header(auth)
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
            response = response.json()
            print(response)
        elif response['status'] == '0':
            lw.logBackUpRecord("Bulk Invoice Data has been uploaded with error.")
            return ""

        lw.logBackUpRecord("Bulk Invoice Data has been uploaded Successfully.")
        return response
    except Exception as e:
        lw.logRecord("Error in purchase: " + str(e))

def sales(body):
    try:
        # auth = getToken()
        global access_token
        auth = access_token
        lw.logBackUpRecord("Calling sales API.")
        url = sd.ey_sales_url
        header = ey_header(auth)
        lw.logBackUpRecord("URL:" + str(url))
        lw.logBackUpRecord("Header:" + str(header))
        lw.logBackUpRecord("Payload:" + str(body))
        response = requests.post(url, headers=header, json=body)#, data=payload)
        response = response.json()
        print(response)
        if response['status'] == 0:# or response.status_code == 400:
            auth, refreshToken = getToken()
            header = ey_header(auth)
            response = requests.post(url, headers=header, json=body)
            # auth = authorization
            lw.logBackUpRecord(auth)
            response = response.json()
            print(response)
        elif response['status'] == '0':
            lw.logBackUpRecord("credit /Debit Note Data has been uploaded with error.")
          
        lw.logBackUpRecord("credit /Debit Note Data has been uploaded Successfully.")
        return response
    except Exception as e:
        lw.logRecord("Error in sales: " + str(e))

def get_status(ack):
    try:
        # auth = getToken()
        while(1==1):
            global access_token
            auth = access_token
            lw.logBackUpRecord("Calling get_status API.")
            url = sd.ey_get_status
            header = ey_header_status(auth, ack)
            lw.logBackUpRecord("URL:" + str(url))
            lw.logBackUpRecord("Header:" + str(header))
            # lw.logBackUpRecord("Payload:" + str(body))
            response = requests.post(url, headers=header)#, data=payload)
            response = response.json()
            if response['status'] == 0:# or response.status_code == 400:
                auth, refreshToken = getToken()
                header = ey_header_status(auth, ack)
                response = requests.post(url, headers=header)
                # auth = authorization
                lw.logBackUpRecord(auth)
                response = response.json()
                print(response)
            # elif response.status_code == 400:
            #     lw.logBackUpRecord("credit /Debit Note Data has been uploaded with error.")
            if response['status'] == '1' and response['operationStatus'] == 'Processed':
                lw.logBackUpRecord("Data processed Successfully.")
                return response
            time.sleep(60)
    except Exception as e:
        lw.logRecord("Error in get_status: " + str(e))

def get_sales_data(ack):
    try:
        # auth = getToken()
        while(1==1):
            global access_token
            auth = access_token
            lw.logBackUpRecord("Calling get_sales_data API.")
            url = sd.ey_sales_ack
            header = ey_header_status(auth, ack)
            lw.logBackUpRecord("URL:" + str(url))
            lw.logBackUpRecord("Header:" + str(header))
            # lw.logBackUpRecord("Payload:" + str(body))
            response = requests.post(url, headers=header)#, data=payload)
            response = requests.post(url, headers=header)#, data=payload)
            response = response.json()
            print(response)
            try:
                if response['status'] == 0:# or response.status_code == 400:
                    auth, refreshToken = getToken()
                    header = ey_header_status(auth, ack)
                    response = requests.post(url, headers=header)
                    # auth = authorization
                    lw.logBackUpRecord(auth)
                    response = response.json()
                    print(response)
            except:
                pass
            # elif response.status_code == 400:
            #     lw.logBackUpRecord("credit /Debit Note Data has been uploaded with error.")
            # if response['status'] == '1':
                lw.logBackUpRecord("Data processed Successfully.")
                return response
            time.sleep(60)
    except Exception as e:
        lw.logRecord("Error in get_sales_data: " + str(e))

def get_purchase_data(ack):
    try:
        # auth = getToken()
        while(1==1):
            global access_token
            auth = access_token
            lw.logBackUpRecord("Calling get_purchase_data API.")
            url = sd.ey_purchase_ack
            header = ey_header_status(auth, ack)
            lw.logBackUpRecord("URL:" + str(url))
            lw.logBackUpRecord("Header:" + str(header))
            # lw.logBackUpRecord("Payload:" + str(body))
            response = requests.post(url, headers=header)#, data=payload)
            response = response.json()
            print(response)
            try:
                if response['status'] == 0:# or response.status_code == 400:
                    auth, refreshToken = getToken()
                    header = ey_header_status(auth, ack)
                    response = requests.post(url, headers=header)
                    # auth = authorization
                    lw.logBackUpRecord(auth)
                    response = response.json()
                    print(response)
            except:
                pass
            # elif response.status_code == 400:
            #     lw.logBackUpRecord("credit /Debit Note Data has been uploaded with error.")
            # if response['status'] == '1':
                lw.logBackUpRecord("Data processed Successfully.")
                return response
            time.sleep(60)
    except Exception as e:
        lw.logRecord("Error in get_purchase_data: " + str(e))
