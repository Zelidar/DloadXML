import tkinter as tk
from py.UI_components import UserInputApp
from py.window_logging import WindowInfoLog

EnvelopeID = None

def main():
    root = tk.Tk() # Create the UI window instance
    window_log = WindowInfoLog(root, EnvelopeID) # Create the info log window instance
    UserInputApp(root, window_log, EnvelopeID) # Create the UI window
    
    root.mainloop()

if __name__ == "__main__":
    main()
