```python
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Whale Icon")

# Create the icon
whale_icon = tk.PhotoImage(file="whale.png")
window.iconphoto(False, whale_icon)

# Create the label
label = tk.Label(text="This is a whale icon.")
label.pack()

# Start the main loop
window.mainloop()
```