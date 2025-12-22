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
    def create_line_items(items, reverse, gstin, customer_type):
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
            # if str(gstin) == 'URP':
            #     supplytype = 'IMP'
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
            if str(gstin) == '' and customer_type == 'overseas':
                if (service == 'Y'):
                    supplytype = 'IMPS'
                else:
                    supplytype = 'IMPG'
            
            if (data['itc_eligibility'] == 'eligible') and (float(igstAmt)> 0.0 or float(cgstAmt)> 0.0):
                if (service == 'Y'):
                    eligIndicator = "IS"
                else:
                    eligIndicator = "IG"
            else:
                    eligIndicator = "NO"
            if eligIndicator != "NO":
                avail_igst = igstAmt
                avail_cgst = cgstAmt
            if str(data['itc_eligibility']) == 'eligible' and (float(igstAmt)> 0.0 or float(cgstAmt)> 0.0):
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
                "isService" : str(service),
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
                            if (data['line_item_taxes'][0]['tax_amount'] > 0):
                                supplytype = "TAX"
                        except:
                            try:
                                if data['line_item_taxes'][0]['tax_name'][:4] == 'IGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'igst':
                                    igstRt = data['line_item_taxes'][0]['tax_name'][4:6]
                                    igstAmt = data['line_item_taxes'][0]['tax_amount']
                                elif (data['line_item_taxes'][0]['tax_name'][:4] == 'CGST' or data['line_item_taxes'][0]['tax_name'][:4] == 'cgst') or (data['line_item_taxes'][0]['tax_specific_type'] == 'sGST' or data['line_item_taxes'][0]['tax_specific_type'] == 'sgst'):
                                    cgstRt = (data['line_item_taxes'][0]['tax_name'][4:6]).replace(" ","")
                                    cgstAmt = data['line_item_taxes'][0]['tax_amount']
                                if (data['line_item_taxes'][0]['tax_amount'] > 0):
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
                            if (data['line_item_taxes'][0]['tax_amount'] > 0):
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
                        if (data['line_item_taxes'][0]['tax_amount'] > 0):
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
                            if (data['line_item_taxes'][0]['tax_amount'] > 0):
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
                # eligIndicator = itc = ""
                # if str(gstin) == 'URP':
                #     if (float(igstAmt) > 0.0) and (float(cgstAmt) > 0.0):
                #         supplytype = 'EXPT'
                #     else:
                #         supplytype = 'EXPWT'
                # try:
                #     if (data['itc_eligibility'] == 'eligible') and (float(igstAmt)> 0.0 or float(cgstAmt)> 0.0):
                #         if (service == 'Y'):
                #             eligIndicator = "IS"
                #         else:
                #             eligIndicator = "IG"
                #     # if (float(igstAmt) <= 0.0) and (float(cgstAmt) <= 0.0):
                #     else:
                #         eligIndicator = "NO"
                # except:
                #     pass
                # if eligIndicator != "NO":
                #     avail_igst = igstAmt
                #     avail_cgst = cgstAmt
                # try:
                #     if str(data['itc_eligibility']) == 'eligible' and (float(igstAmt)> 0.0 or float(cgstAmt)> 0.0):
                #         itc = 'Y'
                # except:
                #     pass
                lineitems = {
                    # Optional
                    "itemNo" : idx +1,
                    "supplyType" : supplytype,
                    "fob" : "",
                    "exportDuty" : "",
                    "hsnsacCode" : str(data['hsn_or_sac']),
                    "productCode" : "",
                    "itemType" : "",
                    "itemUqc" : data['unit'],
                    "itemQty" : data['quantity'],
                    "igstRt" : igstRt,
                    "igstAmt" : igstAmt,
                    "cgstRt" : cgstRt,
                    "cgstAmt" : cgstAmt,
                    "sgstRt" : cgstRt,
                    "sgstAmt" : cgstAmt,
                    "cessRtAdvalorem" : 0,
                    "cessAmtAdvalorem" : 0,
                    "cessRtSpecific" : 0,
                    "cessAmtSpecific" : 0,
                    "stateCessRt" : 0,
                    "stateCessAmt" : 0,
                    "otherValues" : 0,
                    "lineItemAmt" : (float(data['rate']) * float(data['quantity'])),
                    "plantCode" : "",
                    "serialNoII" : "", #"UE00535-WG0000-NAMT",
                    "productName" : (data['description']).replace('"',"'").replace("\n",""), #"Unstudded Earrings",
                    "isService" : str(service),
                    "barcode" : "",
                    "batchNameOrNo" : "",
                    "batchExpiryDate" : "",
                    "warrantyDate" : "",
                    "originCountry" : "",
                    "freeQuantity" : 0,
                    "unitPrice" : float(data['rate']),
                    "itemAmt" : float(data['rate']),
                    "itemDiscount" : 0,
                    "preTaxAmt" : 0,
                    "totalItemAmt" : (float(data['rate']) * float(data['quantity'])) + igstAmt + (2*cgstAmt),
                    "tcsCgstAmt" : 0,
                    "tcsSgstAmt" : 0,
                    "tdsIgstAmt" : 0,
                    "tdsCgstAmt" : 0,
                    "tdsSgstAmt" : 0,
                    "subDivision" : "",
                    "udf1" : "",
                    "ecomTransactionID" : "",
                    "stateCessSpecificRt" : 0,
                    "stateCessSpecificAmt" : 0,
                    "tcsRtIncomeTax" : 0,
                    "tcsAmtIncomeTax" : 0,
                    "docRefNo" : "",
                    "paidAmt" : 0,
                    "balanceAmt" : 0,
                    "profitCentre3" : "",
                    "profitCentre4" : "",
                    "profitCentre5" : "",
                    "profitCentre6" : "",
                    "profitCentre7" : "",
                    "profitCentre8" : ""
                }
                itemlist.append(lineitems)
            print(itemlist)
            return itemlist
        except Exception as e:
            print(str(e))
            pass

    
    @staticmethod
    def bulkBills():
        """Fetch Bills and format response"""
        try:
            has_more_page = True
            page = 1
            # bills = {"req": []}
            while (has_more_page == True):
                bills = {"req": []}
                bill_list = []
                data = ZohoModel.fetch_bills(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "bills" in data and data["bills"]:
                    for idx, item in enumerate(data['bills'], start=1):
                        try:
                            if item['entity_type'] == "bill":
                                bill_list.append({"id": str(item['bill_id']), "number": str(item['bill_number'])})
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
                                sup_type = "TAX"
                                docType = "INV"
                                supgstin = "URP"
                                suppin = ""
                                supStateCode = ""
                                print(details['bill']['gst_no'])
                                if details['bill']['gst_no'] != "":
                                    supgstin = details['bill']['gst_no']
                                    supStateCode = supgstin[:2]
                                    suppin = details['bill']['billing_address']['zip']
                                if str(details['bill']['gst_treatment']) == "overseas":
                                    if float(details['bill']['tax_total']) >0.0:
                                        sup_type = "TAX"
                                    else:
                                        sup_type = "TAX"
                                    docType = 'SLF'
                                    supgstin = ""
                                    suppin = "999999"
                                    supStateCode = "96"
                                elif str(details['bill']['gst_treatment']) == "business_gst":
                                    sup_type = "TAX"
                                elif str(details['bill']['gst_treatment']) == "business_sez":
                                    if float(details['bill']['tax_total']) >0.0:
                                        sup_type = "TAX"
                                    else:
                                        sup_type = "TAX"
                                line_items = ZohoController.create_line_items(details['bill']['line_items'], reverse, supgstin, str(details['bill']['gst_treatment']))                               
                                formatted_date = (datetime.strptime(str(details['bill']['date']), "%Y-%m-%d"))
                                date = formatted_date.strftime("%d/%m/%Y")
                                return_period = formatted_date.strftime("%m%Y")
                                crDrPreGst = "N"
                                igstRt = cgstRt = igstAmt = cgstAmt = 0
                                tdsFlag = "N"
                                
                                try:
                                    if float(details['bill']['tds_percent']) > 0.0:
                                        tdsFlag = 'Y'
                                except Exception as e:
                                    print(str(e))
                                
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
                                    "docType": str(docType),
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
                                    "billToState": str((custdetails['gstin'])[:2]),
                                    "shipToState": str((custdetails['gstin'])[:2]),
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
                            lw.logRecord("Error in bulkBills for loop: " + str(e))
                            print(str(e))
                    print("bills:" + str(bills))
                    
                    cc.bulkBills_DN(bills, bill_list)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in bulkBills: " + str(e))

    @staticmethod
    def bulkVendorCredit():
        """Fetch Bills and format response"""
        try:
            has_more_page = True
            page = 1
            # vendorcredits = {"req": []}
            while (has_more_page == True):
                vendorcredits = {"req": []}
                vc_list = []
                data = ZohoModel.fetch_dn(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "vendor_credits" in data and data["vendor_credits"]:
                    for idx, item in enumerate(data['vendor_credits'], start=1):
                        try:
                            # if item['entity_type'] == "bill":
                            # print(str(item['bill_id']))
                            vc_list.append({"id": str(item['vendor_credit_id']), "number": str(item['vendor_credit_number'])})
                            details = ZohoModel.fetch_dn_details(str(item['vendor_credit_id']))
                            print(details['vendor_credit']['total'])
                            custdetails = sd.organization_address[str(details['vendor_credit']['branch_name'])]
                            reverse = 'N'
                            print(details['vendor_credit']['is_reverse_charge_applied'])
                            print(type(details['vendor_credit']['is_reverse_charge_applied']))
                            if (details['vendor_credit']['is_reverse_charge_applied'] != False):
                                reverse = 'Y'
                            sup_type = "TAX"
                            docType = 'DR'
                            # is_tax_line = details['vendor_credit']['is_item_level_tax_calc']
                            supgstin = "URP"
                            suppin = ""
                            supStateCode = ""
                            print(details['vendor_credit']['gst_no'])
                            if details['vendor_credit']['gst_no'] != "":
                                supgstin = details['vendor_credit']['gst_no']
                                supStateCode = supgstin[:2]
                                suppin = details['vendor_credit']['billing_address']['zip']
                            
                            if str(details['vendor_credit']['gst_treatment']) == "overseas":
                                if float(details['vendor_credit']['tax_total']) >0.0:
                                    sup_type = "TAX"
                                else:
                                    sup_type = "TAX"
                                docType = 'DR'
                                supgstin = ''
                                suppin = "999999"
                                supStateCode = "96"
                            elif str(details['vendor_credit']['gst_treatment']) == "business_gst":
                                sup_type = "TAX"
                            elif str(details['vendor_credit']['gst_treatment']) == "business_sez":
                                if float(details['vendor_credit']['tax_total']) >0.0:
                                    sup_type = "TAX"
                                else:
                                    sup_type = "TAX"
                            line_items = ZohoController.create_line_items(details['vendor_credit']['line_items'], reverse, supgstin, str(details['vendor_credit']['gst_treatment']))
                            formatted_date = (datetime.strptime(str(details['vendor_credit']['date']), "%Y-%m-%d"))
                            date = formatted_date.strftime("%d/%m/%Y")
                            return_period = formatted_date.strftime("%m%Y")
                            crDrPreGst = "Y"
                            igstRt = cgstRt = igstAmt = cgstAmt = 0
                            
                            tdsFlag = "N"
                            
                            try:
                                if float(details['vendor_credit']['tds_percent']) > 0.0:
                                    tdsFlag = 'Y'
                            except Exception as e:
                                print(str(e))
                            
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
                            "docType": str(docType),
                            "docNo": str(details['vendor_credit']['vendor_credit_number']),
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
                            "billToState": str((custdetails['gstin'])[:2]),
                            "shipToState": str((custdetails['gstin'])[:2]),
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
                            lw.logRecord("Error in bulkVendorCredit for loop: " + str(e))
                            print(str(e))
                    print("vendorcredits:" + str(vendorcredits))
                    
                    cc.bulkBills_DN(vendorcredits, vc_list)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in bulkVendorCredit: " + str(e))

    @staticmethod
    def bulkExpense():
        """Fetch Expense and format response"""
        try:
            has_more_page = True
            page = 1
            # expenses = {"req": []}
            while (has_more_page == True):
                expenses = {"req": []}
                expense_list = []
                data = ZohoModel.fetch_expense(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "expenses" in data and data["expenses"]:
                    for idx, item in enumerate(data['expenses'], start=1):
                        try:
                            if item['entity_type'] == "expenses":
                                expense_list.append({"id": str(item['expense_id']), "number": str(item['expense_number'])})
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
                            lw.logRecord("Error in bulkExpense for loop: " + str(e))
                    # print("Invoices" + str(invoices))
                    
                    cc.bulkBills_DN(expenses, expense_list)
                pass
            # return invoices
        except Exception as e:
            lw.logRecord("Error in bulkExpense: " + str(e))

    @staticmethod
    def bulkInvoice():
        """Fetch invoice and format response"""
        try:
            has_more_page = True
            page = 1
            # invoices = {"req": []}
            while (has_more_page == True):
                invoices = {"req": []}
                invoice_list = []
                data = ZohoModel.fetch_invoice(page)
                page += 1

                if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                    has_more_page = False

                if "invoices" in data and data["invoices"]:
                    for idx, item in enumerate(data['invoices'], start=1):
                        try:
                            # if item['entity_type'] == "invoices":
                                
                            # print(str(item['invoices_id']))
                            invoice_list.append({"id": str(item['invoice_id']), "number": str(item['invoice_number'])})
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
                            subsupplyType = "TAX"
                            tdsFlag = "N"
                            try:
                                if float(details['invoice']['tds_percent']) > 0.0:
                                    tdsFlag = 'Y'
                            except Exception as e:
                                print(str(e))
                            # year = ZohoController.get_fiscal_year(date)
                            if str(details['invoice']['gst_treatment']) == "overseas":
                                # subsupplyType = "EXP"
                                if float(details['invoice']['tax_total']) >0.0:
                                    sup_type = "EXPT"
                                    subsupplyType = "EXP"
                                else:
                                    sup_type = "EXPWT"
                                    subsupplyType = "EXP"
                            elif str(details['invoice']['gst_treatment']) == "business_gst":
                                # sup_type = "C"
                                subsupplyType = "TAX"
                            elif str(details['invoice']['gst_treatment']) == "business_sez":
                                if float(details['invoice']['tax_total']) >0.0:
                                    sup_type = "SEZWP"
                                else:
                                    sup_type = "SEZWOP"
                                subsupplyType = "TAX"
                            
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
                            sub_total = float(details['invoice']['sub_total'])
                            print(sub_total)
                            invoice = {
                                # Optional
                                    "userId" : "",
                                    "srcFileName" : "Standard",
                                    "srcIdentifier" : "ZOHO",
                                    "returnPeriod" : str(return_period),
                                    "suppGstin" : str(supgstin),
                                    "docType" : "INV",
                                    "docNo" : str(details['invoice']['invoice_number']),
                                    "docDate" : str(date),
                                    "orgDocType" : "",
                                    "crDrPreGst" : "",
                                    "custGstin" : "",
                                    # "custOrSupType" : sup_type,
                                    "orgCgstin" : "",
                                    "custOrSupName" : str(details['invoice']['customer_name']),
                                    "custOrSupCode" : "",
                                    "custOrSupAddr1" : str(details['invoice']['billing_address']['street']),
                                    "custOrSupAddr2" : str(details['invoice']['billing_address']['address']),
                                    "custOrSupAddr4" : str(details['invoice']['billing_address']['city']),
                                    "billToState" : str(custStateCode),
                                    "shipToState" : str(custStateCode),
                                    "pos" : str(custStateCode),
                                    "stateApplyingCess" : "",
                                    "portCode" : "",
                                    "shippingBillNo" : "",
                                    "shippingBillDate" : "",
                                    "sec7OfIgstFlag" : "",
                                    "reverseCharge" : str(reverse),
                                    "tcsFlag" : "",
                                    "ecomGSTIN" : "",
                                    "claimRefundFlag" : "",
                                    "autoPopToRefundFlag" : "",
                                    "accVoucherNo" : "",
                                    "accVoucherDate" : "",
                                    "ewbNo" : "",
                                    "ewbDate" : "",
                                    "irn" : "",
                                    "irnDate" : "",
                                    "taxScheme" : "NEWB",
                                    "docCat" : "",
                                    "supTradeName" : "Vestian",
                                    "supLegalName" : "Vestian",
                                    "supBuildingNo" : str(supdetails['address_line1']),
                                    "supBuildingName" : str(supdetails['address_line2']),
                                    "supLocation" : str(supdetails['city']),
                                    "supPincode" : str(supdetails['pincode']),
                                    "supStateCode" : str(supdetails['gstin'][:2]),
                                    "supPhone" : str(supdetails['phone']),
                                    "supEmail" : str(supdetails['email']),
                                    "custTradeName" : str(details['invoice']['customer_name']),
                                    "customerLegalName" : str(details['invoice']['customer_name']),
                                    "custPincode" : str(custpin),
                                    "custPhone" : "",
                                    "custEmail" : "",
                                    "dispatcherStateCode" : str(supdetails['gstin'][:2]),
                                    "shipToGstin" : "",
                                    "shipToTradeName" : str(details['invoice']['customer_name']),
                                    "shipToLegalName" : str(details['invoice']['customer_name']),
                                    "shipToBuildingNo" : str(details['invoice']['billing_address']['street']),
                                    "shipToBuildingName" : str(details['invoice']['billing_address']['address']),
                                    "shipToLocation" : str(details['invoice']['billing_address']['city']),
                                    "shipToPincode" : str(custpin),
                                    "invOtherCharges" : "",
                                    "invAssessableAmt" : float(details['invoice']['sub_total']),
                                    "invIgstAmt" : float(igstAmt),
                                    "invCgstAmt" : float(cgstAmt),
                                    "invSgstAmt" : float(cgstAmt),
                                    "invCessAdvaloremAmt" : 0,
                                    "invCessSpecificAmt" : 0,
                                    "invStateCessAmt" : 0,
                                    "roundOff" : 0,
                                    "totalInvValueInWords" : "",
                                    "countryCode" : "IN",
                                    "invValueFc" : sub_total + float(igstAmt) + (2*float(cgstAmt)),
                                    "invPeriodStartDate" : "",
                                    "invPeriodEndDate" : "",
                                    "payeeName" : "",
                                    "modeOfPayment" : "",
                                    "branchOrIfscCode" : "",
                                    "paymentTerms" : "",
                                    "paymentInstruction" : "",
                                    "creditTransfer" : "",
                                    "directDebit" : "",
                                    "creditDays" : "",
                                    "paymentDueDate" : "",
                                    "accDetail" : "",
                                    "tdsFlag" : "",
                                    "tranType" : "",
                                    "subsupplyType" : subsupplyType,
                                    "otherSupplyTypeDesc" : "",
                                    "exchangeRt" : float(details['invoice']['exchange_rate']),
                                    "companyCode" : "",
                                    "glPostingDate" : "",
                                    "salesOrderNo" : "",
                                    "custTan" : "",
                                    "canReason" : "",
                                    "canRemarks" : "",
                                    "tcsFlagIncomeTax" : "",
                                    "custPANOrAadhaar" : "",
                                    "invRemarks" : "",
                                    "lineItems": []
                                }
                            # invoice["lineItems"].append(line_items)
                            invoice["lineItems"] = line_items
                            invoices["req"].append(invoice)
                        except Exception as e:
                            lw.logRecord("Error in bulkInvoice for loop: " + str(e))
                        
                    print("Invoices" + str(invoices))
                    cc.bulkInvoices_CN(invoices, invoice_list)
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
            # credit_notes = {"req": []}
            while (has_more_page == True):
                try:
                    credit_notes = {"req": []}
                    cn_list = []
                    data = ZohoModel.fetch_cn(page)
                    page += 1

                    if data['page_context']['has_more_page'] == 'false' or data['page_context']['has_more_page'] == False:
                        has_more_page = False
                    
                    if "creditnotes" in data and data["creditnotes"]:
                        for idx, item in enumerate(data['creditnotes'], start=1):
                        
                            try:                                    
                                # print(str(item['invoices_id']))
                                cn_list.append({"id": str(item['creditnote_id']), "number": str(item['creditnote_number'])})
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
                                crDrPreGst = "Y"
                                sup_type = subsupplyType = "TAX"

                                tdsFlag = "N"
                                try:
                                    if float(details['creditnote']['tds_percent']) > 0.0:
                                        tdsFlag = 'Y'
                                except Exception as e:
                                    print(str(e))
                                # year = ZohoController.get_fiscal_year(date)
                                if str(details['creditnote']['gst_treatment']) == "overseas":
                                    # if float(details['creditnote']['tax_total']) >0.0:
                                    #     subsupplyType = "EXP"
                                    #     sup_type = "EXPT"
                                    # else:
                                    #     sup_type = "EXPwT"
                                    subsupplyType = "EXP"
                                elif str(details['creditnote']['gst_treatment']) == "business_gst":
                                    # sup_type = "TAX"
                                    subsupplyType = "TAX"
                                elif str(details['creditnote']['gst_treatment']) == "business_sez":
                                    # if float(details['creditnote']['tax_total']) >0.0:
                                    #     sup_type = "SEZWP"
                                    # else:
                                    #     sup_type = "SEZWOP"
                                    subsupplyType = "TAX"
                                
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
                                        "userId" : "",
                                    "srcFileName" : "Standard",
                                    "srcIdentifier" : "ZOHO",
                                    "returnPeriod" : str(return_period),
                                    "suppGstin" : str(supgstin),
                                    "docType" : "SR",
                                    "docNo" : str(details['creditnote']['creditnote_number']),
                                    "docDate" : str(date),
                                    "orgDocType" : "",
                                    "crDrPreGst" : crDrPreGst,
                                    "custGstin" : "",
                                    # "custOrSupType" : sup_type,
                                    "orgCgstin" : "",
                                    "custOrSupName" : str(details['creditnote']['customer_name']),
                                    "custOrSupCode" : "",
                                    "custOrSupAddr1" : str(details['creditnote']['billing_address']['street']),
                                    "custOrSupAddr2" : str(details['creditnote']['billing_address']['address']),
                                    "custOrSupAddr4" : str(details['creditnote']['billing_address']['address2']),
                                    "billToState" : str(custStateCode),
                                    "shipToState" : str(custStateCode),
                                    "pos" : str(custStateCode),
                                    "stateApplyingCess" : "",
                                    "portCode" : "",
                                    "shippingBillNo" : "",
                                    "shippingBillDate" : "",
                                    "sec7OfIgstFlag" : "",
                                    "reverseCharge" : str(reverse),
                                    "tcsFlag" : "",
                                    "ecomGSTIN" : "",
                                    "claimRefundFlag" : "",
                                    "autoPopToRefundFlag" : "",
                                    "accVoucherNo" : "",
                                    "accVoucherDate" : "",
                                    "ewbNo" : "",
                                    "ewbDate" : "",
                                    "irn" : "",
                                    "irnDate" : "",
                                    "taxScheme" : "NEWB",
                                    "docCat" : "",
                                    "supTradeName" : "Vestian",
                                    "supLegalName" : "Vestian",
                                    "supBuildingNo" : str(supdetails['address_line1']),
                                    "supBuildingName" : str(supdetails['address_line2']),
                                    "supLocation" : str(supdetails['city']),
                                    "supPincode" : str(supdetails['pincode']),
                                    "supStateCode" : str(supdetails['gstin'][:2]),
                                    "supPhone" : str(supdetails['phone']),
                                    "supEmail" : str(supdetails['email']),
                                    "custTradeName" : str(details['creditnote']['customer_name']),
                                    "customerLegalName" : str(details['creditnote']['customer_name']),
                                    "custPincode" : str(custpin),
                                    "custPhone" : "",
                                    "custEmail" : "",
                                    "dispatcherStateCode" : str(supdetails['gstin'][:2]),
                                    "shipToGstin" : "",
                                    "shipToTradeName" : str(details['creditnote']['customer_name']),
                                    "shipToLegalName" : str(details['creditnote']['customer_name']),
                                    "shipToBuildingNo" : str(details['creditnote']['billing_address']['street']),
                                    "shipToBuildingName" : str(details['creditnote']['billing_address']['address']),
                                    "shipToLocation" : str(details['creditnote']['billing_address']['city']),
                                    "shipToPincode" : str(custpin),
                                    "invOtherCharges" : "",
                                    "invAssessableAmt" : float(details['creditnote']['sub_total']),
                                    "invIgstAmt" : float(igstAmt),
                                    "invCgstAmt" : float(cgstAmt),
                                    "invSgstAmt" : float(cgstAmt),
                                    "invCessAdvaloremAmt" : 0,
                                    "invCessSpecificAmt" : 0,
                                    "invStateCessAmt" : 0,
                                    "roundOff" : 0,
                                    "totalInvValueInWords" : "",
                                    "countryCode" : "IN",
                                    "invValueFc" : float(details['creditnote']['sub_total']) + float(igstAmt) (2*float(cgstAmt)),
                                    "invPeriodStartDate" : "",
                                    "invPeriodEndDate" : "",
                                    "payeeName" : "",
                                    "modeOfPayment" : "",
                                    "branchOrIfscCode" : "",
                                    "paymentTerms" : "",
                                    "paymentInstruction" : "",
                                    "creditTransfer" : "",
                                    "directDebit" : "",
                                    "creditDays" : "",
                                    "paymentDueDate" : "",
                                    "accDetail" : "",
                                    "tdsFlag" : "",
                                    "tranType" : "",
                                    "subsupplyType" : subsupplyType,
                                    "otherSupplyTypeDesc" : "",
                                    "exchangeRt" : float(details['creditnote']['exchange_rate']),
                                    "companyCode" : "",
                                    "glPostingDate" : "",
                                    "salesOrderNo" : "",
                                    "custTan" : "",
                                    "canReason" : "",
                                    "canRemarks" : "",
                                    "tcsFlagIncomeTax" : "",
                                    "custPANOrAadhaar" : "",
                                    "invRemarks" : "",
                                    "lineItems": []
                                    }
                                # creditnote["lineItems"].append(line_items)
                                credit_note["lineItems"] = line_items
                                credit_notes["req"].append(credit_note)
                            except Exception as e:
                                lw.logRecord("Error in bulkCreditNote for loop: " + str(e))
                        print("CN: " + str(credit_notes))
                        cc.bulkInvoices_CN(credit_notes, cn_list)
                except Exception as e:
                    lw.logRecord("Error in bulkCreditNote for CN: " + str(e))
        except Exception as e:
            lw.logRecord("Error in bulkCreditNote: " + str(e))

