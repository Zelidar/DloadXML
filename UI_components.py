import tkinter as tk
import random
from datetime import datetime
from tkinter import ttk
from event_handling import handle_submission

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%B-%d %H:%M:%S")  # Format the date and time

def generate_number():
    number = random.randint(0, 9999999)  # Generate a random number between 0 and 9999999
    number *= 2  # Ensure the number is divisible by 2
    return f'000{number:07}'  # Format the number as a 10-digit string with leading zeros

class UserInputApp:
    def __init__(self, root, display_info):
        self.display_info = display_info
        self.root = root
        self.root.title("Membership Application")

        # Load and display logo
        self.logo = tk.PhotoImage(file="Logo.png")
        tk.Label(self.root, image=self.logo).pack()

        # Name Entry
        tk.Label(self.root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        # Set default choice
        self.name_entry.insert(0, "Zaid")

        # Email Entry
        tk.Label(self.root, text="Enter your email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        # Set default choice
        self.email_entry.insert(0, "timgat@gmail.com")

        # CRM Customer Number Entry
        tk.Label(self.root, text="CRM Customer Number:").pack()
        self.CrmCustNbr_entry = tk.Entry(self.root, bg='light blue', justify='right')
        self.CrmCustNbr_entry.insert(0, generate_number())  # Insert the random number
        self.CrmCustNbr_entry.pack()

        # CRM Contract Number Entry
        tk.Label(self.root, text="CRM Contract Number:").pack()
        self.CrmContractNbr_entry = tk.Entry(self.root, bg='light blue', justify='right')
        self.CrmContractNbr_entry.insert(0, generate_number())  # Insert the random number
        self.CrmContractNbr_entry.pack()

        # CRM Customer String Entry
        tk.Label(self.root, text="CRM Customer String:").pack()
        self.CrmCustString_entry = tk.Entry(self.root, bg='light blue', justify='right')
        self.CrmCustString_entry.insert(0, get_current_datetime())  # Insert the current date and time
        self.CrmCustString_entry.pack()

        # Month Dropdown
        tk.Label(self.root, text="Month to begin:").pack()
        self.month_var = tk.StringVar()
        self.month_combo = ttk.Combobox(self.root, textvariable=self.month_var, 
                                        values=["January", "February", "March", 
                                                "April", "May", "June", "July", 
                                                "August", "September", "October", 
                                                "November", "December"])
        self.month_combo.pack()
        # Set default choice
        self.month_var.set("January")

        # Submission Text
        submission_text = "Once you press the submit button, a membership application will be sent to the email you have entered. Please sign it."
        tk.Label(self.root, text=submission_text, wraplength=300).pack()

        # Submit Button
        self.submit_button = tk.Button(self.root, text="Send me the contract...", command=self.submit)
        self.submit_button.pack()

        # Bind Enter key to the submit function
        self.root.bind("<Return>", self.submit)

    def submit(self, event=None):
        handle_submission(self.name_entry.get(), 
                          self.email_entry.get(), 
                          self.CrmCustNbr_entry.get(), 
                          self.CrmContractNbr_entry.get(), 
                          self.CrmCustString_entry.get(), 
                          self.month_var.get(),
                          self.display_info)
        self.DefaultEntries()

    def DefaultEntries(self):
        # self.name_entry.delete(0, tk.END) # Uncomment to delete previous value
        # self.email_entry.delete(0, tk.END) # Uncomment to delete previous value
        self.CrmCustNbr_entry.delete(0, tk.END)
        self.CrmCustNbr_entry.insert(0, generate_number())  # Re-insert the random number
        self.CrmContractNbr_entry.delete(0, tk.END)
        self.CrmContractNbr_entry.insert(0, generate_number())  # Re-insert the random number
        self.CrmCustString_entry.delete(0, tk.END)
        self.CrmCustString_entry.insert(0, get_current_datetime())  # Re-insert the current date and time
        self.month_combo.set('January')
