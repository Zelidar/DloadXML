import tkinter as tk
import random
from datetime import datetime
from tkinter import ttk
from event_handling import handle_submission, fetch_user_data, fetch_envelope_status

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%B-%d %H:%M:%S")  # Format the date and time

def generate_number():
    number = random.randint(0, 99999)  # Generate a random number between 0 and 9999999
    number *= 2  # Ensure the number is divisible by 2, making it less random.
    return f'00{number:4}'  # Format the number as a string with leading zeros

class UserInputApp:
    def __init__(self, root, window_log):
        self.window_log = window_log
        self.root = root
        self.root.title("Personal Data Collection")

        # Load and display logo
        self.logo = tk.PhotoImage(file="Logo.png")
        tk.Label(self.root, image=self.logo).pack()

        # Name Entry
        tk.Label(self.root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        # Set default choice
        self.name_entry.insert(0, "Test Customer")

        # Email Entry
        tk.Label(self.root, text="Enter your email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        # Set default choice
        self.email_entry.insert(0, "zaid.el-hoiydi@frama.com")

        # CRM Customer Number Entry
        tk.Label(self.root, text="CRM Customer Number:").pack()
        self.CrmCustNbr_entry = tk.Entry(self.root, bg='light blue', justify='right')
        self.CrmCustNbr_entry.insert(0,  "CRM_" + str(generate_number()))  # Insert the random number
        self.CrmCustNbr_entry.pack()

        # CRM Contract Number Entry
        tk.Label(self.root, text="CRM Contract Number:").pack()
        self.CrmContractNbr_entry = tk.Entry(self.root, bg='light blue', justify='right')
        self.CrmContractNbr_entry.insert(0,  "CRM_" + str(generate_number()))  # Insert the random number
        self.CrmContractNbr_entry.pack()

        # CRM Customer String Entry
        tk.Label(self.root, text="CRM Customer String:").pack()
        self.CrmCustString_entry = tk.Entry(self.root, bg='light blue', justify='right')
        self.CrmCustString_entry.insert(0, "CRM_" + get_current_datetime())  # Insert the current date and time
        self.CrmCustString_entry.pack()

        # Submission Text
        submission_text = "Once you press the submit button, a contract will be sent to the email you have entered. Please provide the requested information, and sign it."
        tk.Label(self.root, text=submission_text, wraplength=300).pack()
        # Submit Button
        self.submit_button = tk.Button(self.root, text="Send the contract...", command=self.SubmitContract)
        self.submit_button.pack()
        # Bind Enter key to the submit function
        self.root.bind("<Return>", self.SubmitContract)

        # Envelope Status Fetching Text
        env_status_fetching_text = "Whatch the log window, when you click it will show you the latest envelope status."
        tk.Label(self.root, text=env_status_fetching_text, wraplength=300).pack()
        # Fetch User Data Button
        self.env_status_fetch_data_button = tk.Button(self.root, 
                                           text="Seeking envelope status...", 
                                           command=self.GettingEnvStatus)
        self.env_status_fetch_data_button.pack()

        # Data Fetching Text
        data_fetching_text = "Whatch the log window. Once signed, you can collect user data from the envelope located in the RPost cloud."
        tk.Label(self.root, text=data_fetching_text, wraplength=300).pack()
        # Fetch User Data Button
        self.fetch_data_button = tk.Button(self.root, 
                                           text="Fetching user data...", 
                                           command=self.GettingUserData)
        self.fetch_data_button.pack()


    def SubmitContract(self, event=None):
        handle_submission(self.name_entry.get(), 
                          self.email_entry.get(), 
                          self.CrmCustNbr_entry.get(), 
                          self.CrmContractNbr_entry.get(), 
                          self.CrmCustString_entry.get(), 
                          self.window_log)
        self.DefaultEntries()

    def GettingEnvStatus(self, event=None):
        fetch_envelope_status(self.window_log)

    def GettingUserData(self, event=None):
        fetch_user_data(self.root)


    def DefaultEntries(self):
        # self.name_entry.delete(0, tk.END) # Uncomment to delete previous value
        # self.email_entry.delete(0, tk.END) # Uncomment to delete previous value
        self.CrmCustNbr_entry.delete(0, tk.END)
        self.CrmCustNbr_entry.insert(0, generate_number())  # Re-insert the random number
        self.CrmContractNbr_entry.delete(0, tk.END)
        self.CrmContractNbr_entry.insert(0, generate_number())  # Re-insert the random number
        self.CrmCustString_entry.delete(0, tk.END)
        self.CrmCustString_entry.insert(0, get_current_datetime())  # Re-insert the current date and time
