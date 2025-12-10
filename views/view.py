# from models.zoho_model import ZohoModel
# from models.zoho_model import ZohoModel
# from controllers.zoho_controller import ZohoController
from controllers.zoho_controller import ZohoController
import views.logWriter as lw
import controllers.ey_controller as cc
# import sql_gen as sg

def mainProcess():
    try:
        # ZohoController.get_contacts()
        ZohoController.bulkBills()
        ZohoController.bulkVendorCredit()
        # ZohoController.bulkExpense()
        ZohoController.bulkInvoice()
        ZohoController.bulkCreditNote()
        # ZohoController.payments()
        # trns_id, vend_id, vend_nm, int_inv_no, ven_int_no, dis_amt, dis_date, matdate = cc.postingCreditDebitNote()

        # print('trns_id-----', trns_id)
        # if trns_id:
        #     ZohoController.create_all_vendor_credit(trns_id, vend_id, vend_nm, int_inv_no, ven_int_no, dis_amt, dis_date, matdate)
            # ZohoController.update_invoice(trns_id, vend_id, vend_nm, int_inv_no, ven_int_no, dis_amt, dis_date, matdate)
    except Exception as e: 
        print(str(e))
        lw.logRecord(f"Error in mainProcess:{str(e)}")
