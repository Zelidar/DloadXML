import tkinter as tk
from UI_components import UserInputApp
from window_logging import DisplayInfo

EnvelopeId = None

def main():
    root = tk.Tk()

    display_info = DisplayInfo(root) # Create the display info window
    UserInputApp(root, display_info)
    
    root.mainloop()

if __name__ == "__main__":
    main()
