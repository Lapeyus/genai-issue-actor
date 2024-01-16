
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Thumbs Up Icon")

# Create a canvas to draw the icon on
canvas = tk.Canvas(window, width=100, height=100)
canvas.pack()

# Draw the thumbs up icon
canvas.create_polygon([50, 10, 90, 50, 50, 90], fill="green")
canvas.create_line(50, 50, 50, 90, width=5)

# Set the window icon
window.iconbitmap("thumbs_up.ico")

# Start the main loop
window.mainloop()
