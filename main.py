 ```python
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("My Computer")

# Set the icon
window.iconbitmap("computer.ico")

# Create a label
label = tk.Label(text="This is a computer.")
label.pack()

# Start the main loop
window.mainloop()
