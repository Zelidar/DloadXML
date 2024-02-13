import tkinter as tk
import datetime

class DisplayInfo:
    def __init__(self):
        self.user_entries = []
        self.info_window = None
        self.text_widget = None

    def APIcallOk(self, name, email):
        if self.text_widget:
            self.text_widget.config(state=tk.NORMAL)  # Enable editing

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Insert and style the message
            callOKmessage = "[{}] The envelope was sent to {}, using {}\n".format(timestamp, name, email)
            self.text_widget.insert(tk.END, callOKmessage, 'call_OK')
            self.text_widget.see(tk.END)

            self.text_widget.config(state=tk.DISABLED)  # Disable editing

    def update_display(self):
        if self.text_widget:
            self.text_widget.config(state=tk.NORMAL)  # Enable editing

            # Display the last entry
            last_entry = self.user_entries[-1]
            self.text_widget.insert(tk.END, last_entry + "\n")
            self.text_widget.see(tk.END)

            # Insert and style the email sent message
            userName = self.user_entries[-1].split(', ')[0].split(': ')[1]
            userEmail = self.user_entries[-1].split(', ')[2].split(': ')[1]
            email_message = "... now sending an email to: {} for user: {}\n".format(userEmail, userName)
            self.text_widget.insert(tk.END, email_message, 'email_sent')
            self.text_widget.see(tk.END)

            self.text_widget.config(state=tk.DISABLED)  # Disable editing

    def display_info(self, name, email, month, CrmCustNbr, CrmContractNbr):
        # Add new entry
        self.user_entries.append(f"Name: {name}, Month: {month}, Email: {email}, CrmCustNbr: {CrmCustNbr}, CrmContractNbr: {CrmContractNbr}")

        # Create the window if it does not exist
        if not self.info_window or not self.info_window.winfo_exists():
            self.info_window = tk.Toplevel()
            self.info_window.title("Operation Log")
            self.info_window.geometry("500x200")  # Set initial size

            # Create a scrollbar
            scrollbar = tk.Scrollbar(self.info_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Create a text widget with the scrollbar
            self.text_widget = tk.Text(self.info_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
            self.text_widget.pack(expand=True, fill=tk.BOTH)

            # Configure the scrollbar to scroll the text widget
            scrollbar.config(command=self.text_widget.yview)

            # Style for messages
            self.text_widget.tag_configure('email_sent', foreground='red', font=('Arial', 10, 'bold'))
            self.text_widget.tag_configure('call_OK', foreground='green', font=('Arial', 10, 'bold'))

            close_button = tk.Button(self.info_window, text="Close", command=self.info_window.destroy)
            close_button.pack()

        # Update the display with the new entry
        self.update_display()
