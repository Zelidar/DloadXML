import tkinter as tk
from tkinter import messagebox  # Import messagebox explicitly
from window_logging import DisplayInfo
from collecting_user_info import CollectedUserInfo
from RSignOperations import GetUserData, GetEnvelopeInfo, SendDynEnvelope, SimCall
from input_validation import UserInputValidator
import threading
from file_logging import log_message

validator = UserInputValidator()

def handle_submission(name, email, CustomerNbr, ContractNbr, CustomerString, display_info):
    global EnvelopeId
    if validator.validate_email(email) and \
       validator.validate_name(name) and \
       validator.validate_number(ContractNbr) and \
       validator.validate_number(CustomerNbr):

        display_info.display_info_window(name, email, CustomerNbr, ContractNbr)
        log_message(name)
        log_message(email)

        # Run the send_email in a separate thread to avoid GUI freeze
        thread = threading.Thread(target=send_email, args=(email, 
                                        name, 
                                        CustomerNbr, 
                                        ContractNbr, 
                                        CustomerString, 
                                        display_info))
        thread.start()
    else:
        messagebox.showerror("Error", "Invalid submission details")


def send_email(email, name, CustomerNbr, ContractNbr, CustomerString, display_info):
    try:
        # Call the SendEnvelope function with email, 
        # name, and the data provided by the CRM.
        # response = SendDynEnvelope(email, name, CustomerNbr, ContractNbr, CustomerString)

        # Extract the required items
        # EnvelopeId = response['EnvelopeId']

        global EnvelopeId
        EnvelopeId = SimCall("10561868-5872-AFAB-4282-DECC")
        display_info.APIcallOk(name, email) 

        # SignDocumentUrl = response['SignDocumentUrl']
        # RecipientList = response['RecipientList']
        # # Assuming each recipient in the list has 'RecipientName' and 'RecipientEmail'
        # for recipient in RecipientList:
        #     RecipientName = recipient['RecipientName']
        #     RecipientEmail = recipient['RecipientEmail']

        #     # Print or use the extracted information
        #     print(f"EnvelopeId: {EnvelopeId}")
        #     print(f"SignDocumentUrl: {SignDocumentUrl}")
        #     print(f"RecipientName: {RecipientName}")
        #     print(f"RecipientEmail: {RecipientEmail}")
        
        # result = SimCall("A call to the RSign API was simulated")

        # result = GetEnvelopeInfo()
        # print(result)

        # Handle the result (e.g., update GUI or log)
    except Exception as e:
        print("Error during email sending:", e)
        messagebox.showerror("Error", "API call failed")


def fetch_user_data(window):
    global EnvelopeId
    try:
        userElements = [
            'CustomerNbr',
            'ContractNbr',
            'CustLongString1',
            'CustLongString2',
            'CustEntryText1',
            'CustEntryText2',
            'Dropdown control assigned to Customer',
            'Single',
            'Married',
            'Widowed'
        ]
        result = GetUserData(EnvelopeId, userElements)
        userInfoWindow = CollectedUserInfo(window)
        userInfoWindow.create_user_info_window()
        userInfoWindow.update_info_display(result)
        # print(result)
    except Exception as e:
        print("Error with user data fetching:", e)
        messagebox.showerror("Error", "GetUserData API call failed")