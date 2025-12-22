import views.logWriter as lw
from datetime import datetime
import config as sd
import config as sd
import models.ey_model as cm
from models.zoho_model import ZohoModel
import json
from collections import defaultdict

def grouped_data(data):
    grouped = {}
    for item in data:
        key = (
            item.get("docNo"),
            item.get("suppGstin"),
            item.get("docDate"),
            item.get("X_REQUEST_ID")
        )

        if key not in grouped:
            grouped[key] = {
                "docNo": item.get("docNo"),
                "suppGstin": item.get("suppGstin"),
                "docDate": item.get("docDate"),
                "docType": item.get("docType"),
                "status": item.get("status"),
                "X_REQUEST_ID": item.get("X_REQUEST_ID"),
                "AckNo": item.get("AckNo"),
                "NicAckNo": item.get("NicAckNo"),
                "AckDt": item.get("AckDt"),
                "Irn": item.get("Irn"),
                "SignedQRCode": item.get("SignedQRCode"),
                "SignedInvoice": item.get("SignedInvoice"),
                "EwbNo": item.get("EwbNo"),
                "EwbDt": item.get("EwbDt"),
                "EwbValidTill": item.get("EwbValidTill"),
                "errorDetails": [],
                "InfoDtls": item.get("InfoDtls")
            }

        # merge errorDetails
        if item.get("errorDetails"):
            grouped[key]["errorDetails"].extend(item["errorDetails"])
    result = list(grouped.values())
    return result

def bulkInvoices_CN(invoice, data_list):
    try:
        response = cm.sales(invoice)
        # print(response)
        if response['status'] != '1':
            lw.logBackUpRecord("Bulk Invoice/CN Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Invoice/CN Data has been uploaded Successfully.")
            # json_data = json.dumps(response, indent=4)
            json_data = response
            print(str(json_data['AckNo']))
            cm.get_status(str(json_data['AckNo']))
            response = cm.get_sales_data(str(json_data['AckNo']))
            # json_data = json.dumps(response, indent=4)
            # json_data = response
            json_data = grouped_data(response)
            print(json_data)
            for data in json_data:
                error_message = field_id1 = field_id2 = ''
                print(data['docNo'])
                
                try:
                    data_id = next(item['id'] for item in data_list if item['number'] == str(data['docNo']))
                    if data.get("errorDetails") and (data.get("status") == "0"):
                        for err in data["errorDetails"]:
                            error_message += err.get('errorDesc') + "at lineNo " + err.get('lineNo') + ". "
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
        print(response)
        if response['status'] != '1':
            lw.logBackUpRecord("Bulk Bills/DN Data has been uploaded with error.")
        else:
            lw.logBackUpRecord("Bulk Bills/DN Data has been uploaded Successfully.")
            # json_data = json.dumps(response, indent=4)
            json_data = response
            print(str(json_data['AckNo']))
            cm.get_status(str(json_data['AckNo']))
            response = cm.get_purchase_data(str(json_data['AckNo']))
            # json_data = json.dumps(response, indent=4)
            # json_data = response
            json_data = grouped_data(response)
            for data in json_data:
                error_message = field_id1 = field_id2 = ''
                print(data['docNo'])
                
                try:
                    data_id = next(item['id'] for item in data_list if item['number'] == str(data['docNo']))
                    if data.get("errorDetails") and (data.get("status") == "0"):
                        for err in data["errorDetails"]:
                            error_message += err.get('errorDesc') + "at lineNo " + err.get('lineNo') + ". "
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
                                    "value_formatted": str(error_message),
                                    "search_entity": "bill",
                                    "data_type": "string",
                                    "placeholder": "cf_sync_message",
                                    "value": str(error_message),
                                    "is_dependent_field": False
                                }
                            ]
                        }
                        
                    if str(data['docType']) == 'INV' or str(data['docType']) == 'SLF':
                        ZohoModel.update_bill(data_id, json_up)
                    else:
                        ZohoModel.update_vendor_credit(data_id, json_up)
                        pass
                except Exception as e:
                    print(str(e))
        pass
    except Exception as e:
        lw.logRecord("Error in bulkBills_DN: " + str(e))

