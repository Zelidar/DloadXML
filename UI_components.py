import tkinter as tk
import random
from datetime import datetime
from tkinter import ttk, font as tkFont
from event_handling import handle_submission, fetch_user_data, fetch_envelope_status

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%B-%d %H:%M:%S")  # Format the date and time

def generate_number():
    number = random.randint(0, 99999)  # Generate a random number between 0 and 9999999
    number *= 2  # Ensure the number is divisible by 2, making it less random.
    return f'00{number:4}'  # Format the number as a string with leading zeros

class UserInputApp:
    def __init__(self, root, window_log, EnvelopeID):
        self.window_log = window_log
        self.root = root
        self.EnvelopeID = EnvelopeID
        self.root.title("CRM Simulation")
        entry_width = 16
        large_entry_width = 32

        # Load and display logo
        self.logo = tk.PhotoImage(file="Logo.png")
        tk.Label(self.root, image=self.logo).pack()

        # Introduction Text
        Introduction_text = ("This demonstration application will partially "
                            "prefill (CRM_) a RSign contract, and then collect "
                            "information the signer has entered.")
        tk.Label(self.root, text=Introduction_text, wraplength=300).pack()

        # Name Entry
        tk.Label(self.root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.root, width=large_entry_width, justify='center')
        self.name_entry.pack()
        # Set default choice
        self.name_entry.insert(0, "Zaid El-Hoiydi")

        # Email Entry
        tk.Label(self.root, text="Enter an email:").pack()
        self.email_entry = tk.Entry(self.root, width=large_entry_width, justify='center')
        self.email_entry.pack()
        # Set default choice
        self.email_entry.insert(0, "zaid.el-hoiydi@frama.com")

        # CRM Customer Number Entry
        tk.Label(self.root, text="CRM Customer Number:").pack()
        self.CrmCustNbr_entry = tk.Entry(self.root, width=entry_width, bg='light blue', justify='center')
        self.CrmCustNbr_entry.insert(0,  "CRM_" + str(generate_number()))  # Insert the random number
        self.CrmCustNbr_entry.pack()

        # CRM Contract Number Entry
        tk.Label(self.root, text="CRM Contract Number:").pack()
        self.CrmContractNbr_entry = tk.Entry(self.root, width=entry_width, bg='light blue', justify='center')
        self.CrmContractNbr_entry.insert(0,  "CRM_" + str(generate_number()))  # Insert the random number
        self.CrmContractNbr_entry.pack()

        # CRM Customer String Entry
        tk.Label(self.root, text="CRM Customer String:").pack()
        self.CrmCustString_entry = tk.Entry(self.root, width=large_entry_width, bg='light blue', justify='center')
        self.CrmCustString_entry.insert(0, "CRM_" + get_current_datetime())  # Insert the current date and time
        self.CrmCustString_entry.pack()

        # Submission Text
        submission_text = ("Once you press the 'Send ...' button, a RSign transaction"
                           " will begin = email be sent to the one you have entered.")
        tk.Label(self.root, text=submission_text, wraplength=300).pack()
        # Submit Button
        self.submit_button = tk.Button(self.root, 
                                       text="1 - Send the contract...", 
                                       font=("Helvetica", 10, "bold"), 
                                       command=self.SubmitContract)
        # Bind Enter key to the submit function
        self.root.bind("<Return>", self.SubmitContract)
        self.submit_button.pack()

        # Envelope Status Fetching Text
        env_status_fetching_text = ("Clicking 'Seek ...' button will fetch the latest"
                                    " envelope status and put it in the log window.")
        tk.Label(self.root, text=env_status_fetching_text, wraplength=300).pack()
        # Fetch User Data Button
        self.env_status_fetch_data_button = tk.Button(self.root, 
                                           text="2 - Seek envelope status...", 
                                           font=("Helvetica", 10, "bold"), 
                                           command=self.GettingEnvStatus)
        self.env_status_fetch_data_button.pack()

        # Data Fetching Text
        data_fetching_text = ("Once signed, you can collect user data from the envelope"
                              " located in the RPost cloud using 'Import user...'")
        tk.Label(self.root, text=data_fetching_text, wraplength=300).pack()
        # Fetch User Data Button
        self.fetch_data_button = tk.Button(self.root, 
                                           text="3 - Import user data...", 
                                           font=("Helvetica", 10, "bold"), 
                                           command=self.GettingUserData)
        self.fetch_data_button.pack(pady=(0,10))

    def SubmitContract(self, event=None):
        self.EnvelopeID = handle_submission(self.name_entry.get(), 
                                            self.email_entry.get(), 
                                            self.CrmCustNbr_entry.get(), 
                                            self.CrmContractNbr_entry.get(), 
                                            self.CrmCustString_entry.get(), 
                                            self.window_log,
                                            self.EnvelopeID)
        self.DefaultEntries()

    def GettingEnvStatus(self, event=None):
        fetch_envelope_status(self.window_log, self.EnvelopeID)

    def GettingUserData(self, event=None):
        fetch_user_data(self.root, self.window_log, self.EnvelopeID)


    def DefaultEntries(self):
        # self.name_entry.delete(0, tk.END) # Uncomment to delete previous value
        # self.email_entry.delete(0, tk.END) # Uncomment to delete previous value
        self.CrmCustNbr_entry.delete(0, tk.END)
        self.CrmCustNbr_entry.insert(0, generate_number())  # Re-insert the random number
        self.CrmContractNbr_entry.delete(0, tk.END)
        self.CrmContractNbr_entry.insert(0, generate_number())  # Re-insert the random number
        self.CrmCustString_entry.delete(0, tk.END)
        self.CrmCustString_entry.insert(0, get_current_datetime())  # Re-insert the current date and time
