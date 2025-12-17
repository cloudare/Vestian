import requests
import config as sd
from datetime import datetime, timedelta
import views.logWriter as lw
import pytz
import json

class ZohoModel:
    access_token = sd.access_token
    @staticmethod
    def get_access_token():
        try:
            lw.logBackUpRecord("Calling API to get the refresh token.")
            """Fetch new access token using refresh token"""
            url = sd.zoho_refresh_token + "refresh_token=" + str(sd.refresh_token) + "&client_id=" + str(sd.client_id) + "&client_secret=" + str(sd.client_secret)+ "&grant_type=refresh_token"
            header = {"Authorization": f"Bearer {sd.access_token}"}
            lw.logBackUpRecord("URL:" + str(url))
            lw.logBackUpRecord("Header:" + str(header))
            response = requests.post(url, headers=header, verify=False)#, data=payload)
            return response.json().get("access_token")
        except Exception as e:
            lw.logRecord("Error in get access token: " + str(e))

    # @staticmethod
    # def fetch_contacts(page):
    #     """Fetch contacts from Zoho CRM"""
    #     try:
    #         # page = 1
    #         # access_token = ZohoModel.get_access_token()
    #         tz = pytz.timezone("Asia/Kolkata")
    #         time = (datetime.now(tz)- timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S%z")
    #         time = time.replace("+", "%2B")
    #         # print(time)
    #         header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #         lw.logBackUpRecord("Calling API for Contact List for 25 records at a time.")
    #         lw.logBackUpRecord("URL:" + str(f"{sd.zoho_contact}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor")) #&last_modified_time={time}
    #         lw.logBackUpRecord("Header:" + str(header))
    #         response = requests.get(f"{sd.zoho_contact}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor", headers=header) #&last_modified_time={time}
    #         # print(response.json())
    #         if response.status_code == 401:
    #             ZohoModel.access_token = ZohoModel.get_access_token()
    #             header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #             response = requests.get(f"{sd.zoho_contact}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor", headers=header) #&last_modified_time={time}
    #             lw.logBackUpRecord(ZohoModel.access_token)
    #         print(response.json())
    #         lw.logBackUpRecord("Contact List Data:" + str(response.json()))
    #         return response.json()
    #     except Exception as e:
    #         lw.logRecord("Error in fetch_contacts: " + str(e))
    
    # @staticmethod
    # def fetch_contacts_details(id):
    #     """Fetch Contacts Details from Zoho CRM"""
    #     try:
    #         # access_token = ZohoModel.get_access_token()
    #         lw.logBackUpRecord("Calling API for Contact deatils.")
    #         lw.logBackUpRecord("URL:" + str(f"{sd.zoho_contact}/{id}?organization_id={sd.organization_id}"))
    #         header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #         lw.logBackUpRecord("Header:" + str(header))
            
    #         response = requests.get(f"{sd.zoho_contact}/{id}?organization_id={sd.organization_id}", headers=header)
    #         if response.status_code == 401:
    #             ZohoModel.access_token = ZohoModel.get_access_token()
    #             header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #             response = requests.get(f"{sd.zoho_contact}/{id}?organization_id={sd.organization_id}", headers=header)
    #             lw.logBackUpRecord(ZohoModel.access_token)
    #         print(response.json())
    #         # lw.logBackUpRecord("Contact Details Data:" + str(response.json()))
    #         return response.json()
    #     except Exception as e:
    #         lw.logRecord("Error in fetch_contacts_details: " + str(e))

    @staticmethod
    def fetch_bills(page):
        """Fetch Bill from Zoho CRM"""
        try:
            # page = 1
            # access_token = ZohoModel.get_access_token()
            tz = pytz.timezone("Asia/Kolkata")
            time = (datetime.now(tz)- timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S%z")
            time = time.replace("+", "%2B")
            # print(time)
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Calling API for Bill List for 200 records at a time.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_bills}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor")) #&last_modified_time={time}
            lw.logBackUpRecord("Header:" + str(header))
            response = requests.get(f"{sd.zoho_bills}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor", headers=header, verify=False) #&last_modified_time={time}
            # print(response.json())
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_bills}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor", headers=header, verify=False) #&last_modified_time={time}
                lw.logBackUpRecord(ZohoModel.access_token)
            # print(response.json())
            # lw.logBackUpRecord("Bill List Data:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_bills: " + str(e))


    @staticmethod
    def fetch_bill_details(id):
        """Fetch Bill Details from Zoho CRM"""
        try:
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for Bill deatils.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_bills}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            
            response = requests.get(f"{sd.zoho_bills}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_bills}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            print(response.json())
            
            # lw.logBackUpRecord("Bill Details Data:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_bill_details: " + str(e))

    @staticmethod
    def fetch_expense(page):
        """Fetch Expense from Zoho CRM"""
        try:
            # page = 1
            # access_token = ZohoModel.get_access_token()
            tz = pytz.timezone("Asia/Kolkata")
            time = (datetime.now(tz)- timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S%z")
            time = time.replace("+", "%2B")
            # print(time)
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Calling API for Expense List for 200 records at a time.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_expense}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor")) #&last_modified_time={time}
            lw.logBackUpRecord("Header:" + str(header))
            response = requests.get(f"{sd.zoho_expense}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor", headers=header, verify=False) #&last_modified_time={time}
            # print(response.json())
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_expense}?organization_id={sd.organization_id}&page={page}&per_page=200&contact_type=vendor", headers=header, verify=False) #&last_modified_time={time}
                lw.logBackUpRecord(ZohoModel.access_token)
            print(response.json())
            # lw.logBackUpRecord("Expense List Data:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_Expense: " + str(e))


    @staticmethod
    def fetch_expense_details(id):
        """Fetch Bill Details from Zoho CRM"""
        try:
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for Expense deatils.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_expense}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            
            response = requests.get(f"{sd.zoho_expense}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_expense}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            # print(response.json())
            
            # lw.logBackUpRecord("Expense Details Data:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_Expense_details: " + str(e))

    @staticmethod
    def fetch_dn(page):
        """Fetch DN from Zoho CRM"""
        try:
            # page = 1
            # access_token = ZohoModel.get_access_token()
            tz = pytz.timezone("Asia/Kolkata")
            time = (datetime.now(tz)- timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S%z")
            time = time.replace("+", "%2B")
            # print(time)
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Calling API for DN List for 200 records at a time.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_dn}?organization_id={sd.organization_id}&page={page}&per_page=200")) #&last_modified_time={time}
            lw.logBackUpRecord("Header:" + str(header))
            response = requests.get(f"{sd.zoho_dn}?organization_id={sd.organization_id}&page={page}&per_page=200", headers=header, verify=False) #&last_modified_time={time}
            print(response.json())
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_dn}?organization_id={sd.organization_id}&page={page}&per_page=200", headers=header, verify=False) #&last_modified_time={time}
                lw.logBackUpRecord(ZohoModel.access_token)
            print(response.json())
            lw.logBackUpRecord("DN List Data:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_dn: " + str(e))


    @staticmethod
    def fetch_dn_details(id):
        """Fetch DN Details from Zoho CRM"""
        try:
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for DN deatils.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_dn}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            
            response = requests.get(f"{sd.zoho_dn}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_dn}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            # lw.logBackUpRecord("DN Details Data:" + str(response.json()))
            print(response.json())
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_dn_details: " + str(e))

    @staticmethod
    def fetch_invoice(page):
        """Fetch Invoice from Zoho CRM"""
        try:
            # page = 1
            # access_token = ZohoModel.get_access_token()
            tz = pytz.timezone("Asia/Kolkata")
            time = (datetime.now(tz)- timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S%z")
            time = time.replace("+", "%2B")
            # print(time)
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Calling API for Invoice List for 200 records at a time.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_invoice}?organization_id={sd.organization_id}&page={page}&per_page=200")) #&last_modified_time={time}
            lw.logBackUpRecord("Header:" + str(header))
            response = requests.get(f"{sd.zoho_invoice}?organization_id={sd.organization_id}&page={page}&per_page=200", headers=header, verify=False) #&last_modified_time={time}
            print(response.json())
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_invoice}?organization_id={sd.organization_id}&page={page}&per_page=200", headers=header, verify=False) #&last_modified_time={time}
                lw.logBackUpRecord(ZohoModel.access_token)
            # print(response.json())
            # lw.logBackUpRecord("Invoice List Data:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_Invoice: " + str(e))


    @staticmethod
    def fetch_invoice_details(id):
        """Fetch Invoice Details from Zoho CRM"""
        try:
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for Invoice deatils.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_invoice}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            
            response = requests.get(f"{sd.zoho_invoice}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_invoice}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            # lw.logBackUpRecord("Invoice Details Data:" + str(response.json()))
            print(str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_Invoice_details: " + str(e))

    @staticmethod
    def fetch_cn(page):
        """Fetch CN from Zoho CRM"""
        try:
            # page = 1
            # access_token = ZohoModel.get_access_token()
            tz = pytz.timezone("Asia/Kolkata")
            time = (datetime.now(tz)- timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S%z")
            time = time.replace("+", "%2B")
            # print(time)
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Calling API for CN List for 200 records at a time.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_cn}?organization_id={sd.organization_id}&page={page}&per_page=200")) #&last_modified_time={time}
            lw.logBackUpRecord("Header:" + str(header))
            response = requests.get(f"{sd.zoho_cn}?organization_id={sd.organization_id}&page={page}&per_page=200", headers=header, verify=False) #&last_modified_time={time}
            # print(response.json())
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_cn}?organization_id={sd.organization_id}&page={page}&per_page=200", headers=header, verify=False) #&last_modified_time={time}
                lw.logBackUpRecord(ZohoModel.access_token)
            # print(response.json())
            lw.logBackUpRecord("CN List Data:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_cn: " + str(e))


    @staticmethod
    def fetch_cn_details(id):
        """Fetch CN Details from Zoho CRM"""
        try:
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for CN deatils.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_cn}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            
            response = requests.get(f"{sd.zoho_cn}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.get(f"{sd.zoho_cn}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            # print(response.json())
            lw.logBackUpRecord("CN Details Data:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in fetch_cn_details: " + str(e))

    # @staticmethod
    # def fetch_payments(page):
    #     """Fetch Payments from Zoho CRM"""
    #     try:
    #         # page = 1
    #         # access_token = ZohoModel.get_access_token()
    #         tz = pytz.timezone("Asia/Kolkata")
    #         time = (datetime.now(tz)- timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S%z")
    #         time = time.replace("+", "%2B")
    #         # print(time)
    #         header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #         lw.logBackUpRecord("Calling API for Payments List for 25 records at a time.")
    #         lw.logBackUpRecord("URL:" + str(f"{sd.zoho_payments}?organization_id={sd.organization_id}&page={page}&per_page=200")) #&last_modified_time={time}
    #         lw.logBackUpRecord("Header:" + str(header))
    #         response = requests.get(f"{sd.zoho_payments}?organization_id={sd.organization_id}&page={page}&per_page=200", headers=header) #&last_modified_time={time}
    #         # print(response.json())
    #         if response.status_code == 401:
    #             ZohoModel.access_token = ZohoModel.get_access_token()
    #             header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #             response = requests.get(f"{sd.zoho_payments}?organization_id={sd.organization_id}&page={page}&per_page=200", headers=header) #&last_modified_time={time}
    #             lw.logBackUpRecord(ZohoModel.access_token)
    #         # print(response.json())
    #         lw.logBackUpRecord("Payment List Data:" + str(response.json()))
    #         return response.json()
    #     except Exception as e:
    #         lw.logRecord("Error in fetch_payments: " + str(e))

    # @staticmethod
    # def fetch_payments_details(id):
    #     """Fetch Payment Details from Zoho CRM"""
    #     try:
    #         # access_token = ZohoModel.get_access_token()
    #         lw.logBackUpRecord("Calling API for Payment deatils.")
    #         lw.logBackUpRecord("URL:" + str(f"{sd.zoho_payments}/{id}?organization_id={sd.organization_id}"))
    #         header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #         lw.logBackUpRecord("Header:" + str(header))
            
    #         response = requests.get(f"{sd.zoho_payments}/{id}?organization_id={sd.organization_id}", headers=header)
    #         if response.status_code == 401:
    #             ZohoModel.access_token = ZohoModel.get_access_token()
    #             header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #             response = requests.get(f"{sd.zoho_payments}/{id}?organization_id={sd.organization_id}", headers=header)
    #             lw.logBackUpRecord(ZohoModel.access_token)
    #         # lw.logBackUpRecord("Payment Details Data:" + str(response.json()))
    #         return response.json()
    #     except Exception as e:
    #         lw.logRecord("Error in fetch_payments_details: " + str(e))

    @staticmethod
    def update_invoice(id, body):
        """Fetch Update Invoices from Zoho CRM"""
        try:
            body['due_date'] = body['due_date'].strftime('%Y-%m-%d')
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for Update Invoices.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_invoice}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            lw.logBackUpRecord("Update Invoice Json:" + str(body))
            json.dumps(body)
            # print(body)
            response = requests.put(f"{sd.zoho_invoice}/{id}?organization_id={sd.organization_id}", json=body, headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.put(f"{sd.zoho_invoice}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            lw.logBackUpRecord("Update Invoice status:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in update_invoice: " + str(e))

    @staticmethod
    def update_vendor_credit(id, body):
        """Fetch Update Vendor Credit from Zoho CRM"""
        try:
            body['due_date'] = body['due_date'].strftime('%Y-%m-%d')
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for Update Vendor Credit.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_dn}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            lw.logBackUpRecord("Update Vendor Credit Json:" + str(body))
            json.dumps(body)
            # print(body)
            response = requests.put(f"{sd.zoho_dn}/{id}?organization_id={sd.organization_id}", json=body, headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.put(f"{sd.zoho_dn}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            lw.logBackUpRecord("Update Vendor Credit status:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in update_vendor_credit: " + str(e))

    @staticmethod
    def update_bill(id, body):
        """Fetch Update Bills from Zoho CRM"""
        try:
            body['due_date'] = body['due_date'].strftime('%Y-%m-%d')
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for Update Bills.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_bills}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            lw.logBackUpRecord("Update Invoice Json:" + str(body))
            json.dumps(body)
            # print(body)
            response = requests.put(f"{sd.zoho_bills}/{id}?organization_id={sd.organization_id}", json=body, headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.put(f"{sd.zoho_bills}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            lw.logBackUpRecord("Update Bills status:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in update_bill: " + str(e))

    @staticmethod
    def update_credit_note(id, body):
        """Fetch Update Credit Note from Zoho CRM"""
        try:
            body['due_date'] = body['due_date'].strftime('%Y-%m-%d')
            # access_token = ZohoModel.get_access_token()
            lw.logBackUpRecord("Calling API for Update Credit Note.")
            lw.logBackUpRecord("URL:" + str(f"{sd.zoho_cn}/{id}?organization_id={sd.organization_id}"))
            header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
            lw.logBackUpRecord("Header:" + str(header))
            lw.logBackUpRecord("Update Invoice Json:" + str(body))
            json.dumps(body)
            # print(body)
            response = requests.put(f"{sd.zoho_cn}/{id}?organization_id={sd.organization_id}", json=body, headers=header, verify=False)
            if response.status_code == 401:
                ZohoModel.access_token = ZohoModel.get_access_token()
                header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
                response = requests.put(f"{sd.zoho_cn}/{id}?organization_id={sd.organization_id}", headers=header, verify=False)
                lw.logBackUpRecord(ZohoModel.access_token)
            lw.logBackUpRecord("Update Credit Note status:" + str(response.json()))
            return response.json()
        except Exception as e:
            lw.logRecord("Error in update_credit_note: " + str(e))

    # @staticmethod
    # def create_vendor_credit(body):
    #     """Creating Vendor Credits from Zoho CRM"""
    #     try:
    #         # body['due_date'] = body['due_date'].strftime('%Y-%m-%d')
    #         # access_token = ZohoModel.get_access_token()
    #         lw.logBackUpRecord("Calling API for Creating Vendor Credits.")
    #         lw.logBackUpRecord("URL:" + str(f"{sd.zoho_dn}?organization_id={sd.organization_id}"))
    #         header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #         lw.logBackUpRecord("Header:" + str(header))
    #         lw.logBackUpRecord("Creating Vendor Credits Json:" + str(body))
    #         json.dumps(body)
    #         # print(body)
    #         response = requests.post(f"{sd.zoho_dn}?organization_id={sd.organization_id}", json=body, headers=header)
    #         if response.status_code == 401:
    #             ZohoModel.access_token = ZohoModel.get_access_token()
    #             header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #             response = requests.post(f"{sd.zoho_dn}?organization_id={sd.organization_id}", headers=header)
    #             lw.logBackUpRecord(ZohoModel.access_token)
    #         # lw.logBackUpRecord("Creating Vendor Credits status:" + str(response.json()))
    #         return response.json()
    #     except Exception as e:
    #         lw.logRecord("Error in create_vendor_credit: " + str(e))

    # @staticmethod
    # def apply_to_bills(id, body):
    #     """Apply to bills from Zoho CRM"""
    #     try:
    #         # body['due_date'] = body['due_date'].strftime('%Y-%m-%d')
    #         # access_token = ZohoModel.get_access_token()
    #         lw.logBackUpRecord("Calling API for Apply to bills.")
    #         lw.logBackUpRecord("URL:" + str(f"{sd.zoho_dn}/{id}/bills?organization_id={sd.organization_id}"))
    #         header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #         lw.logBackUpRecord("Header:" + str(header))
    #         lw.logBackUpRecord("Apply to bills Json:" + str(body))
    #         json.dumps(body)
    #         # print(body)
    #         response = requests.post(f"{sd.zoho_dn}/{id}/bills?organization_id={sd.organization_id}", json=body, headers=header)
    #         if response.status_code == 401:
    #             ZohoModel.access_token = ZohoModel.get_access_token()
    #             header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #             response = requests.post(f"{sd.zoho_dn}/{id}/bills?organization_id={sd.organization_id}", headers=header)
    #             lw.logBackUpRecord(ZohoModel.access_token)
    #         print(response.json())
    #         lw.logBackUpRecord("Apply to bills status:" + str(response.json()))
    #         return response.json()
    #     except Exception as e:
    #         lw.logRecord("Error in apply_to_bills: " + str(e))

    # @staticmethod
    # def create_paymets(body):
    #     """Create Payments from Zoho CRM"""
    #     try:
    #         # body['due_date'] = body['due_date'].strftime('%Y-%m-%d')
    #         # access_token = ZohoModel.get_access_token()
    #         lw.logBackUpRecord("Calling API for creating Payments.")
    #         lw.logBackUpRecord("URL:" + str(f"{sd.zoho_payments}?organization_id={sd.organization_id}"))
    #         header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #         lw.logBackUpRecord("Header:" + str(header))
    #         lw.logBackUpRecord("Create Payments Json:" + str(body))
    #         json.dumps(body)
    #         # print(body)
    #         response = requests.post(f"{sd.zoho_payments}?organization_id={sd.organization_id}", json=body, headers=header)
    #         if response.status_code == 401:
    #             ZohoModel.access_token = ZohoModel.get_access_token()
    #             header = {"Authorization": f"Zoho-oauthtoken {ZohoModel.access_token}"}
    #             response = requests.post(f"{sd.zoho_payments}?organization_id={sd.organization_id}", headers=header)
    #             lw.logBackUpRecord(ZohoModel.access_token)
    #         print(response.json())

    #         # lw.logBackUpRecord("Create Payments status:" + str(json.dumps(response.json(), ensure_ascii=False)))
    #         return response.json()
    #     except Exception as e:
    #         lw.logRecord("Error in create_paymets: " + str(e))
