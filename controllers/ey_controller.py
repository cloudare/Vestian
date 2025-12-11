import views.logWriter as lw
from datetime import datetime
import config as sd
import config as sd
import models.ey_model as cm
from models.zoho_model import ZohoModel
import json


# def bulkVendor(vendors):
#     try:
#         # print(vendors)
#         response = cm.bulkVendorMaster(vendors)
#         # print(response)
#         if response.status_code != 200:
#             lw.logBackUpRecord("Bulk Vendor Data has been uploaded with error.")
#         else:
#             lw.logBackUpRecord("Bulk Vendor Data has been uploaded Successfully.")
#         pass
#     except Exception as e:
#         lw.logRecord("Error in bulkVendor: " + str(e))

def bulkInvoices_CN(invoice, data_list):
    try:
        response = cm.sales(invoice)
        # print(response)
        if response.status_code != 200:
            lw.logBackUpRecord("Bulk Invoice/CN Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Invoice/CN Data has been uploaded Successfully.")
            json_data = json.dumps(response, indent=4)
            print(str(json_data['AckNo']))
            cm.get_status(str(json_data['AckNo']))
            response = cm.get_sales_data(str(json_data['AckNo']))
            json_data = json.dumps(response, indent=4)
            for data in json_data:
                error_message = field_id1 = field_id2 = ''
                print(data['docNo'])
                
                try:
                    data_id = next(item['number'] for item in data_list if item['number'] == str(data['docNo']))
                    if data.get("errorDetails") and (data.get("status") == "0"):
                        for err in data["errorDetails"]:
                            error_message += err.get('errorDesc')
                    if str(data['docType']) == 'INV':
                        field_id1 = "3264698000000109001"
                        field_id2 = "3264698000000109009"
                    else:
                        field_id1 = "3264698000000113075"
                        field_id2 = "3264698000000113083"

                    if error_message == '':
                        json_up = {
                            "custom_fields": [
                                {
                                    "field_id": str(field_id1),
                                    "customfield_id": str(field_id1),
                                    "show_in_store": False,
                                    "show_in_portal": False,
                                    "is_active": True,
                                    "index": 1,
                                    "label": "Sync_Status",
                                    "show_on_pdf": False,
                                    "edit_on_portal": False,
                                    "edit_on_store": False,
                                    "is_color_code_supported": False,
                                    "api_name": "cf_sync_status",
                                    "show_in_all_pdf": False,
                                    "selected_option_id": "3264698000000113005",
                                    "value_formatted": "TRUE",
                                    "search_entity": "bill",
                                    "data_type": "dropdown",
                                    "placeholder": "cf_sync_status",
                                    "value": "TRUE",
                                    "is_dependent_field": False
                                },
                                {
                                    "field_id": str(field_id2),
                                    "customfield_id": str(field_id2),
                                    "show_in_store": False,
                                    "show_in_portal": False,
                                    "is_active": True,
                                    "index": 2,
                                    "label": "Sync_Message",
                                    "show_on_pdf": False,
                                    "edit_on_portal": False,
                                    "edit_on_store": False,
                                    "api_name": "cf_sync_message",
                                    "show_in_all_pdf": False,
                                    "value_formatted": "Sent Syccessfully",
                                    "search_entity": "bill",
                                    "data_type": "string",
                                    "placeholder": "cf_sync_message",
                                    "value": "Sent Syccessfully",
                                    "is_dependent_field": False
                                }
                            ]
                        }
                    else:
                        json_up = {
                            "custom_fields": [
                                {
                                    "field_id": str(field_id1),
                                    "customfield_id": str(field_id1),
                                    "show_in_store": False,
                                    "show_in_portal": False,
                                    "is_active": True,
                                    "index": 1,
                                    "label": "Sync_Status",
                                    "show_on_pdf": False,
                                    "edit_on_portal": False,
                                    "edit_on_store": False,
                                    "is_color_code_supported": False,
                                    "api_name": "cf_sync_status",
                                    "show_in_all_pdf": False,
                                    "selected_option_id": "3264698000000113005",
                                    "value_formatted": "FALSE",
                                    "search_entity": "bill",
                                    "data_type": "dropdown",
                                    "placeholder": "cf_sync_status",
                                    "value": "FALSE",
                                    "is_dependent_field": False
                                },
                                {
                                    "field_id": str(field_id2),
                                    "customfield_id": str(field_id2),
                                    "show_in_store": False,
                                    "show_in_portal": False,
                                    "is_active": True,
                                    "index": 2,
                                    "label": "Sync_Message",
                                    "show_on_pdf": False,
                                    "edit_on_portal": False,
                                    "edit_on_store": False,
                                    "api_name": "cf_sync_message",
                                    "show_in_all_pdf": False,
                                    "value_formatted": str(error_message),
                                    "search_entity": "bill",
                                    "data_type": "string",
                                    "placeholder": "cf_sync_message",
                                    "value": str(error_message),
                                    "is_dependent_field": False
                                }
                            ]
                        }
                        
                    if str(data['docType']) == 'INV':
                        ZohoModel.update_invoice(data_id, json_up)
                    else:
                        ZohoModel.update_credit_note(data_id, json_up)
                        pass
                except Exception as e:
                    print(str(e))

        pass
    except Exception as e:
        lw.logRecord("Error in bulkInvoices_CN: " + str(e))

def bulkBills_DN(cndn, data_list):
    try:
        response = cm.purchase(cndn)
        # print(response)
        if response.status_code != 200:
            lw.logBackUpRecord("Bulk Bills/DN Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Bills/DN Data has been uploaded Successfully.")
            json_data = json.dumps(response, indent=4)
            print(str(json_data['AckNo']))
            cm.get_status(str(json_data['AckNo']))
            response = cm.get_purchase_data(str(json_data['AckNo']))
            json_data = json.dumps(response, indent=4)
            for data in json_data:
                error_message = field_id1 = field_id2 = ''
                print(data['docNo'])
                
                try:
                    data_id = next(item['number'] for item in data_list if item['number'] == str(data['docNo']))
                    if data.get("errorDetails") and (data.get("status") == "0"):
                        for err in data["errorDetails"]:
                            error_message += err.get('errorDesc')
                    if str(data['docType']) == 'INV':
                        field_id1 = "3264698000000113001"
                        field_id2 = "3264698000000113009"
                    else:
                        field_id1 = "3264698000000113065"
                        field_id2 = "3264698000000113061"

                    if error_message == '':
                        json_up = {
                            "custom_fields": [
                                {
                                    "field_id": str(field_id1),
                                    "customfield_id": str(field_id1),
                                    "show_in_store": False,
                                    "show_in_portal": False,
                                    "is_active": True,
                                    "index": 1,
                                    "label": "Sync_Status",
                                    "show_on_pdf": False,
                                    "edit_on_portal": False,
                                    "edit_on_store": False,
                                    "is_color_code_supported": False,
                                    "api_name": "cf_sync_status",
                                    "show_in_all_pdf": False,
                                    "selected_option_id": "3264698000000113005",
                                    "value_formatted": "TRUE",
                                    "search_entity": "bill",
                                    "data_type": "dropdown",
                                    "placeholder": "cf_sync_status",
                                    "value": "TRUE",
                                    "is_dependent_field": False
                                },
                                {
                                    "field_id": str(field_id2),
                                    "customfield_id": str(field_id2),
                                    "show_in_store": False,
                                    "show_in_portal": False,
                                    "is_active": True,
                                    "index": 2,
                                    "label": "Sync_Message",
                                    "show_on_pdf": False,
                                    "edit_on_portal": False,
                                    "edit_on_store": False,
                                    "api_name": "cf_sync_message",
                                    "show_in_all_pdf": False,
                                    "value_formatted": "Sent Syccessfully",
                                    "search_entity": "bill",
                                    "data_type": "string",
                                    "placeholder": "cf_sync_message",
                                    "value": "Sent Syccessfully",
                                    "is_dependent_field": False
                                }
                            ]
                        }
                    else:
                        json_up = {
                            "custom_fields": [
                                {
                                    "field_id": str(field_id1),
                                    "customfield_id": str(field_id1),
                                    "show_in_store": False,
                                    "show_in_portal": False,
                                    "is_active": True,
                                    "index": 1,
                                    "label": "Sync_Status",
                                    "show_on_pdf": False,
                                    "edit_on_portal": False,
                                    "edit_on_store": False,
                                    "is_color_code_supported": False,
                                    "api_name": "cf_sync_status",
                                    "show_in_all_pdf": False,
                                    "selected_option_id": "3264698000000113005",
                                    "value_formatted": "FALSE",
                                    "search_entity": "bill",
                                    "data_type": "dropdown",
                                    "placeholder": "cf_sync_status",
                                    "value": "FALSE",
                                    "is_dependent_field": False
                                },
                                {
                                    "field_id": str(field_id2),
                                    "customfield_id": str(field_id2),
                                    "show_in_store": False,
                                    "show_in_portal": False,
                                    "is_active": True,
                                    "index": 2,
                                    "label": "Sync_Message",
                                    "show_on_pdf": False,
                                    "edit_on_portal": False,
                                    "edit_on_store": False,
                                    "api_name": "cf_sync_message",
                                    "show_in_all_pdf": False,
                                    "value_formatted": str(error_message),
                                    "search_entity": "bill",
                                    "data_type": "string",
                                    "placeholder": "cf_sync_message",
                                    "value": str(error_message),
                                    "is_dependent_field": False
                                }
                            ]
                        }
                        
                    if str(data['docType']) == 'INV':
                        ZohoModel.update_bill(data_id, json_up)
                    else:
                        ZohoModel.update_vendor_credit(data_id, json_up)
                        pass
                except Exception as e:
                    print(str(e))
        pass
    except Exception as e:
        lw.logRecord("Error in bulkBills_DN: " + str(e))

# def payments(payments):
#     try:
#         # print(payments)
#         response = cm.payments(payments)
#         # print(response.json())
#         if response.status_code != 200:
#             lw.logBackUpRecord("Bulk Vendor Data has been uploaded with error.")
#         else:
#             lw.logBackUpRecord("Bulk Vendor Data has been uploaded Successfully.")
#         pass
#     except Exception as e:
#         lw.logRecord("Error in payments: " + str(e))

# def update_invoice(data, t, v, i, vi, da, dd, md):
#     try:
#         try:
#             discount_account_id = data['discount_account_id']
#         except:
#             discount_account_id = ""

#         if discount_account_id == "":
#             discount_account_id = sd.discount_id

#         # diff = (datetime.strptime(md, '%Y-%m-%d')) - (datetime.strptime(data['date'], '%Y-%m-%d')).days
#         json = {
#             "discount_account_id": discount_account_id,
#             "bill_id": i,
#             "due_date": datetime.strptime(md, '%Y-%m-%d'),
#             "payment_terms": -1, #diff,
#             "payment_terms_label": "Custom", #"Net " + str(diff),
#             "discount": float(da) + float(data['discount_amount'])
#         }
#         # print(json)
#         response = ZohoModel.update_invoice(i, json)
#         # print(response)
#         postingAck(t, v, i, vi)
#         pass
#     except Exception as e:
#         lw.logRecord("Error in update_invoice: " + str(e))

# def postingAck(t, v, i, vi):
#     try:
#         data = [{
#             "transactionId": t,
#             "vendorId": v,
#             "internalInvoiceNumber": i,
#             "vendorInvoiceNumber": vi,
#             "postingStatus": "True",
#             "postingResponse": "Success",
#             "referenceNumber": i,
#             "voucherPosted": "Yes",
#             "invoiceeyed": "No",
#             "invoiceUpdated": "Yes",
#             "postingDate": str((datetime.now()).strftime("%d-%m-%Y"))
#             }]
#         # data['postingDate'] = data['postingDate'].strftime('%Y-%m-%d')
#         json.dumps(data)
#         # print(data)
#         response = cm.postingAck(data)
#         # print(response)
#         if response[0]['status'] == 'Success':
#             lw.logBackUpRecord('Posting of Bill has been acknowledged.')
#     except Exception as e:
#         lw.logRecord("Error in postingAck: " + str(e))

# def postingCreditDebitNote():
#     try:
#         json = {
#             "userName": str(sd.userName)
#         }
#         response = cm.postingCreditDebitNote(json)
#         # print(response)
#         transactionId = []
#         vendorId = [] 
#         internalInvoiceNumber = []
#         vendorInvoiceNumber = []
#         discountAmount = []
#         discountingDate = []
#         maturityDate = []
#         vendorName = []
#         if response != []:
#             if response:
#                 for data in response:
#                     transactionId.append(data.get('id'))
#                     vendorId.append(data.get('vendorId'))
#                     vendorName.append(data.get('vendorName'))
#                     internalInvoiceNumber.append(data.get('internalInvoiceNumber'))
#                     vendorInvoiceNumber.append(data.get('vendorInvoiceNumber'))
#                     discountAmount.append(data.get('discountAmount'))
#                     discountingDate.append(data.get('discountingDate'))
#                     maturityDate.append(data.get('maturityDate'))
#                     # referenceNumber = data.get('transactionId')
#             # print(transactionId)
#             # print(vendorId)
#             # print(internalInvoiceNumber)
#             # print(vendorInvoiceNumber)
#             # print(discountAmount)
#             # print(discountAmount)
#             # print(maturityDate)
#         return transactionId, vendorId, vendorName, internalInvoiceNumber, vendorInvoiceNumber, discountAmount, discountingDate, maturityDate
#     except Exception as e:
#         lw.logRecord("Error in postingCreditDebitNote: " + str(e))
