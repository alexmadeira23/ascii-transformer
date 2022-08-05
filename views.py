from PIL import Image, ImageTk
from tkinter import filedialog
import PySimpleGUI as sg
import cv2
from threading import Thread
from logic import *

sg.theme('GrayGrayGray') 

res_decrease = 1

def app():
    current_image = None
    global res_decrease

    layout = [
        [sg.Text("Resolution decrease:", pad=((0, 0), (15, 0)), justification="center"), sg.Slider(range=(1, 100), expand_x=True, orientation="h", key='-SLIDER-')],
        [sg.Image(size=(200, 200), key="-IMAGE-"), sg.Multiline(size=(100, 20), disabled=True, expand_x=True, expand_y=True, background_color="black", text_color="white", font="consolas", key='-OUTPUT-')],
        [sg.Button('Choose image', expand_x=True)],
        [sg.Button('Transform image', expand_x=True), sg.Button('Webcam', expand_x=True), sg.Button('Quit', expand_x=True)]
    ]

    window = sg.Window('Ascii Transformer', layout, resizable=True, finalize=True)
    window['-SLIDER-'].bind('<ButtonRelease-1>', ' Release')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        elif event == "Choose image":
            file_path = filedialog.askopenfilename()
            if file_path != "":
                current_image = Image.open(file_path)
                thumbnail = current_image.copy()
                thumbnail.thumbnail((200, 1000), resample=Image.Resampling.BICUBIC)
                photo_image = ImageTk.PhotoImage(image=thumbnail)
                window["-IMAGE-"].update(data=photo_image)

        elif event == '-SLIDER- Release':
            res_decrease = values['-SLIDER-']

        elif event == 'Transform image':
            if current_image != None:
                width = current_image.size[0]
                height = current_image.size[1]
                copy = current_image.copy()
                copy.thumbnail(get_new_size(width, height, res_decrease), resample=Image.Resampling.BICUBIC)
                print_ascii(copy, window["-OUTPUT-"])
            else:
                sg.popup("You need to select an image first!", no_titlebar=True, button_type=5, auto_close=True, auto_close_duration=1)
        
        elif event == "Webcam":
            Thread(target=lambda : webcam(window["-OUTPUT-"]), daemon=True).start()

    window.close()

def print_ascii(img, output=None):
    text = ""

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

        if text == "":
            text = text + line
        else:
            text = text + "\n" + line
        
    if output != None:
        output.update(text)
    else:
        print(text)

def webcam(output=None):

    global res_decrease

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()

        if not ret:
            print("failed to grab frame")
            break
    
        # flip the image
        flip = cv2.flip(frame,1)

        cv2.imshow("test", flip)
        image = Image.fromarray(flip)
        image.thumbnail(get_new_size(image.size[0], image.size[1], res_decrease), resample=Image.Resampling.BICUBIC)
        print_ascii(image, output)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

    cam.release()
    cv2.destroyAllWindows()

def main():
    app()

if __name__ == "__main__":
    main()