from models.zoho_model import ZohoModel
import controllers.ey_controller as cc
import views.logWriter as lw
from datetime import datetime
from itertools import zip_longest
import config as sd

class ZohoController:
    @staticmethod
    def get_fiscal_year(date):
        try:
            year = date.year
            if date.month < 4:  # Before April, it's part of the previous fiscal year
                return f"{year}"
            else:  # April onwards, it's the current fiscal year
                return f"{year+1}"
        except Exception as e:
            lw.logRecord("Error in get_fiscal_year: " + str(e))

    @staticmethod
    def create_line_items(items, reverse, gstin):
        print(items)
        itemlist = []
        # print(is_tax_line)
        for idx, data in enumerate(items):
            service = 'N'
            igstRt = cgstRt = igstAmt = cgstAmt = igst_tds = cgst_tds = avail_igst = avail_cgst = 0
            #  = 0
            supplytype = "TAX"
            if data['hsn_or_sac'][:2] == '99':
                service = 'Y'
            try:
                print(data['tax_percentage'])
            except:
                pass
            if str(gstin) == 'URP':
                supplytype = 'IMP'
            if (reverse == 'N'):
                if (float(data['tax_percentage']) > 0.0):
                    # if is_tax_line == True:
                    try:
                        if data['line_item_taxes'][0]['tax_specific_type'] == 'IGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'igst':
                            igstRt = data['line_item_taxes'][0]['tax_percentage']
                            igstAmt = data['line_item_taxes'][0]['tax_amount']
                        elif (data['line_item_taxes'][0]['tax_specific_type'] == 'CGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'cgst') or (data['line_item_taxes'][0]['tax_specific_type'] == 'sGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'sgst'):
                            cgstRt = data['line_item_taxes'][0]['tax_percentage']
                            cgstAmt = data['line_item_taxes'][0]['tax_amount']
                        # if (data['line_item_taxes'][0]['tax_amount'] > 0):
                        #     supplytype = "TAX"
                    except:
                        try:
                            if data['line_item_taxes'][0]['tax_name'][:4] == 'IGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'igst':
                                igstRt = data['line_item_taxes'][0]['tax_name'][4:6]
                                igstAmt = data['line_item_taxes'][0]['tax_amount']
                            elif (data['line_item_taxes'][0]['tax_name'][:4] == 'CGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'cgst') or (data['line_item_taxes'][0]['tax_specific_type'] == 'sGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'sgst'):
                                cgstRt = (data['line_item_taxes'][0]['tax_name'][4:6]).replace(" ","")
                                cgstAmt = data['line_item_taxes'][0]['tax_amount']
                            # if (data['line_item_taxes'][0]['tax_amount'] > 0):
                            #     supplytype = "TAX"
                        except Exception as e:
                            print(str(e))
                else:
                    try:
                        if data['line_item_taxes'][0]['tax_name'][:4] == 'IGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'igst':
                            igstRt = data['line_item_taxes'][0]['tax_name'][4:6]
                            igstAmt = data['line_item_taxes'][0]['tax_amount']
                        elif (data['line_item_taxes'][0]['tax_name'][:4] == 'CGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'cgst') or (data['line_item_taxes'][0]['tax_specific_type'] == 'sGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'sgst'):
                            cgstRt = (data['line_item_taxes'][0]['tax_name'][4:6]).replace(" ","")
                            cgstAmt = data['line_item_taxes'][0]['tax_amount']
                        # if (data['line_item_taxes'][0]['tax_amount'] > 0):
                        #     supplytype = "TAX"
                    except Exception as e:
                        print(str(e))
            else:
                if data['reverse_charge_tax_name'][:4] == 'IGST':
                    igstRt = data['reverse_charge_tax_percentage']
                    igstAmt = data['reverse_charge_tax_amount']
                elif (data['reverse_charge_tax_name'][:4] == 'CGST') or data['reverse_charge_tax_name'][:4] == 'IGST':
                    cgstRt = data['reverse_charge_tax_percentage']
                    cgstAmt = float(data['reverse_charge_tax_amount'] / 2)
                # if (data['reverse_charge_tax_amount'] > 0):
                #     supplytype = "TAX"
            try:
                if float(igstAmt) > 0.0:
                    if float(data['tds_tax_percentage']) > 0.0:
                        igst_tds = float(data['tds_tax_amount'])
                else:
                    if float(data['tds_tax_percentage']) > 0.0:
                        cgst_tds = float(data['tds_tax_amount'])/2
            except Exception as e:
                print(str(e))
            eligIndicator = itc = ""
            
            if (data['itc_eligibility'] == 'eligible'):
                if (service == 'Y'):
                    eligIndicator = "IS"
                else:
                    eligIndicator = "IG"
            else:
                    eligIndicator = "NO"
            if eligIndicator != "NO":
                avail_igst = igstAmt
                avail_cgst = cgstAmt
            if str(data['itc_eligibility']) == 'eligible':
                itc = 'Y'
            lineitems = {
                # Optional
                "itemNo": idx +1,
                "glCodeTaxableVal": "",
                "supplyType": supplytype,
                "cif": "",
                "customDuty": "",
                "hsnsacCode": str(data['hsn_or_sac']),
                "productCode": "", #"100000009185728",
                "itemDesc": data['description'].replace('"',"'").replace("\n",""),
                "itemType": data['item_type'], #"FG",
                "itemUqc": data['unit'],
                "itemQty": data['quantity'],
                "taxableVal": data['item_total'],
                "igstRt": igstRt,
                "igstAmt": igstAmt,
                "cgstRt": cgstRt,
                "cgstAmt": cgstAmt,
                "sgstRt": cgstRt,
                "sgstAmt": cgstAmt,
                "tcsIgstAmnt": 0,
                "tcsCgstAmt": 0,
                "tcsSgstAmt": 0,
                "tdsIgstAmt": igst_tds,
                "tdsCgstAmt": cgst_tds,
                "tdsSgstAmt": cgst_tds,
                "itcEntitlement": itc,
                "lineItemAmt": "",
                "crDrReason": "",
                "unitPrice": "",
                "itemAmt": "",
                "itemDiscount": "0",
                "preTaxAmt": "",
                "totalItemAmt": "",
                "preceedingInvNo": "",
                "preceedingInvDate": "",
                "orderLineRef": "",
                "supportingDocURL": "",
                "supportingDocBase64": "",
                "eligIndicator": eligIndicator,
                "availIgst": avail_igst,
                "availCgst": avail_cgst,
                "availSgst": avail_cgst,
                "availCess": "0",
                "udf1": "", #"257026"
            }
            itemlist.append(lineitems)
        print(itemlist)
        return itemlist
    

    @staticmethod
    def create_line_items_sales(items, reverse, gstin):
        try:
            print(items)
            itemlist = []
            # print(is_tax_line)
            for idx, data in enumerate(items):
                service = 'N'
                igstRt = cgstRt = igstAmt = cgstAmt = igst_tds = cgst_tds = avail_igst = avail_cgst = 0
                #  = 0
                supplytype = "NIL"
                if data['hsn_or_sac'][:2] == '99':
                    service = 'Y'
                try:
                    print(data['tax_percentage'])
                except:
                    pass
                if str(gstin) == 'URP':
                    supplytype = 'EXP'
                if (reverse == 'N'):
                    if (float(data['tax_percentage']) > 0.0):
                        # if is_tax_line == True:
                        try:
                            if data['line_item_taxes'][0]['tax_specific_type'] == 'IGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'igst':
                                igstRt = data['line_item_taxes'][0]['tax_percentage']
                                igstAmt = data['line_item_taxes'][0]['tax_amount']
                            elif (data['line_item_taxes'][0]['tax_specific_type'] == 'CGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'cgst') or (data['line_item_taxes'][0]['tax_specific_type'] == 'sGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'sgst'):
                                cgstRt = data['line_item_taxes'][0]['tax_percentage']
                                cgstAmt = data['line_item_taxes'][0]['tax_amount']
                            if (data['line_item_taxes'][0]['tax_amount'] > 0) and (supplytype != 'EXP'):
                                supplytype = "TAX"
                        except:
                            try:
                                if data['line_item_taxes'][0]['tax_name'][:4] == 'IGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'igst':
                                    igstRt = data['line_item_taxes'][0]['tax_name'][4:6]
                                    igstAmt = data['line_item_taxes'][0]['tax_amount']
                                elif (data['line_item_taxes'][0]['tax_name'][:4] == 'CGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'cgst') or (data['line_item_taxes'][0]['tax_specific_type'] == 'sGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'sgst'):
                                    cgstRt = (data['line_item_taxes'][0]['tax_name'][4:6]).replace(" ","")
                                    cgstAmt = data['line_item_taxes'][0]['tax_amount']
                                if (data['line_item_taxes'][0]['tax_amount'] > 0) and (supplytype != 'EXP'):
                                    supplytype = "TAX"
                            except Exception as e:
                                print(str(e))
                    else:
                        try:
                            if data['line_item_taxes'][0]['tax_name'][:4] == 'IGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'igst':
                                igstRt = data['line_item_taxes'][0]['tax_name'][4:6]
                                igstAmt = data['line_item_taxes'][0]['tax_amount']
                            elif (data['line_item_taxes'][0]['tax_name'][:4] == 'CGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'cgst') or (data['line_item_taxes'][0]['tax_specific_type'] == 'sGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'sgst'):
                                cgstRt = (data['line_item_taxes'][0]['tax_name'][4:6]).replace(" ","")
                                cgstAmt = data['line_item_taxes'][0]['tax_amount']
                            if (data['line_item_taxes'][0]['tax_amount'] > 0) and (supplytype != 'EXP'):
                                supplytype = "TAX"
                        except Exception as e:
                            print(str(e))
                else:
                    try:
                        if data['reverse_charge_tax_name'][:4] == 'IGST':
                            igstRt = data['reverse_charge_tax_percentage']
                            igstAmt = data['reverse_charge_tax_amount']
                        elif (data['reverse_charge_tax_name'][:4] == 'CGST') or data['reverse_charge_tax_name'][:4] == 'IGST':
                            cgstRt = data['reverse_charge_tax_percentage']
                            cgstAmt = float(data['reverse_charge_tax_amount'] / 2)
                        if (data['line_item_taxes'][0]['tax_amount'] > 0) and (supplytype != 'EXP'):
                            supplytype = "TAX"
                    except Exception as e:
                        print(str(e))
                        try:
                            if data['line_item_taxes'][0]['tax_name'][:4] == 'IGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'igst':
                                igstRt = data['line_item_taxes'][0]['tax_name'][4:6]
                                igstAmt = data['line_item_taxes'][0]['tax_amount']
                            elif (data['line_item_taxes'][0]['tax_name'][:4] == 'CGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'cgst') or (data['line_item_taxes'][0]['tax_specific_type'] == 'sGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'sgst'):
                                cgstRt = (data['line_item_taxes'][0]['tax_name'][4:6]).replace(" ","")
                                cgstAmt = data['line_item_taxes'][0]['tax_amount']
                            if (data['line_item_taxes'][0]['tax_amount'] > 0) and (supplytype != 'EXP'):
                                supplytype = "TAX"
                        except Exception as e:
                            print(str(e))
                        
                try:
                    if str(data['tds_tax_percentage']) != "":
                        if float(igstAmt) > 0.0:
                            if float(data['tds_tax_percentage']) > 0.0:
                                igst_tds = float(data['tds_tax_amount'])
                        else:
                            if float(data['tds_tax_percentage']) > 0.0:
                                cgst_tds = float(data['tds_tax_amount'])/2
                except Exception as e:
                    print(str(e))
                eligIndicator = itc = ""
                try:
                    # if (data['itc_eligibility'] == 'eligible'):
                    if (service == 'Y'):
                        eligIndicator = "IS"
                    else:
                        eligIndicator = "IG"
                    if (float(igstAmt) <= 0.0) and (float(cgstAmt) <= 0.0):
                        eligIndicator = "NO"
                except:
                    pass
                if eligIndicator != "NO":
                    avail_igst = igstAmt
                    avail_cgst = cgstAmt
                try:
                    if str(data['itc_eligibility']) == 'eligible':
                        itc = 'Y'
                except:
                    pass
                lineitems = {
                    # Optional
                    "itemNo": idx +1,
                    "glCodeTaxableVal": "",
                    "supplyType": supplytype,
                    "cif": "",
                    "customDuty": "",
                    "hsnsacCode": str(data['hsn_or_sac']),
                    "productCode": "", #"100000009185728",
                    "itemDesc": data['description'].replace('"',"'").replace("\n",""),
                    "itemType": data['item_type'], #"FG",
                    "itemUqc": data['unit'],
                    "itemQty": data['quantity'],
                    "taxableVal": data['item_total'],
                    "igstRt": igstRt,
                    "igstAmt": igstAmt,
                    "cgstRt": cgstRt,
                    "cgstAmt": cgstAmt,
                    "sgstRt": cgstRt,
                    "sgstAmt": cgstAmt,
                    "tcsIgstAmnt": 0,
                    "tcsCgstAmt": 0,
                    "tcsSgstAmt": 0,
                    "tdsIgstAmt": igst_tds,
                    "tdsCgstAmt": cgst_tds,
                    "tdsSgstAmt": cgst_tds,
                    "itcEntitlement": itc,
                    "lineItemAmt": "",
                    "crDrReason": "",
                    "unitPrice": "",
                    "itemAmt": "",
                    "itemDiscount": "0",
                    "preTaxAmt": "",
                    "totalItemAmt": "",
                    "preceedingInvNo": "",
                    "preceedingInvDate": "",
                    "orderLineRef": "",
                    "supportingDocURL": "",
                    "supportingDocBase64": "",
                    "eligIndicator": eligIndicator,
                    "availIgst": avail_igst,
                    "availCgst": avail_cgst,
                    "availSgst": avail_cgst,
                    "availCess": "0",
                    "udf1": "", #"257026"
                }
                itemlist.append(lineitems)
            print(itemlist)
            return itemlist
        except Exception as e:
            print(str(e))
            pass

    # @staticmethod
    # def get_contacts():
    #     """Fetch contacts and format response"""
    #     try:
    #         has_more_page = True
    #         page = 1
    #         customers = []
    #         vendors = []
    #         while (has_more_page == True):
    #             data = ZohoModel.fetch_contacts(page)
    #             page += 1

    #             if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
    #                 has_more_page = False

    #             if "contacts" in data and data["contacts"]:
    #                 for idx, item in enumerate(data['contacts'], start=1):
    #                     try:
    #                         if item['contact_type'] == "vendor":
    #                             # print(str(item['contact_id']))
    #                             details = ZohoModel.fetch_contacts_details(str(item['contact_id']))
    #                             try:
    #                                 msme_data = details['contact']['msme_type']
    #                             except:
    #                                 msme_data = ''
    #                             msme = ''
    #                             if msme_data != '':
    #                                 msme = 'MSME'
    #                             # if str(details['contact']['contact_id']) == '2362602000000054387':
    #                             #     pass
    #                             vendor = {
    #                                     "vendorID": details['contact']['contact_id'],
    #                                     "vendorName": details['contact']['company_name'] if details['contact']['company_name'] is not None else '',
    #                                     "keyContactPerson": str(details['contact']['contact_salutation']) + str(details['contact']['first_name']) + str(details['contact']['last_name']),
    #                                     "emailId": details['contact']['email'],
    #                                     "mobileNo": details['contact']['phone'],
    #                                     "panNumber": details['contact']['pan_no'],
    #                                     "address1": details['contact']['billing_address']['address'],
    #                                     "address2": details['contact']['billing_address']['street2'],
    #                                     "address3": '',#details['contact']['billing_address']['city'],
    #                                     "city": details['contact']['billing_address']['city'],
    #                                     "state": details['contact']['billing_address']['state'],
    #                                     "pinCode": details['contact']['billing_address']['zip'],
    #                                     "gstin": details['contact']['gst_no'],
    #                                     "createdDate": datetime.strptime((details['contact']['created_date']), '%d/%m/%Y').strftime('%Y-%m-%d'),
    #                                     "cin": '', #details['contact']['contact_name'],
    #                                     "companyClass": '', #details['contact']['contact_name'],
    #                                     "companyCategory": '', #details['contact']['contact_name'],
    #                                     "companySubCategory": '', #details['contact']['contact_name'],
    #                                     "userName": "api@eatgoods.com", #details['contact']['created_by_name'],
    #                                     # "companyCode": sd.organization_id, #details['contact']['contact_name'],
    #                                     "companyCreationDate": '', #details['contact']['contact_name'],
    #                                     "category": msme
    #                                 }
    #                             vendors.append(vendor)
    #                     except Exception as e:
    #                         lw.logRecord("Error in get_contacts for loop: " + str(e))
    #             # print("Vendors" + str(vendors))
    #             # print("Customers" + str(customers))
    #             cc.bulkVendor(vendors)
    #             pass
    #         # return vendors#, customers
    #     except Exception as e:
    #         lw.logRecord("Error in get_contacts: " + str(e))

    @staticmethod
    def bulkBills():
        """Fetch Bills and format response"""
        try:
            has_more_page = True
            page = 1
            bills = {"req": []}
            while (has_more_page == True):
                data = ZohoModel.fetch_bills(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "bills" in data and data["bills"]:
                    for idx, item in enumerate(data['bills'], start=1):
                        try:
                            if item['entity_type'] == "bill":
                                # print(str(item['bill_id']))
                                details = ZohoModel.fetch_bill_details(str(item['bill_id']))
                                print(details['bill']['total'])
                                custdetails = sd.organization_address[str(details['bill']['branch_name'])]
                                reverse = 'N'
                                print(details['bill']['is_reverse_charge_applied'])
                                print(type(details['bill']['is_reverse_charge_applied']))
                                if (details['bill']['is_reverse_charge_applied'] != False):
                                    reverse = 'Y'
                                # is_tax_line = details['bill']['is_item_level_tax_calc']
                                supgstin = "URP"
                                suppin = "999999"
                                supStateCode = "96"
                                print(details['bill']['gst_no'])
                                if details['bill']['gst_no'] != "":
                                    supgstin = details['bill']['gst_no']
                                    supStateCode = supgstin[:2]
                                    suppin = details['bill']['billing_address']['zip']
                                line_items = ZohoController.create_line_items(details['bill']['line_items'], reverse, supgstin)                               
                                formatted_date = (datetime.strptime(str(details['bill']['date']), "%Y-%m-%d"))
                                date = formatted_date.strftime("%d/%m/%Y")
                                return_period = formatted_date.strftime("%m%Y")
                                crDrPreGst = "N"
                                igstRt = cgstRt = igstAmt = cgstAmt = 0
                                sup_type = ""
                                tdsFlag = "N"
                                try:
                                    if float(details['vendor_credit']['tds_percent']) > 0.0:
                                        tdsFlag = 'Y'
                                except Exception as e:
                                    print(str(e))
                                if str(details['bill']['gst_treatment']) == "overseas":
                                    if float(details['bill']['tax_total']) >0.0:
                                        sup_type = "TAX"
                                    else:
                                        sup_type = "TAX"
                                elif str(details['bill']['gst_treatment']) == "business_gst":
                                    sup_type = "TAX"
                                elif str(details['bill']['gst_treatment']) == "business_sez":
                                    if float(details['bill']['tax_total']) >0.0:
                                        sup_type = "TAX"
                                    else:
                                        sup_type = "TAX"
                                if reverse == 'N':
                                    if (float(details['bill']['tax_total']) > 0.0):
                                        # if is_tax_line == True:
                                        taxtype = ''.join([c for c in str(details['bill']['taxes'][0]['tax_name']) if c.isalpha()])
                                        if taxtype == 'IGST' or taxtype == 'igst':
                                            igstRt = ''.join([c for c in str(details['bill']['taxes'][0]['tax_name']) if c.isdigit()])
                                            igstAmt = details['bill']['taxes'][0]['tax_amount']
                                        elif (taxtype == 'CGST' or taxtype == 'cgst') or (taxtype == 'SGST' or taxtype == 'sgst'):
                                            cgstRt = ''.join([c for c in str(details['bill']['taxes'][0]['tax_name']) if c.isdigit()])
                                            cgstAmt = details['bill']['taxes'][0]['tax_amount']
                                else:
                                    taxtype = ''.join([c for c in str(details['bill']['reverse_charge_vat_summary'][0]['tax_name']) if c.isalpha()])
                                    if taxtype == 'IGST' or taxtype == 'igst':
                                        igstRt = ''.join([c for c in str(details['bill']['reverse_charge_vat_summary'][0]['tax_name']) if c.isdigit()])
                                        igstAmt = details['bill']['reverse_charge_vat_summary'][0]['tax_amount']
                                    elif (taxtype == 'CGST' or taxtype == 'cgst') or (taxtype == 'SGST' or taxtype == 'sgst'):
                                        cgstRt = ''.join([c for c in str(details['bill']['taxes'][0]['reverse_charge_vat_summary']) if c.isdigit()])
                                        cgstAmt = details['bill']['reverse_charge_vat_summary'][0]['tax_amount']
                                # custGstin = sd.organization_gst.get(str(details['bill']['branch_name']))
                                bill = {
                                    # Optional
                                    "srcFileName": "Standard",
                                    "srcIdentifier": "Zoho",
                                    "returnPeriod": str(return_period),
                                    "suppGstin": str(supgstin),
                                    "docType": "INV",
                                    "docNo": str(details['bill']['bill_number']),
                                    "docDate": str(date),
                                    "orgDocType": "",
                                    "crDrPreGst": crDrPreGst,
                                    "custGstin": str(custdetails['gstin']),
                                    "supType": str(sup_type),
                                    "diffPercent": "",
                                    "orgSgstin": "",
                                    "custOrSupName": "",
                                    "supCode": str(suppin),
                                    "custOrSupAddr1": str(custdetails['address_line1']),
                                    "custOrSupAddr2": str(custdetails['address_line2']),
                                    "custOrSupAddr4": str(custdetails['city']),
                                    "billToState": str(custdetails['state']),
                                    "shipToState": str(custdetails['state']),
                                    "pos": str((custdetails['gstin'])[:2]),
                                    "stateApplyingCess": "",
                                    "portCode": "",
                                    "billOfEntry": "",
                                    "billOfEntryDate": "",
                                    "reverseCharge": str(reverse),
                                    "accVoucherNo": "", #"202502011001321",
                                    "accVoucherDate": "", #"2025-10-07",
                                    "taxScheme": "",
                                    "docCat": "",
                                    "supTradeName": str(details['bill']['vendor_name']),
                                    "supLegalName": str(details['bill']['vendor_name']),
                                    "supBuildingNo": str(details['bill']['billing_address']['address']),
                                    "supBuildingName": "",
                                    "supLocation": "",
                                    "supPincode": str(suppin),
                                    "supStateCode": str(supStateCode),
                                    "supPhone": "",
                                    "supEmail": "",
                                    "custTradeName": "",
                                    "custPincode": "",
                                    "custPhone": "",
                                    "custEmail": "",
                                    "shipToGstin": "",
                                    "shipToTradeName": "",
                                    "shipToLegalName": "",
                                    "shipToBuildingNo": "",
                                    "shipToBuildingName": "",
                                    "shipToLocation": "",
                                    "shipToPincode": "",
                                    "invOtherCharges": "",
                                    "invAssessableAmt": str(details['bill']['sub_total']),
                                    "invIgstAmt": str(igstAmt),
                                    "invCgstAmt": str(cgstAmt),
                                    "invSgstAmt": str(cgstAmt),
                                    "invCessAdvaloremAmt": "",
                                    "roundOff": "",
                                    "exchangeRt": details['bill']['exchange_rate'],
                                    "totalInvValueInWords": "", #str(details['bill']['sub_total']),
                                    "foreignCurrency": "",
                                    "countryCode": "",
                                    "invValueFc": "",
                                    "invPeriodStartDate": "",
                                    "invPeriodEndDate": "",
                                    "accDetail": "", #"2550326",
                                    "division": str(details['bill']['branch_name']),
                                    "profitCentre1": "",
                                    "tdsFlag": tdsFlag,
                                    "lineItems": []
                                    }
                            bill["lineItems"] = line_items
                            bills["req"].append(bill)
                            print("bills" + str(bills))
                        except Exception as e:
                            lw.logRecord("Error in bulkbill for loop: " + str(e))
                            print(str(e))
                    print("bills:" + str(bills))
                    
                    # cc.bulkBills_DN(bills)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in bulkInvoice: " + str(e))

    @staticmethod
    def bulkVendorCredit():
        """Fetch Bills and format response"""
        try:
            has_more_page = True
            page = 1
            vendorcredits = {"req": []}
            while (has_more_page == True):
                data = ZohoModel.fetch_dn(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "vendor_credits" in data and data["vendor_credits"]:
                    for idx, item in enumerate(data['vendor_credits'], start=1):
                        try:
                            # if item['entity_type'] == "bill":
                            # print(str(item['bill_id']))
                            details = ZohoModel.fetch_dn_details(str(item['vendor_credit_id']))
                            print(details['vendor_credit']['total'])
                            custdetails = sd.organization_address[str(details['vendor_credit']['branch_name'])]
                            reverse = 'N'
                            print(details['vendor_credit']['is_reverse_charge_applied'])
                            print(type(details['vendor_credit']['is_reverse_charge_applied']))
                            if (details['vendor_credit']['is_reverse_charge_applied'] != False):
                                reverse = 'Y'
                            # is_tax_line = details['vendor_credit']['is_item_level_tax_calc']
                            supgstin = "URP"
                            suppin = "999999"
                            supStateCode = "96"
                            print(details['vendor_credit']['gst_no'])
                            if details['vendor_credit']['gst_no'] != "":
                                supgstin = details['vendor_credit']['gst_no']
                                supStateCode = supgstin[:2]
                                suppin = details['vendor_credit']['billing_address']['zip']
                            line_items = ZohoController.create_line_items(details['vendor_credit']['line_items'], reverse, supgstin)
                            formatted_date = (datetime.strptime(str(details['vendor_credit']['date']), "%Y-%m-%d"))
                            date = formatted_date.strftime("%d/%m/%Y")
                            return_period = formatted_date.strftime("%m%Y")
                            crDrPreGst = "Y"
                            igstRt = cgstRt = igstAmt = cgstAmt = 0
                            sup_type = "TAX"
                            tdsFlag = "N"
                            try:
                                if float(details['vendor_credit']['tds_percent']) > 0.0:
                                    tdsFlag = 'Y'
                            except Exception as e:
                                print(str(e))
                            # if str(details['vendor_credit']['gst_treatment']) == "overseas":
                            #     if float(details['vendor_credit']['tax_total']) >0.0:
                            #         sup_type = "TAX"
                            #     else:
                            #         sup_type = "TAX"
                            # elif str(details['vendor_credit']['gst_treatment']) == "business_gst":
                            #     sup_type = "TAX"
                            # elif str(details['vendor_credit']['gst_treatment']) == "business_sez":
                            #     if float(details['vendor_credit']['tax_total']) >0.0:
                            #         sup_type = "TAX"
                            #     else:
                            #         sup_type = "TAX"
                            try:
                                if reverse == 'N':
                                    # if (float(details['vendor_credit']['tax_percentage']) > 0.0):
                                        # if is_tax_line == True:
                                    taxtype = ''.join([c for c in str(details['vendor_credit']['taxes'][0]['tax_name']) if c.isalpha()])
                                    if taxtype == 'IGST' or taxtype == 'igst':
                                        igstRt = ''.join([c for c in str(details['vendor_credit']['taxes'][0]['tax_name']) if c.isdigit()])
                                        igstAmt = details['vendor_credit']['taxes'][0]['tax_amount']
                                    elif (taxtype == 'CGST' or taxtype == 'cgst') or (taxtype == 'SGST' or taxtype == 'sgst'):
                                        cgstRt = ''.join([c for c in str(details['vendor_credit']['taxes'][0]['tax_name']) if c.isdigit()])
                                        cgstAmt = details['vendor_credit']['taxes'][0]['tax_amount']
                                else:
                                    taxtype = ''.join([c for c in str(details['vendor_credit']['reverse_charge_vat_summary'][0]['tax_name']) if c.isalpha()])
                                    if taxtype == 'IGST' or taxtype == 'igst':
                                        igstRt = ''.join([c for c in str(details['vendor_credit']['reverse_charge_vat_summary'][0]['tax_name']) if c.isdigit()])
                                        igstAmt = details['vendor_credit']['reverse_charge_vat_summary'][0]['tax_amount']
                                    elif (taxtype == 'CGST' or taxtype == 'cgst') or (taxtype == 'SGST' or taxtype == 'sgst'):
                                        cgstRt = ''.join([c for c in str(details['vendor_credit']['taxes'][0]['reverse_charge_vat_summary']) if c.isdigit()])
                                        cgstAmt = details['vendor_credit']['reverse_charge_vat_summary'][0]['tax_amount']
                            except Exception as e:
                                print(str(e))
                            # custGstin = sd.organization_gst.get(str(details['vendor_credit']['branch_name']))
                            vendorcredit = {
                            # Optional
                            "srcFileName": "Standard",
                            "srcIdentifier": "Zoho",
                            "returnPeriod": str(return_period),
                            "suppGstin": str(supgstin),
                            "docType": "DR",
                            "docNo": str(details['vendor_credit']['bill_number']),
                            "docDate": str(date),
                            "orgDocType": str(details['vendor_credit']['reference_number']),
                            "crDrPreGst": crDrPreGst,
                            "custGstin": str(custdetails['gstin']),
                            "supType": str(sup_type),
                            "diffPercent": "",
                            "orgSgstin": "",
                            "custOrSupName": "",
                            "supCode": str(suppin),
                            "custOrSupAddr1": str(custdetails['address_line1']),
                            "custOrSupAddr2": str(custdetails['address_line2']),
                            "custOrSupAddr4": str(custdetails['city']),
                            "billToState": str(custdetails['state']),
                            "shipToState": str(custdetails['state']),
                            "pos": str((custdetails['gstin'])[:2]),
                            "stateApplyingCess": "",
                            "portCode": "",
                            "billOfEntry": "",
                            "billOfEntryDate": "",
                            "reverseCharge": str(reverse),
                            "accVoucherNo": "", #"202502011001321",
                            "accVoucherDate": "", #"2025-10-07",
                            "taxScheme": "",
                            "docCat": "",
                            "supTradeName": str(details['vendor_credit']['vendor_name']),
                            "supLegalName": str(details['vendor_credit']['vendor_name']),
                            "supBuildingNo": str(details['vendor_credit']['billing_address']['address']),
                            "supBuildingName": "",
                            "supLocation": "",
                            "supPincode": str(suppin),
                            "supStateCode": str(supStateCode),
                            "supPhone": "",
                            "supEmail": "",
                            "custTradeName": "",
                            "custPincode": "",
                            "custPhone": "",
                            "custEmail": "",
                            "shipToGstin": "",
                            "shipToTradeName": "",
                            "shipToLegalName": "",
                            "shipToBuildingNo": "",
                            "shipToBuildingName": "",
                            "shipToLocation": "",
                            "shipToPincode": "",
                            "invOtherCharges": "",
                            "invAssessableAmt": str(details['vendor_credit']['sub_total']),
                            "invIgstAmt": str(igstAmt),
                            "invCgstAmt": str(cgstAmt),
                            "invSgstAmt": str(cgstAmt),
                            "invCessAdvaloremAmt": "",
                            "roundOff": "",
                            "exchangeRt": details['vendor_credit']['exchange_rate'],
                            "totalInvValueInWords": "", #str(details['vendor_credit']['sub_total']),
                            "foreignCurrency": "",
                            "countryCode": "",
                            "invValueFc": "",
                            "invPeriodStartDate": "",
                            "invPeriodEndDate": "",
                            "accDetail": "", #"2550326",
                            "division": str(details['vendor_credit']['branch_name']),
                            "profitCentre1": "",
                            "tdsFlag": tdsFlag,
                            "lineItems": []
                            }
                            vendorcredit["lineItems"] = line_items
                            vendorcredits["req"].append(vendorcredit)
                            print("vendorcredits" + str(vendorcredits))
                        except Exception as e:
                            lw.logRecord("Error in bulkbill for loop: " + str(e))
                            print(str(e))
                    print("vendorcredits:" + str(vendorcredits))
                    
                    # cc.bulkBills_DN(vendorcredits)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in bulkInvoice: " + str(e))
    @staticmethod
    def bulkExpense():
        """Fetch Expense and format response"""
        try:
            has_more_page = True
            page = 1
            expenses = {"req": []}
            while (has_more_page == True):
                data = ZohoModel.fetch_expense(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "expenses" in data and data["expenses"]:
                    for idx, item in enumerate(data['expenses'], start=1):
                        try:
                            if item['entity_type'] == "expenses":
                                
                                # print(str(item['expenses_id']))
                                details = ZohoModel.fetch_expense_details(str(item['expense_id']))
                                print(details['expenses']['total'])
                                reverse = 'N'
                                line_items = ZohoController.create_line_items(details['expenses']['line_items'])
                                # print(details['expense']['is_reverse_charge_applied'])
                                if details['expense']['is_reverse_charge_applied'] != 'false' or details['expense']['is_reverse_charge_applied'] == False:
                                    reverse = 'Y'
                                companyCode = ''
                                ref1 = ''
                                ref2 = ''
                                for cust in details['expense']['custom_fields']:
                                    # if cust['expense']['label'] == 'Company Id':
                                    #     companyCode = cust['value']
                                    if cust['label'] == 'Customer Invoice Ref':
                                        ref1 = cust['value']
                                    elif cust['label'] == 'Vendor Invoice Date':
                                        inv_date = cust['value']
                                    elif cust['label'] == 'Invoice Acceptance Date':
                                        acp_date = cust['value']
                                
                                # for ref in details['salesorders']:
                                #     if ref['salesorder_number'] == details['reference_number']:
                                #         # ref1 = ref['reference_number']
                                #         ref2 = ref['shipment_date']
                                date =datetime.strptime(str(details['expense']['date']), "%d-%m-%Y") 
                                return_period = date.strftime("%m%Y")
                                crDrPreGst = ""
                                # year = ZohoController.get_fiscal_year(date)
                                if details['expense']['date'] == False:
                                    crDrPreGst = "N"
                                else:
                                    crDrPreGst = "Y"
                                igstRt = cgstRt = igstAmt = cgstAmt = 0
                                taxtype = ''.join([c for c in str(details['expense']['taxes'][0]['tax_name']) if c.isalpha()])
                                if taxtype == 'IGST' or taxtype == 'igst':
                                    igstRt = ''.join([c for c in str(details['expense']['taxes'][0]['tax_name']) if c.isdigit()])
                                    igstAmt = details['expense']['taxes'][0]['tax_amount']
                                elif (taxtype == 'CGST' or taxtype == 'cgst') or (taxtype == 'sGST' or taxtype == 'sgst'):
                                    cgstRt = ''.join([c for c in str(details['expense']['taxes'][0]['tax_name']) if c.isdigit()])
                                    cgstAmt = details['expense']['taxes'][0]['tax_amount']
                                custGstin = sd.organization_gst.get(str(details['expense']['branch_name']))
                                expense = {
                                    # Optional
                                    "taxScheme": "GST",
                                    # "supTradeName": str(details['expense']['vendor_name']),
                                    # "supLegalName": str(details['expense']['vendor_name']),
                                    # "supBuildingNo": str(details['expense']['expenseing_address']['address']),
                                    # "supBuildingName": str(details['expense']['date']),
                                    # "supLocation": str(details['expense']['date']),
                                    # "supPincode": str(details['expense']['date']),
                                    # "supStateCode": str(details['expense']['date']),
                                    # "supPhone": str(details['expense']['date']),
                                    # "supEmail": str(details['expense']['date']),
                                    # "custTradeName": str(details['expense']['date']),
                                    # "custOrSupName": str(details['expense']['date']),
                                    # "custOrSupAddr1": str(details['expense']['date']),
                                    # "custOrSupAddr2": str(details['expense']['date']),
                                    # "custOrSupAddr4": str(details['expense']['date']),
                                    # "custPincode": str(details['expense']['date']),
                                    # "expenseToState": str(details['expense']['date']),
                                    # "custPhone": str(details['expense']['date']),
                                    # "custEmail": str(details['expense']['date']),
                                    # "invOtherCharges": str(details['expense']['date']),
                                    # "invCessSpecificAmt": str(details['expense']['date']),
                                    # "invStateCessAmt": str(details['expense']['date']),
                                    "roundOff": str(details['expense']['roundoff_value']),
                                    # "totalInvValueInWords": "abc",
                                    # "tcsFlagIncomeTax": "trt",
                                    "foreignCurrency": "a",##########################################
                                    "countryCode": "12",################################################################
                                    # "invValueFc": "10.1",
                                    # "invPeriodStartDate": "09/03/2020",
                                    # "invPeriodEndDate": "09/03/2020",
                                    # "payeeName": "divya",
                                    # "modeOfPayment": "a",
                                    # "branchOrIfscCode": "abced",
                                    # "paymentTerms": "abcde",
                                    # "paymentInstruction": "intrcustion",
                                    # "creditTransfer": "anc",
                                    # "directDebit": "direct",
                                    # "creditDays": 1,
                                    # "paymentDueDate": "09/03/2020",
                                    # "accDetail": "abcde",
                                    # "orgDocType": "inv",
                                    # "supCode": "RL&S",
                                    # "exchangeRt": 0,
                                    # "tcsFlag": "N",
                                    # "tdsFlag": "N",
                                    # "userId": "P0002",
                                    # "companyCode": "a",
                                    # "glCodeIgst": "GL002",
                                    # "glCodeCgst": "GL003",
                                    # "glCodeSgst": "GL004",
                                    # "glCodeAdvCess": "GL005",
                                    # "glCodeSpCess": "GL006",
                                    # "glCodeStateCess": "glCodeStateCess",
                                    # "glStateCessSpecific": "kgf",
                                    # Mandatory
                                    "docType": "INV",
                                    "docNo": str(details['expense']['expense_number']),
                                    "docDate": str(date),
                                    "custGstin": custGstin,
                                    "pos": str(custGstin[:2]),
                                    "returnPeriod": str(return_period),
                                    "supType ": str(details['expense']['']),######################
                                    # Conditional Mandatory
                                    "reverseCharge": str(reverse),
                                    "suppGstin": str(details['expense']['gst_no']),
                                    "invAssessableAmt": str(details['expense']['sub_total']),
                                    "invIgstAmt": str(igstAmt),
                                    "invCgstAmt": str(cgstAmt),
                                    "invSgstAmt": str(cgstAmt),
                                    # "invCessAdvaloremAmt": str(details['expense']['date']),
                                    # "invCessSpecificAmt": str(details['expense']['date']),
                                    # "portCode": str(details['expense']['date']),
                                    # "expenseOfEntry": str(details['expense']['date']),
                                    # "expenseOfEntryDate": str(details['expense']['date']),
                                    # "diffPercent": str(details['expense']['date']),
                                    # "sec7OfIgstFlag": str(details['expense']['date']),
                                    # "claimRefundFlag": str(details['expense']['date']),
                                    # "autoPopToRefundFlag": str(details['expense']['date']),
                                    "lineItems": []
                                    }
                                expense["lineItems"].append(line_items)
                                expenses["req"].append(expense)
                        except Exception as e:
                            lw.logRecord("Error in bulkInvoice for loop: " + str(e))
                    # print("Invoices" + str(invoices))
                    
                    cc.bulkInvoices(expenses)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in bulkInvoice: " + str(e))



    @staticmethod
    def bulkInvoice():
        """Fetch invoice and format response"""
        try:
            has_more_page = True
            page = 1
            invoices = {"req": []}
            while (has_more_page == True):
                data = ZohoModel.fetch_invoice(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "invoices" in data and data["invoices"]:
                    for idx, item in enumerate(data['invoices'], start=1):
                        try:
                            # if item['entity_type'] == "invoices":
                                
                            # print(str(item['invoices_id']))
                            details = ZohoModel.fetch_invoice_details(str(item['invoice_id']))
                            print(details['invoice']['total'])
                            reverse = 'N'
                            try:
                                if details['invoice']['is_reverse_charge_applied'] == False:
                                    reverse = 'Y'
                            except:
                                pass
                            custGstin = "URP"
                            custpin = "999999"
                            custStateCode = "96"
                            print(details['invoice']['gst_no'])
                            if details['invoice']['gst_no'] != "":
                                custGstin = details['invoice']['gst_no']
                                custStateCode = custGstin[:2]
                                custpin = details['invoice']['billing_address']['zip']
                            line_items = ZohoController.create_line_items_sales(details['invoice']['line_items'], reverse, custGstin)
                            # print(details['invoice']['is_reverse_charge_applied'])

                            formatted_date = (datetime.strptime(str(details['invoice']['date']), "%Y-%m-%d"))
                            date = formatted_date.strftime("%d/%m/%Y")
                            print(date)
                            return_period = formatted_date.strftime("%m%Y")
                            crDrPreGst = "N"
                            sup_type = "TAX"
                            tdsFlag = "N"
                            try:
                                if float(details['invoice']['tds_percent']) > 0.0:
                                    tdsFlag = 'Y'
                            except Exception as e:
                                print(str(e))
                            # year = ZohoController.get_fiscal_year(date)
                            if str(details['invoice']['gst_treatment']) == "overseas":
                                if float(details['invoice']['tax_total']) >0.0:
                                    sup_type = "EXPT"
                                else:
                                    sup_type = "EXPWT"
                            elif str(details['invoice']['gst_treatment']) == "business_gst":
                                sup_type = "TAX"
                            elif str(details['invoice']['gst_treatment']) == "business_sez":
                                if float(details['invoice']['tax_total']) >0.0:
                                    sup_type = "SEZWP"
                                else:
                                    sup_type = "SEZWOP"
                            
                            igstRt = cgstRt = igstAmt = cgstAmt = 0
                            taxtype = ''.join([c for c in str(details['invoice']['taxes'][0]['tax_name']) if c.isalpha()])
                            if taxtype == 'IGST' or taxtype == 'igst':
                                igstRt = ''.join([c for c in str(details['invoice']['taxes'][0]['tax_name']) if c.isdigit()])
                                igstAmt = details['invoice']['taxes'][0]['tax_amount']
                            elif (taxtype == 'CGST' or taxtype == 'cgst') or (taxtype == 'sGST' or taxtype == 'sgst'):
                                cgstRt = ''.join([c for c in str(details['invoice']['taxes'][0]['tax_name']) if c.isdigit()])
                                cgstAmt = details['invoice']['taxes'][0]['tax_amount']
                            # custGstin = sd.organization_gst.get(str(details['invoice']['branch_name']))
                            supdetails = sd.organization_address[str(details['invoice']['branch_name'])]
                            supgstin = supdetails['gstin']
                            invoice = {
                                # Optional
                                    "srcFileName": "Standard",
                                    "srcIdentifier": "Zoho",
                                    "returnPeriod": str(return_period),
                                    "suppGstin": str(supgstin),
                                    "docType": "INV",
                                    "docNo": str(details['invoice']['invoice_number']),
                                    "docDate": str(date),
                                    "orgDocType": "",
                                    "crDrPreGst": crDrPreGst,
                                    "custGstin": str(custGstin),
                                    "supType": str(sup_type),
                                    "diffPercent": "",
                                    "orgSgstin": "",
                                    "custOrSupName": "",
                                    "supCode": str(custpin),
                                    "custOrSupAddr1": str(details['invoice']['billing_address']['street']),
                                    "custOrSupAddr2": str(details['invoice']['billing_address']['address']),
                                    "custOrSupAddr4": str(details['invoice']['billing_address']['street2']),
                                    "billToState": str(details['invoice']['billing_address']['state']),
                                    "shipToState": str(details['invoice']['shipping_address']['state']),
                                    "pos": str(custStateCode),
                                    "stateApplyingCess": "",
                                    "portCode": "",
                                    "billOfEntry": "",
                                    "billOfEntryDate": "",
                                    "reverseCharge": str(reverse),
                                    "accVoucherNo": "", #"202502011001321",
                                    "accVoucherDate": "", #"2025-10-07",
                                    "taxScheme": "",
                                    "docCat": "",
                                    "supTradeName": str("Vestian"),
                                    "supLegalName": str("Vestian"),
                                    "supBuildingNo": str(supdetails['address_line1']),
                                    "supBuildingName": str(supdetails['address_line1']),
                                    "supLocation": str(supdetails['address_line2']),
                                    "supPincode": str(supdetails['pincode']),
                                    "supStateCode": str(supgstin[:2]),
                                    "supPhone": str(supdetails['phone']),
                                    "supEmail": str(supdetails['email']),
                                    "custTradeName": str(details['invoice']['customer_name']),
                                    "custPincode": "",
                                    "custPhone": "",
                                    "custEmail": "",
                                    "shipToGstin": "",
                                    "shipToTradeName": "",
                                    "shipToLegalName": "",
                                    "shipToBuildingNo": "",
                                    "shipToBuildingName": "",
                                    "shipToLocation": "",
                                    "shipToPincode": "",
                                    "invOtherCharges": "",
                                    "invAssessableAmt": str(details['invoice']['sub_total']),
                                    "invIgstAmt": str(igstAmt),
                                    "invCgstAmt": str(cgstAmt),
                                    "invSgstAmt": str(cgstAmt),
                                    "invCessAdvaloremAmt": "",
                                    "roundOff": "",
                                    "exchangeRt": details['invoice']['exchange_rate'],
                                    "totalInvValueInWords": "", #str(details['invoice']['sub_total']),
                                    "foreignCurrency": "",
                                    "countryCode": "",
                                    "invValueFc": "",
                                    "invPeriodStartDate": "",
                                    "invPeriodEndDate": "",
                                    "accDetail": "", #"2550326",
                                    "division": str(details['invoice']['branch_name']),
                                    "profitCentre1": "",
                                    "tdsFlag": tdsFlag,
                                    "lineItems": []
                                }
                            # invoice["lineItems"].append(line_items)
                            invoice["lineItems"] = line_items
                            invoices["req"].append(invoice)
                        except Exception as e:
                            lw.logRecord("Error in bulkInvoice for loop: " + str(e))
                        
                    print("Invoices" + str(invoices))
                    # cc.bulkInvoices_CN(invoices)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in bulkInvoice: " + str(e))

    @staticmethod
    def bulkCreditNote():
        """Fetch contacts and format response"""
        try:
            has_more_page = True
            page = 1
            credit_notes = {"req": []}
            while (has_more_page == True):
                try:
                    data = ZohoModel.fetch_cn(page)
                    page += 1

                    if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                        has_more_page = False
                    
                    if "creditnotes" in data and data["creditnotes"]:
                        for idx, item in enumerate(data['creditnotes'], start=1):
                        
                            try:                                    
                                # print(str(item['invoices_id']))
                                details = ZohoModel.fetch_cn_details(str(item['creditnote_id']))
                                print(details['creditnote']['total'])
                                reverse = 'N'
                                try:
                                    if details['creditnote']['is_reverse_charge_applied'] == False:
                                        reverse = 'Y'
                                except:
                                    pass
                                custGstin = "URP"
                                custpin = "999999"
                                custStateCode = "96"
                                print(details['creditnote']['gst_no'])
                                if details['creditnote']['gst_no'] != "":
                                    custGstin = details['creditnote']['gst_no']
                                    custStateCode = custGstin[:2]
                                    custpin = details['creditnote']['billing_address']['zip']
                                line_items = ZohoController.create_line_items_sales(details['creditnote']['line_items'], reverse, custGstin)
                                # print(details['creditnote']['is_reverse_charge_applied'])

                                formatted_date = (datetime.strptime(str(details['creditnote']['date']), "%Y-%m-%d"))
                                date = formatted_date.strftime("%d/%m/%Y")
                                print(date)
                                return_period = formatted_date.strftime("%m%Y")
                                crDrPreGst = "N"
                                sup_type = "TAX"
                                tdsFlag = "N"
                                try:
                                    if float(details['creditnote']['tds_percent']) > 0.0:
                                        tdsFlag = 'Y'
                                except Exception as e:
                                    print(str(e))
                                # year = ZohoController.get_fiscal_year(date)
                                if str(details['creditnote']['gst_treatment']) == "overseas":
                                    if float(details['creditnote']['tax_total']) >0.0:
                                        sup_type = "EXPT"
                                    else:
                                        sup_type = "EXPWT"
                                elif str(details['creditnote']['gst_treatment']) == "business_gst":
                                    sup_type = "TAX"
                                elif str(details['creditnote']['gst_treatment']) == "business_sez":
                                    if float(details['creditnote']['tax_total']) >0.0:
                                        sup_type = "SEZWP"
                                    else:
                                        sup_type = "SEZWOP"
                                
                                igstRt = cgstRt = igstAmt = cgstAmt = 0
                                taxtype = ''.join([c for c in str(details['creditnote']['taxes'][0]['tax_name']) if c.isalpha()])
                                if taxtype == 'IGST' or taxtype == 'igst':
                                    igstRt = ''.join([c for c in str(details['creditnote']['taxes'][0]['tax_name']) if c.isdigit()])
                                    igstAmt = details['creditnote']['taxes'][0]['tax_amount']
                                elif (taxtype == 'CGST' or taxtype == 'cgst') or (taxtype == 'sGST' or taxtype == 'sgst'):
                                    cgstRt = ''.join([c for c in str(details['creditnote']['taxes'][0]['tax_name']) if c.isdigit()])
                                    cgstAmt = details['creditnote']['taxes'][0]['tax_amount']
                                # custGstin = sd.organization_gst.get(str(details['creditnote']['branch_name']))
                                supdetails = sd.organization_address[str(details['creditnote']['branch_name'])]
                                supgstin = supdetails['gstin']
                                credit_note = {
                                    # Optional
                                        "srcFileName": "Standard",
                                        "srcIdentifier": "Zoho",
                                        "returnPeriod": str(return_period),
                                        "suppGstin": str(supgstin),
                                        "docType": "INV",
                                        "docNo": str(details['creditnote']['invoice_number']),
                                        "docDate": str(date),
                                        "orgDocType": "",
                                        "crDrPreGst": crDrPreGst,
                                        "custGstin": str(custGstin),
                                        "supType": str(sup_type),
                                        "diffPercent": "",
                                        "orgSgstin": "",
                                        "custOrSupName": "",
                                        "supCode": str(custpin),
                                        "custOrSupAddr1": str(details['creditnote']['billing_address']['street']),
                                        "custOrSupAddr2": str(details['creditnote']['billing_address']['address']),
                                        "custOrSupAddr4": str(details['creditnote']['billing_address']['street2']),
                                        "billToState": str(details['creditnote']['billing_address']['state']),
                                        "shipToState": str(details['creditnote']['shipping_address']['state']),
                                        "pos": str(custStateCode),
                                        "stateApplyingCess": "",
                                        "portCode": "",
                                        "billOfEntry": "",
                                        "billOfEntryDate": "",
                                        "reverseCharge": str(reverse),
                                        "accVoucherNo": "", #"202502011001321",
                                        "accVoucherDate": "", #"2025-10-07",
                                        "taxScheme": "",
                                        "docCat": "",
                                        "supTradeName": str("Vestian"),
                                        "supLegalName": str("Vestian"),
                                        "supBuildingNo": str(supdetails['address_line1']),
                                        "supBuildingName": str(supdetails['address_line1']),
                                        "supLocation": str(supdetails['address_line2']),
                                        "supPincode": str(supdetails['pincode']),
                                        "supStateCode": str(supgstin[:2]),
                                        "supPhone": str(supdetails['phone']),
                                        "supEmail": str(supdetails['email']),
                                        "custTradeName": str(details['creditnote']['customer_name']),
                                        "custPincode": "",
                                        "custPhone": "",
                                        "custEmail": "",
                                        "shipToGstin": "",
                                        "shipToTradeName": "",
                                        "shipToLegalName": "",
                                        "shipToBuildingNo": "",
                                        "shipToBuildingName": "",
                                        "shipToLocation": "",
                                        "shipToPincode": "",
                                        "invOtherCharges": "",
                                        "invAssessableAmt": str(details['creditnote']['sub_total']),
                                        "invIgstAmt": str(igstAmt),
                                        "invCgstAmt": str(cgstAmt),
                                        "invSgstAmt": str(cgstAmt),
                                        "invCessAdvaloremAmt": "",
                                        "roundOff": "",
                                        "exchangeRt": details['creditnote']['exchange_rate'],
                                        "totalInvValueInWords": "", #str(details['creditnote']['sub_total']),
                                        "foreignCurrency": "",
                                        "countryCode": "",
                                        "invValueFc": "",
                                        "invPeriodStartDate": "",
                                        "invPeriodEndDate": "",
                                        "accDetail": "", #"2550326",
                                        "division": str(details['creditnote']['branch_name']),
                                        "profitCentre1": "",
                                        "tdsFlag": tdsFlag,
                                        "lineItems": []
                                    }
                                # invoice["lineItems"].append(line_items)
                                credit_note["lineItems"] = line_items
                                credit_notes["req"].append(credit_note)
                            except Exception as e:
                                lw.logRecord("Error in bulkInvoice for loop: " + str(e))
                        print("CN: " + str(credit_notes))
                        # cc.creditDebitNote(credit_notes)
                except Exception as e:
                    lw.logRecord("Error in creditDebitNote for CN: " + str(e))
        except Exception as e:
            lw.logRecord("Error in fetch_contacts: " + str(e))

    # @staticmethod
    # def payments():
    #     """Fetch Invoice and format response"""
    #     try:
    #         has_more_page = True
    #         page = 1
    #         # payments = []
    #         while (has_more_page == True):
    #             payments = []
    #             data = ZohoModel.fetch_payments(page)
    #             page += 1

    #             if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
    #                 has_more_page = False

    #             if "vendorpayments" in data and data["vendorpayments"]:
    #                 for idx, item in enumerate(data['vendorpayments'], start=1):
    #                     try:
    #                         details = ZohoModel.fetch_payments_details(str(item['payment_id']))
    #                         # msme_data = details['invoices']['msme_type']
    #                         reverse = 'N'
    #                         if details['vendorpayment']['is_reverse_charge_applied'] != 'false' or details['vendorpayment']['is_reverse_charge_applied'] == False:
    #                             reverse = 'Y'
    #                         companyCode = ''
    #                         ref1 = ''
    #                         ref2 = ''
    #                         # for cust in details['custom_fields']:
    #                         #     if cust['label'] == 'Company Id':
    #                         #         companyCode = cust['value']
    #                         #     elif cust['label'] == 'Customer Invoice Ref':
    #                         #         ref1 = cust['value']
                            
    #                         # for ref in details['salesorders']:
    #                         #     if ref['salesorder_number'] == details['reference_number']:
    #                         #         # ref1 = ref['reference_number']
    #                         #         ref2 = ref['shipment_date']
    #                         date =datetime.strptime(str(details['vendorpayment']['date']), "%Y-%m-%d") 
    #                         year = ZohoController.get_fiscal_year(date)
    #                         payment = {
    #                             "vendorId": details['vendorpayment']['vendor_id'],
    #                             "vendorName": details['vendorpayment']['vendor_name'],
    #                             "plantLocation": details['vendorpayment']['destination_of_supply'],
    #                             # "bookNumber": "", #details['vendorpayment']['reference_number'],
    #                             "paymentsNumber": details['vendorpayment']['payment_number'],
    #                             "internalInvoiceNumber": details['vendorpayment']['bills'][0]['bill_id'],
    #                             "vendorInvoiceNumber": details['vendorpayment']['bills'][0]['bill_number'],
    #                             "paymentType": "PAY",
    #                             "paymentDate": datetime.strptime((details['vendorpayment']['date']), '%Y-%m-%d').strftime('%d-%m-%Y'), #details['vendorpayment']['total'],
    #                             "invoiceAmount": details['vendorpayment']['amount'],
    #                             "paymentAmount": details['vendorpayment']['total_payment_amount'],
    #                             "fiscalYear": year,        
    #                             # "companyCode": companyCode, #details['vendorpayment']['customer_custom_fields'],
    #                             "currency":details['vendorpayment']['currency_code']                                   
    #                             }
    #                         payments.append(payment)
    #                     except Exception as e:
    #                         lw.logRecord("Error in payments for loop: " + str(e))
    #                 # print("Invoices" + str(payments))
                    
    #                 cc.payments(payments)
    #             pass
    #         # return payment
    #     except Exception as e:
    #         lw.logRecord("Error in payments: " + str(e))

    @staticmethod
    def update_invoice(trns_id, vend_id, int_inv_no, ven_int_no, dis_amt, dis_date, mat_date):
        try:
            for t, v, i, vi, da, dd, md in zip_longest(trns_id, vend_id, int_inv_no, ven_int_no, dis_amt, dis_date, mat_date, fillvalue="NA"):
                data = ZohoModel.fetch_bill_details(i)
                # print(data)
                cc.update_invoice(data['bill'], t, v, i, vi, da, dd, md)
        except Exception as e:
            lw.logRecord("Error in update_invoice: " + str(e))

    @staticmethod
    def create_all_vendor_credit(trns_id, vend_id, vend_nm, int_inv_no, ven_int_no, dis_amt, dis_date, mat_date):
        try:
            for t, v, vn, i, vi, da, dd, md in zip_longest(trns_id, vend_id, vend_nm, int_inv_no, ven_int_no, dis_amt, dis_date, mat_date, fillvalue="NA"):
                details = ZohoModel.fetch_bill_details(str(i))
                print(details)
                print(details['bill']['total'])
                body = {
                    "vendor_id": str(v),
                    "vendor_name": str(vn),
                    "bill_id": str(i),
                    "bill_number": str(vi),
                    "date": str(dd),
                    "line_items": []
                }
                discount_rate = round((float(details['bill']['discount_amount'])/float(details['bill']['total'])),3)
                rate = round((float(da)/ (float(details['bill']['total']))),3) #-details['bill']['discount_amount'])
                print(str(rate))
                for item in details['bill']['line_items']:
                    print(float(item['item_total']))
                    print(round((float(item['item_total'])*discount_rate),2))
                    print(round((float(item['item_total'])*discount_rate),2) * rate)
                    amt = round(((float(item['item_total']) - round((float(item['item_total'])*discount_rate),2)) * rate),3)
                    print(amt)
                    line_items = {
                                "item_id": item['item_id'],
                                "account_id": item['account_id'],
                                "name": item['name'],
                                "description": item['description'],
                                "rate": amt,
                                "quantity": item['quantity'],
                                "item_type": item['item_type'],
                            }
                    body["line_items"].append(line_items)
                print(body)
                data = ZohoModel.create_vendor_credit(body)
                if data['message'] == 'Vendor credit has been created.':
                    body_bills = {
                                    "bills": [
                                        {
                                            "bill_id": str(i),
                                            "amount_applied": float(da)
                                        }
                                    ]
                                }
                    data_bills = ZohoModel.apply_to_bills(str(data['vendor_credit']['vendor_credit_id']), body_bills)
                    if data_bills['message'] == 'Credits have been applied to the bill(s).':
                        lw.logBackUpRecord("Credit has been applied successfullly for bill: " + str(vi))
                        body_pay = {
                                    "vendor_id": str(v),
                                    "bills": [
                                        {
                                            "bill_id": str(i),
                                            "amount_applied": float(details['bill']['total']) - float(da)
                                        }
                                    ],
                                    "date": str(dd),
                                    "amount": float(details['bill']['total']) - float(da)
                                }
                        print(body_pay)
                        data_pay = ZohoModel.create_paymets(body_pay)
                        print(data_pay)
                        if data_pay['message'] == 'The payment made to the vendor has been recorded':
                            lw.logBackUpRecord("Payment has been created successfullly for bill: " + str(vi))
                            cc.postingAck(t, v, i, vi)
                        else: 
                            lw.logRecord("Error while creating payments for bill: " + str(vi))

                    else: 
                        lw.logRecord("Error while applying credit for bill: " + str(vi))
                else:
                    lw.logRecord("Error while creating vendor credit for: " + str(vi))
                # print(data)
                # cc.update_invoice(data['bill'], t, v, i, vi, da, dd, md)
        except Exception as e:
            print("Error in update_invoice: " + str(e))
            lw.logRecord("Error in update_invoice: " + str(e))