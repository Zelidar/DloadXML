from tkinter import messagebox  # Import messagebox explicitly
from py.collecting_user_info import CollectedUserInfo
from py.RSignOperations import GetUserData, GetEnvelopeStatus, SimCall, SendDynEnvelope, SendEnvelopeFromRule
from py.input_validation import UserInputValidator
import threading
import queue
from py.FileLogging import log_message

validator = UserInputValidator()

def handle_submission(name, 
                      email, 
                      CustomerNbr, 
                      ContractNbr, 
                      CustomerString, 
                      window_log, 
                      EnvelopeID):
    if validator.validate_email(email) and \
       validator.validate_name(name) and \
       validator.validate_number(ContractNbr) and \
       validator.validate_number(CustomerNbr):

        window_log.window_log_window(name, email, CustomerNbr, ContractNbr)
        log_message(name)
        log_message(email)

        result_queue = queue.Queue()
        # Run the send_email in a separate thread to avoid GUI freeze
        thread = threading.Thread(target=send_email, 
                                  args=(email, 
                                        name, 
                                        CustomerNbr, 
                                        ContractNbr, 
                                        CustomerString, 
                                        window_log,
                                        EnvelopeID, result_queue))
        thread.start()
        #  Wait for the EnvelopeID in the queue, you may optionally add a timeout here
        EnvelopeID = result_queue.get()
        print(f"Received EnvelopeID from thread: {EnvelopeID}")
        return EnvelopeID
    else:
        messagebox.showerror("Error", "Invalid submission details")
        return None


def send_email(email, name, CustomerNbr, ContractNbr, CustomerString, window_log, EnvelopeID, result_queue):
    try:
        # Call the SendEnvelope function with email, 
        # name, and the data provided by the CRM.
        response = SendEnvelopeFromRule(email, name, CustomerNbr, ContractNbr, CustomerString)
        
        # Check if the response was successful
        if isinstance(response, dict) and 'EnvelopeCode' in response:
            # Extract the required items
            EnvelopeID = response['EnvelopeCode']
            result_queue.put(EnvelopeID)  # Put the result into the queue
            window_log.AddTextInWindowLog(f"Current envelope id: {EnvelopeID}")
            print(f"Current envelope code: {EnvelopeID}")
            window_log.APIcallOk(name, email)
        else:
            # Handle unsuccessful response
            error_message = response  # Assuming response is the error message string as 'else' in SendEnvelopeFromRule
            print("Error during sending:", error_message)
            window_log.AddTextInWindowLog(f"Error: {error_message}")
            messagebox.showerror("Error", f"send_email call failed: {error_message}")
            result_queue.put(None)

    except Exception as e:
        # This will only handle unexpected errors not related to response handling
        print("Error during email sending:", e)
        messagebox.showerror("Error", "send_email call failed")
        result_queue.put(None)



def fetch_user_data(window_user_data, window_log, EnvelopeID):
    if EnvelopeID is None:  
        window_log.AddTextInWindowLog("(fetch_user_data) EnvelopeID is required. Did you create an envelope?")
        return  
    try:
        if EnvelopeID is None:  # Check if EnvelopeID is provided
            window_user_data.AddTextInWindowLog("EnvelopeID is required. Did you create an envelope?")
            return  # Exit the function if no EnvelopeID
        userElements = [
            'CrmCustomerNbr',
            'CrmContractNbr',
            'CustLongString1',
            'CustLongString2',
            'CustEntryText1',
            'CustEntryText2',
            'DropDownControl',
            'Saturn',
            'Uranus',
            'Neptune',
            'Earth'
        ]
        result = GetUserData(EnvelopeID, userElements)
        userInfoWindow = CollectedUserInfo(window_user_data)
        userInfoWindow.create_user_info_window()
        userInfoWindow.update_info_display(result)
        # print(result)
    except Exception as e:
        print("Error with user data fetching: ", e)
        messagebox.showerror("Error", "GetUserData API call failed")


def fetch_envelope_status(window_log, EnvelopeID):
    if EnvelopeID is None:  
        window_log.AddTextInWindowLog("(fetch_envelope_status) EnvelopeID is required. Did you create an envelope?")
        return  
    try:
        result = GetEnvelopeStatus(EnvelopeID)
        # Extract StatusMessage and Message from the result
        status_message = result.get("StatusMessage", "")
        message = result.get("Message", "")
        # Combine StatusMessage and Message with a space in between
        combined_message = f"Status message = '{status_message}', Message = '{message}'"
        window_log.AddTextInWindowLog(combined_message)
    except Exception as e:
        print("Error with fetching envelope status: ", e)
        messagebox.showerror("Error", "GetEnvelopeStatus API call failed")
