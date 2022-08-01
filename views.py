import imageio.v3 as imageio
from skimage.transform import resize
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import PySimpleGUI as sg
from logic import *

def show_image(img):
    plt.imshow(img)
    plt.axis("off")
    plt.show()

def app():
    original_img = None
    resolution_decrease = 1

    # Define the window's contents
    layout = [
        [sg.Button('Choose photo')],
        [sg.Text("Resolution decrease value: ")],
        [sg.Slider(range=(1, 10), orientation="h", key='-SLIDER-')],
        [sg.Image(key="-IMAGE-")],
        [sg.Button('Transform into ASCII art'), sg.Button('Quit')],
        [sg.Text(size=(40,1), key='-OUTPUT-')],
    ]

    # Create the window
    window = sg.Window('Ascii Transformer', layout, finalize=True)

    window['-SLIDER-'].bind('<ButtonRelease-1>', ' Release')

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()

        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        elif event == "Choose photo":
            file_path = filedialog.askopenfilename()
            if file_path != "":
                original_img = imageio.imread(file_path)
                window["-IMAGE-"].update(source=file_path)

        elif event == '-SLIDER- Release':
            resolution_decrease = values['-SLIDER-']

        elif event == 'Transform into ASCII art':
            height = original_img.shape[0]
            width = original_img.shape[1]

            img = resize(original_img, (height / resolution_decrease, width / resolution_decrease))

            print_ascii(img)


        # Output a message to the window
        #window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

    # Finish up by removing from the screen
    window.close()

def console_app():
    file_path = filedialog.askopenfilename()
    img = imageio.imread(file_path)
    show_image(img)

    height = img.shape[0]
    width = img.shape[1]

    resolution_decrease = 2

    img = resize(img, (height / resolution_decrease, width / resolution_decrease))
    show_image(img)

    print_ascii(img)

def print_ascii(img):
    height = img.shape[0]
    width = img.shape[1]

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

app()