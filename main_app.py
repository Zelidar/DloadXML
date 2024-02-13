import tkinter as tk
from UI_components import UserInputApp
from info_display import DisplayInfo
from collected_info import CollectedInfo

def main():
    root = tk.Tk()
    display_info = DisplayInfo()
    UserInputApp(root, display_info)
    collected_info_instance = CollectedInfo(root)  # Create the collected info window
    
    example_data = {
        "CustomerNbr": "123456",
        "ContractNbr": "78910",
        "CustLongString1": "This is an example of a long string, written by the user.",
        "CustEntryText1": "That first text has been entered by the user.",
        "CustEntryText2": "That second text has also been entered by the user.",
        "DropdownList": ["Option1", "Option2", "Option3", "Option4"],  # Dropdown options
        "VertRadioButton": ["Choice1", "Choice2", "Choice3"]  # Radio button choices
    }
    
    # This line would be called when data is received from the API
    collected_info_instance.update_info_display(example_data)
    
    root.mainloop()

if __name__ == "__main__":
    main()
