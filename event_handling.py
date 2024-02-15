import tkinter as tk
from tkinter import messagebox  # Import messagebox explicitly
from info_display import DisplayInfo
from collected_info import CollectedUserInfo
from RSignOperations import GetUserData, GetEnvelopeInfo

import re
def is_valid_email(email):
    # Simple regex for validating an Email
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_name(name):
    # Check if the name is not empty and contains only letters and spaces
    return name.isalpha() or " " in name


import threading
from file_logging import log_user_info
def handle_submission(name, email, CustomerNbr, ContractNbr, CustomerString, display_info):
    if is_valid_email(email) and is_valid_name(name):
        display_info.display_info(name, email, CustomerNbr, ContractNbr)
        log_user_info(name, email)
        # Run the send_email in a separate thread to avoid GUI freeze
        threading.Thread(target=send_email, args=(email, 
                                                  name, 
                                                  CustomerNbr, 
                                                  ContractNbr, 
                                                  CustomerString, 
                                                  display_info)).start()
    else:
        messagebox.showerror("Error", "Invalid submission details")


def fetch_user_data(window):
    try:
        EnvelopeCode = "03615419-8101-BFFD-9105-FDEF"
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
        result = GetUserData(EnvelopeCode, userElements)
        userInfoWindow = CollectedUserInfo(window)
        userInfoWindow.create_user_info_window()
        userInfoWindow.update_info_display(result)
        # print(result)
    except Exception as e:
        print("Error with user data fetching:", e)
        messagebox.showerror("Error", "GetUserData API call failed")


def send_email(email, name, CustomerNbr, ContractNbr, CustomerString, display_info):
    try:
        # Call the SendEnvelope function with email and name
        display_info.display = DisplayInfo()
        # result = SendDynEnvelope(email, name, CustomerNbr, ContractNbr, CustomerString)
        # result = SimCall("A call to the RSign API was simulated")
        result = GetEnvelopeInfo()
        print(result)
        display_info.APIcallOk(name, email)
        # Handle the result (e.g., update GUI or log)
    except Exception as e:
        print("Error during email sending:", e)
        messagebox.showerror("Error", "API call failed")
