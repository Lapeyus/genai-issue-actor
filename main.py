 ```python
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Peach Icon")

# Create a canvas to draw on
canvas = tk.Canvas(window, width=300, height=300)
canvas.pack()

# Create a peach image
peach_image = tk.PhotoImage(file="peach.png")

# Draw the peach image on the canvas
canvas.create_image(150, 150, image=peach_image)

# Start the main loop
window.mainloop()
