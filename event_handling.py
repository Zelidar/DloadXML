import tkinter as tk
from tkinter import messagebox  # Import messagebox explicitly
from info_display import DisplayInfo


import re
def is_valid_email(email):
    # Simple regex for validating an Email
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_name(name):
    # Check if the name is not empty and contains only letters and spaces
    return name.isalpha() or " " in name


def is_valid_month(month):
    # Check if the month is one of the valid options
    valid_months = ["January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"]
    return month in valid_months


import threading
from file_logging import log_user_info
def handle_submission(name, email, CustomerNbr, ContractNbr, CustomerString, month, display_info):
    if is_valid_email(email) and is_valid_name(name) and is_valid_month(month):
        display_info.display_info(name, email, month, CustomerNbr, ContractNbr)
        log_user_info(name, email, month)
        # Run the send_email in a separate thread to avoid GUI freeze
        threading.Thread(target=send_email, args=(email, name, CustomerNbr, ContractNbr, CustomerString, display_info)).start()
    else:
        messagebox.showerror("Error", "Invalid submission details")


from RSignOperations import SendDynEnvelope
def send_email(email, name, CustomerNbr, ContractNbr, CustomerString, display_info):
    try:
        # Call the SendEnvelope function with email and name
        display_info.display = DisplayInfo()
        result = SendDynEnvelope(email, name, CustomerNbr, ContractNbr, CustomerString)
        # result = SimCall("A call to the RSign API was simulated")
        print(result)
        display_info.APIcallOk(name, email)
        # Handle the result (e.g., update GUI or log)
    except Exception as e:
        print("Error during email sending:", e)
        messagebox.showerror("Error", "API call failed")
