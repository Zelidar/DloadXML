import tkinter as tk
from tkinter import ttk
import datetime

class CollectedInfo:
    def __init__(self, root):
        self.root = root
        self.create_info_window()

    def create_info_window(self):
        self.info_window = tk.Toplevel(self.root)
        self.info_window.title("Collected Information")
        
        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.info_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the text widget
        self.text_widget = tk.Text(self.info_window, wrap='word', yscrollcommand=scrollbar.set, state=tk.DISABLED)
        self.text_widget.pack(expand=True, fill='both')
        
        # Configure scrollbar
        scrollbar.config(command=self.text_widget.yview)
        
        # Configure tag for timestamp
        self.text_widget.tag_configure('timestamp', foreground='green', font=('Helvetica', 10, 'bold'))
        
    def update_info_display(self, data):
        # Enable the text widget to insert data
        self.text_widget.config(state=tk.NORMAL)
        
        # Insert the timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_widget.insert(tk.END, timestamp + " Data Collection Set:\n", 'timestamp')
        
        counter = 1
        for label, value in data.items():
            if isinstance(value, list):
                # Convert list to a comma-separated string
                value = ", ".join(value)
            
            # Insert the counting number
            self.text_widget.insert(tk.END, f"{counter}. ")
            
            # Insert the label in bold
            bold_label = f"{label}: "
            self.text_widget.insert(tk.END, bold_label)
            
            # Insert the value
            self.text_widget.insert(tk.END, f"{value}\n")
            
            # Get the index of where the label starts and ends
            label_start = f"{counter}.0"
            label_end = f"{counter}.{len(bold_label)}"
            
            # Define and apply the tag for bold text to the label
            self.text_widget.tag_add("bold", label_start, label_end)
            self.text_widget.tag_config("bold", font=('TkDefaultFont', 9, 'bold'))
            
            counter += 1  # Increment the counter
        
        # Scroll to the end
        self.text_widget.see(tk.END)
        
        # Disable the text widget to make it read-only
        self.text_widget.config(state=tk.DISABLED)