import tkinter as tk
from UI_components import UserInputApp
from window_logging import WindowInfoLog

EnvelopeId = None

def main():
    root = tk.Tk() # Create the UI window instance
    window_log = WindowInfoLog(root) # Create the info log window instance
    UserInputApp(root, window_log) # Create the UI window
    
    root.mainloop()

if __name__ == "__main__":
    main()
