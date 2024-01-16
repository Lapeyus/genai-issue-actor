 ```python
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Dog Icon")

# Create a canvas to draw on
canvas = tk.Canvas(window, width=300, height=300)
canvas.pack()

# Create a dog image
dog_image = tk.PhotoImage(file="dog.png")

# Draw the dog image on the canvas
canvas.create_image(150, 150, image=dog_image)

# Start the main loop
window.mainloop()
