from controllers.zoho_controller import ZohoController
import views.logWriter as lw
import controllers.ey_controller as cc

def mainProcess():
    try:
        # ZohoController.bulkBills()
        # ZohoController.bulkVendorCredit()
        # ZohoController.bulkExpense()
        ZohoController.bulkInvoice()
        # ZohoController.bulkCreditNote()
    except Exception as e: 
        print(str(e))
        lw.logRecord(f"Error in mainProcess:{str(e)}")
