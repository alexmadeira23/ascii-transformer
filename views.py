import imageio.v3 as imageio
import tkinter as tk
from tkinter import filedialog
from logic import *

root = tk.Tk()
root.withdraw() # if there isnt any other gui element

file_path = filedialog.askopenfilename()

img = imageio.imread(file_path)

height = img.shape[0]
width = img.shape[1]

file = open("output.txt", "a")

jump_value = 2

y = 0
while y < height:
    line = ""
    x = 0
    while x < width:
        grayscales = []
        for _ in range(jump_value):
            if x >= width:
                break
            pixel = img[y, x]
            r = int(pixel[0])
            g = int(pixel[1])
            b = int(pixel[2])
            grayscales.append(get_grayscale(r, g, b))
            x = x + 1
        line += get_char(average(grayscales))
    print(line)
    file.write(line)
    y = y + jump_value

file.close()