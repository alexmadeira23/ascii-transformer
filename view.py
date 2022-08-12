from PIL import Image, ImageTk
from tkinter import filedialog
import PySimpleGUI as sg
import cv2
from threading import Thread
from logic import *

sg.theme('GrayGrayGray')

SELECT = "Select image"
TRANSFORM = "Transform image"
WEBCAM = "Webcam"
QUIT = "Quit"

RESOLUTION = "-RESOLUTION-"
LIGHT = "-LIGHT-"
INVERT = "Invert"
IMAGE = "-IMAGE-"
OUTPUT = "-OUTPUT-"


def app():

    def choose_image_action():
        global current_image
        file_path = filedialog.askopenfilename()
        if file_path != "":
            current_image = Image.open(file_path)
            thumbnail = current_image.copy()
            thumbnail.thumbnail((200, 1000), resample=Image.Resampling.BICUBIC)
            photo_image = ImageTk.PhotoImage(image=thumbnail)
            window[IMAGE].update(data=photo_image)

    def resolution_release_action():
        global res_decrease
        res_decrease = values[RESOLUTION]

    def transform_image_action():
        global current_image
        global res_decrease
        if current_image != None:
            copy = current_image.copy()
            copy.thumbnail(get_new_size(current_image.size,
                           res_decrease), resample=Image.Resampling.BICUBIC)
            text = image_to_text(copy)
            window[OUTPUT].update(text)
        else:
            sg.popup("You need to select an image first!", no_titlebar=True,
                     button_type=5, auto_close=True, auto_close_duration=1)

    def webcam_action():
        global webcam_on
        if not webcam_on:
            webcam_on = True
            Thread(target=lambda: webcam_job(
                window[OUTPUT], show_video=False), daemon=True).start()
        else:
            webcam_on = False

    # create class to store every setting called Settings
    global res_decrease
    global webcam_on
    global current_image
    res_decrease = 1
    webcam_on = False
    current_image = None

    layout = [
        [sg.Text("Resolution decrease:", pad=((0, 0), (15, 0)), justification="center"),
         sg.Slider(range=(1, 100), expand_x=True, orientation="h", key=RESOLUTION)],
        [sg.Text("Light:", pad=((0, 0), (15, 0)), justification="center"),
         sg.Slider(range=(1, 20), expand_x=True, orientation="h", key=LIGHT)],
        [sg.Button(INVERT, expand_x=True,)],
        [sg.Image(size=(200, 200), key=IMAGE),
         sg.Multiline(size=(100, 20), disabled=True, expand_x=True,
                      expand_y=True, background_color="black", text_color="white", font="consolas", key=OUTPUT)],
        [sg.Button(SELECT, expand_x=True)],
        [sg.Button(TRANSFORM, expand_x=True),
         sg.Button(WEBCAM, expand_x=True), sg.Button(QUIT, expand_x=True)]
    ]

    window = sg.Window('Ascii Transformer', layout,
                       resizable=True, finalize=True)
    window.Maximize()
    window[RESOLUTION].bind('<ButtonRelease-1>', ' Release')
    window[LIGHT].bind('<ButtonRelease-1>', ' Release')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == QUIT:
            break

        elif event == SELECT:
            choose_image_action()

        elif event == RESOLUTION + ' Release':
            resolution_release_action()

        elif event == LIGHT + ' Release':
            print('Light')

        elif event == INVERT:
            print('Invert')

        elif event == TRANSFORM:
            transform_image_action()

        elif event == WEBCAM:
            webcam_action()

    window.close()


def webcam_job(output=None, show_video=False):
    global res_decrease
    global webcam_on
    cam = cv2.VideoCapture(0)

    while webcam_on:
        ret, frame = cam.read()

        if not ret:
            print("failed to grab frame")
            break

        flipped = cv2.flip(frame, 1)

        if show_video:
            cv2.imshow("Camera", flipped)

        image = Image.fromarray(flipped)
        image.thumbnail(get_new_size(image.size, res_decrease),
                        resample=Image.Resampling.BICUBIC)
        text = image_to_text(image)
        output.update(text)

        cv2.waitKey(1)

    cam.release()
    cv2.destroyAllWindows()


def get_new_size(size, res_decrease):
    return (math.floor(size[0] / res_decrease), math.floor(size[1] / res_decrease))


def main():
    app()


if __name__ == "__main__":
    main()
