import tkinter as tk
from UI_components import UserInputApp
from info_display import DisplayInfo
from collected_info import CollectedInfo

def main():
    root = tk.Tk()
    display_info = DisplayInfo() # Create the display info window
    UserInputApp(root, display_info)
    collected_info_instance = CollectedInfo(root)  # Create the collected info window
    
    # This line would be called when data is received from the API
    # collected_info_instance.update_info_display(userElements)
    
    root.mainloop()

if __name__ == "__main__":
    main()
