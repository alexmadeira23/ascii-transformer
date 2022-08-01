import imageio.v3 as imageio
from skimage.transform import resize
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from logic import *

def show_image(img):
    plt.imshow(img)
    plt.axis("off")
    plt.show()

root = tk.Tk()
root.withdraw() # if there isnt any other gui element

file_path = filedialog.askopenfilename()

img = imageio.imread(file_path)
show_image(img)

height = img.shape[0]
width = img.shape[1]

jump_value = 10

img = resize(img, (height / jump_value, width / jump_value))
show_image(img)

height = img.shape[0]
width = img.shape[1]

file = open("output.txt", "a")

for y in range(height):
    line = ""
    for x in range(width):
        pixel = img[y, x]
        r = int(pixel[0] * 255)
        g = int(pixel[1] * 255)
        b = int(pixel[2] * 255)
        grayscale = get_grayscale(r, g, b)
        line += get_char(grayscale)
    print(line)
    file.write(line)

file.close()