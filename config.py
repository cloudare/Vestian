import json


dataJSON = '''{
				"clientName":"Vestian",
				"serviceName":"Cloudare",
			}'''
# serverData = json.loads(dataJSON)


#URL
# zoho_access_token   = 'https://accounts.zoho.in/oauth/v2/token?grant_type=authorization_code&'
zoho_refresh_token  = 'https://accounts.zoho.in/oauth/v2/token?'
zoho_contact    	= 'https://www.zohoapis.in/books/v3/contacts'
zoho_bills		= 'https://www.zohoapis.in/books/v3/bills'
zoho_expense		= 'https://www.zohoapis.in/books/v3/expenses'
zoho_dn		= 'https://www.zohoapis.in/books/v3/vendorcredits'
zoho_invoice		= 'https://www.zohoapis.in/books/v3/invoices'
zoho_cn		= 'https://www.zohoapis.in/books/v3/creditnotes'
zoho_payments		= 'https://www.zohoapis.in/books/v3/vendorpayments'



# ey urls
ey_auth_url = 'https://einvoicesyncapi.eyasp.in/einvoiceapi/v2.0/authenticate'
ey_refresh_url = 'https://einvoicesyncapi.eyasp.in/einvoiceapi/v2.0/refreshtoken'
ey_purchase_url = 'https://einvoicesyncapi.eyasp.in/einvoiceapi/v2.0/async/savePurcahseRegister' 
ey_sales_url = 'https://einvoicesyncapi.eyasp.in/einvoiceapi/v2.0/async/generateIRN' 
ey_get_status = 'https://einvoicesyncapi.eyasp.in/einvoiceapi/v2.0/async/getStatusForAckNum'
ey_sales_ack = 'https://einvoicesyncapi.eyasp.in/einvoiceapi/v2.0/async/getData'
ey_purchase_ack = 'https://einvoicesyncapi.eyasp.in/einvoiceapi/v2.0/async/purchaseRegisterGetData'

#ey Token
authorization = ''

#ey credentials

apiaccesskey = '80e27ccb48a34034866ee416a5989e6e'
refresh_token_ey = ''
        
#Who column fixed value
createdBy = 'Cloudare'
updatedBy = 'Cloudare' 

# Zoho details
organization_id = '60058067152'
client_id       = '1000.OZ9KDR5H5O1TCA42H8V4JWU2S1WIFY'
client_secret   = '980f86dca2e14faa016e26348aca8a0db89517a596'
refresh_token   = '1000.38dd876593bbc4b20d9db5464290f1c7.8fe3f6028cbb6f1bdf7b5354da6f9b67'
access_token    = '1000.9532a231c6559c12beefd2bccf1ce9ea.b8d88980dca5097514a99c4b1e33a1bc'
code = '1000.d0e559ca83e84bc9144aa72d5756ed43.a0d6275585391330ad3b647907beb6da'

#Organization GSTIN's
organization_gst = {"Head Office":"29AADCV2193D1ZA", "Telangana": "36AADCV2193D1ZF", "Tamil Nadu": "33AADCV2193D1ZL"}
organization_address = {
						"Head Office": {
							"address_line1": "First Floor, West Wing, DuParc Trinity",
							"address_line2": "17, M G Road",
							"city": "Bangalore",
							"state": "Karnataka",
							"pincode": "560001",
							"country": "India",
							"gstin": "29AADCV2193D1ZA",
							"phone": "",
							"email": "ganesh@vestian.in"
						},
						"Telangana": {
							"address_line1": "45 MG Road",
							"address_line2": "Near Metro Station",
							"city": "Adilabad",
							"state": "Telangana",
							"pincode": "504273",
							"country": "India",
							"gstin": "36AADCV2193D1ZF",
							"phone": "",
							"email": ""
						},
						"Tamil Nadu": {
							"address_line1": "Plot 56, Industrial Area",
							"address_line2": "",
							"city": "Chennai",
							"state": "Tamil Nadu",
							"pincode": "600001",
							"country": "India",
							"gstin": "33AADCV2193D1ZL",
							"phone": "",
							"email": ""
						}
					}


