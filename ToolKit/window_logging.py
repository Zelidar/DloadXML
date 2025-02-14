import tkinter as tk
import datetime

class WindowInfoLog:
    def __init__(self, root, EnvelopeID):
        self.root = root  # Store root for later use
        self.info_window = None  # Delay creation
        self.EnvelopeID = EnvelopeID
        self.text_widget = None
        self.user_entries = []


    def ensure_info_window_created(self):
        if not self.info_window or not self.info_window.winfo_exists():
            self.info_window = tk.Toplevel(self.root)  # Use stored root
            self.info_window.title("Operation Log")
            self.info_window.geometry("500x200")  # Set initial size

            scrollbar = tk.Scrollbar(self.info_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.text_widget = tk.Text(self.info_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
            self.text_widget.pack(expand=True, fill=tk.BOTH)
            scrollbar.config(command=self.text_widget.yview)

            self.text_widget.tag_configure('email_sent', foreground='red', font=('Arial', 10, 'bold'))
            self.text_widget.tag_configure('call_OK', foreground='green', font=('Arial', 10, 'bold'))

            close_button = tk.Button(self.info_window, text="Close", command=self.info_window.destroy)
            close_button.pack()


    def window_log_window(self, name, email, CrmCustNbr, CrmContractNbr):
        self.user_entries.append(f"Name: {name}, Email: {email}, CrmCustNbr: {CrmCustNbr}, CrmContractNbr: {CrmContractNbr}")
        self.ensure_info_window_created()  # Ensure the window and widgets are created before updating
        self.update_display()


    def update_display(self):
        if self.text_widget:
            self.text_widget.config(state=tk.NORMAL)  # Enable editing

            # Display the last entry
            last_entry = self.user_entries[-1]
            self.text_widget.insert(tk.END, last_entry + "\n")
            self.text_widget.see(tk.END)

            # Insert and style the email sent message
            userName = self.user_entries[-1].split(', ')[0].split(': ')[1]
            userEmail = self.user_entries[-1].split(', ')[1].split(': ')[1]
            email_message = "... now sending an email to: {} for user: {}\n".format(userEmail, userName)
            self.text_widget.insert(tk.END, email_message, 'email_sent')
            self.text_widget.see(tk.END)

            self.text_widget.config(state=tk.DISABLED)  # Disable editing


    def APIcallOk(self, name, email):
        if self.text_widget:
            self.text_widget.config(state=tk.NORMAL)  # Enable editing

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Insert and style the message
            callOKmessage = "[{}] The envelope was sent to {}, using {}\n".format(timestamp, name, email)
            self.text_widget.insert(tk.END, callOKmessage, 'call_OK')
            self.text_widget.see(tk.END)

            self.text_widget.config(state=tk.DISABLED)  # Disable editing


    def AddTextInWindowLog(self, message):
        """
        Adds a message to the text widget with a timestamp prefix.
        Parameters:
        - message: The message string to be added.
        """
        self.ensure_info_window_created()  # Ensure the window and widgets are created
        if self.text_widget:
            self.text_widget.config(state=tk.NORMAL)  # Enable editing

            # Format the message with the current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timestamped_message = "[{}] {}\n".format(timestamp, message)

            # Insert the timestamped message into the text widget
            self.text_widget.insert(tk.END, timestamped_message)
            self.text_widget.see(tk.END)

            self.text_widget.config(state=tk.DISABLED)  # Disable editing
