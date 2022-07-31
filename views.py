import imageio.v3 as imageio
import tkinter as tk
from tkinter import filedialog
from logic import *

root = tk.Tk()
root.withdraw() # if there isnt any toher gui element

file_path = filedialog.askopenfilename()

img = imageio.imread(file_path)

height = img.shape[0]
width = img.shape[1]

print(height)
print(width)

for y in range(height):
    for x in range(width):
        pixel = img[y, x]
        r = int(pixel[0])
        g = int(pixel[1])
        b = int(pixel[2])
        grayscale = get_grayscale(r, g, b)