from PIL import Image, ImageTk
from tkinter import filedialog
import PySimpleGUI as sg
from logic import *

sg.theme('DarkGrey13') 

def app():
    image = None
    resolution_decrease = 1

    layout = [
        [sg.Button('Choose photo'),
        [sg.Text("Resolution decrease: ", justification="center"), sg.Slider(range=(1, 100), expand_x=True, orientation="h", key='-SLIDER-')],
        [sg.Image(size=(300, 300), key="-IMAGE-"), sg.Multiline(size=(100, 30), disabled=True, background_color="black", text_color="white", font="consolas", key='-OUTPUT-')]],
        [sg.Button('Transform'), sg.Button('Quit')]
    ]

    window = sg.Window('Ascii Transformer', layout, finalize=True)
    window['-SLIDER-'].bind('<ButtonRelease-1>', ' Release')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        elif event == "Choose photo":
            file_path = filedialog.askopenfilename()
            if file_path != "":
                image = Image.open(file_path)
                image = image.resize(image.size, resample=Image.Resampling.BICUBIC)
                photo_image = ImageTk.PhotoImage(image=image)
                window["-IMAGE-"].update(data=photo_image)

        elif event == '-SLIDER- Release':
            height = image.size[1]
            width = image.size[0]
            resolution_decrease = values['-SLIDER-']
            img = image.resize((math.floor(width / resolution_decrease), math.floor(height / resolution_decrease)), resample=Image.Resampling.BICUBIC)
            photo_img = ImageTk.PhotoImage(image=img)
            window["-IMAGE-"].update(data=photo_img)

        elif event == 'Transform':
            height = image.size[1]
            width = image.size[0]
            img = image.resize((math.floor(width / resolution_decrease), math.floor(height / resolution_decrease)), resample=Image.Resampling.BICUBIC)
            output = window["-OUTPUT-"]
            output.update("")
            print_ascii(img, output)

    window.close()

def console_app():
    file_path = filedialog.askopenfilename()
    img = Image.open(file_path)
    img.show()

    height = img.size[1]
    width = img.size[0]

    resolution_decrease = 2

    img = img.resize((math.floor(width / resolution_decrease), math.floor(height / resolution_decrease)), resample=Image.Resampling.BICUBIC)
    img.show()

    print_ascii(img)

def print_ascii(img, output=None):
    height = img.size[1]
    width = img.size[0]

    px = img.load()

    for y in range(height):
        line = ""
        for x in range(width):
            pixel = px[x, y]
            r, g, b = pixel[0], pixel[1], pixel[2]
            grayscale = get_grayscale(r, g, b)
            line += get_char(grayscale)
        if output != None:
            if output.get() == "":
                output.update(line)
            else:
                output.update(output.get() + "\n" + line)
        else:
            print(line)

app()