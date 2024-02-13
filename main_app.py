import tkinter as tk
from ui_components import UserInputApp
from info_display import DisplayInfo

def main():
    root = tk.Tk()
    display_info = DisplayInfo()  # Create a single window instance
    UserInputApp(root, display_info)
    root.mainloop()

if __name__ == "__main__":
    main()
