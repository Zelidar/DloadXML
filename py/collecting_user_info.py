import tkinter as tk
from tkinter import ttk
import datetime

class CollectedUserInfo:
    def __init__(self, root):
        self.root = root
    #     self.create_user_info_window()

    def create_user_info_window(self):
        self.info_window = tk.Toplevel(self.root)
        self.info_window.title("Collected Information")
        
        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.info_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the text widget with a monospaced font
        self.text_widget = tk.Text(self.info_window, wrap='word', yscrollcommand=scrollbar.set, 
                                   state=tk.DISABLED, font=('Courier', 10))
        self.text_widget.pack(expand=True, fill='both')
        
        # Configure scrollbar
        scrollbar.config(command=self.text_widget.yview)
        
        # Configure tag for timestamp
        self.text_widget.tag_configure('timestamp', foreground='green', font=('Courier', 10, 'bold'))
        
        # Configure tag for bold text to use the same monospaced font
        self.text_widget.tag_configure('bold', font=('Courier', 10, 'bold'))


    def update_info_display(self, data):
        # Enable the text widget to insert data
        self.text_widget.config(state=tk.NORMAL)
        
        # Insert the timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_widget.insert(tk.END, timestamp + " -- Data Collection Set:\n", 'timestamp')
        
        counter = 1
        for label, value in data.items():
            if isinstance(value, list):
                # Convert list to a comma-separated string
                value = ", ".join(value)
            
            # Insert the counting number and the label
            label_text = f"{counter}. {label}:  "
            self.text_widget.insert(tk.END, label_text)
            
            # Insert the value
            self.text_widget.insert(tk.END, f"{value}\n")
            
            counter += 1  # Increment the counter
        
        # Scroll to the end
        self.text_widget.see(tk.END)
        
        # Disable the text widget to make it read-only
        self.text_widget.config(state=tk.DISABLED)
