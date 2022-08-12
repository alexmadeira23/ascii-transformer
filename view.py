from PIL import Image, ImageTk
from tkinter import filedialog
import PySimpleGUI as sg
import cv2
import math
from threading import Thread
from logic import Settings

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

    # Auxiliary functions

    def choose_image_action():
        file_path = filedialog.askopenfilename()
        if file_path != "":
            settings._current_image = Image.open(file_path)
            thumbnail = settings._current_image.copy()
            thumbnail.thumbnail((200, 1000), resample=Image.Resampling.BICUBIC)
            photo_image = ImageTk.PhotoImage(image=thumbnail)
            window[IMAGE].update(data=photo_image)

    def resolution_release_action():
        settings._resolution = values[RESOLUTION]

    def light_release_action():
        settings.change_light(int(values[LIGHT]))

    def invert_action():
        settings.invert()

    def transform_image_action():
        current_image = settings._current_image
        resolution = settings._resolution
        if current_image != None:
            copy = current_image.copy()
            copy.thumbnail(get_new_size(current_image.size,
                           resolution), resample=Image.Resampling.BICUBIC)
            text = settings.image_to_text(copy)
            window[OUTPUT].update(text)
        else:
            sg.popup("You need to select an image first!", no_titlebar=True,
                     button_type=5, auto_close=True, auto_close_duration=1)

    def webcam_action():
        if not settings._webcam_on:
            settings.switch_webcam()
            Thread(
                target=lambda: webcam_job(window[OUTPUT], settings, show_video=False), daemon=True
            ).start()
        else:
            settings.switch_webcam()

    # App procedure

    settings = Settings()

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

    window = sg.Window(
        title='Ascii Transformer', 
        layout=layout,
        resizable=True, 
        finalize=True
    )
    
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
            light_release_action()

        elif event == INVERT:
            invert_action()

        elif event == TRANSFORM:
            transform_image_action()

        elif event == WEBCAM:
            webcam_action()

    window.close()

def webcam_job(output=None, settings=None, show_video=False):
    cam = cv2.VideoCapture(0)

    while settings._webcam_on:
        ret, frame = cam.read()

        if not ret:
            print("failed to grab frame")
            break

        flipped = cv2.flip(frame, 1)

        if show_video:
            cv2.imshow("Camera", flipped)

        image = Image.fromarray(flipped)
        image.thumbnail(get_new_size(image.size, settings._resolution),
                        resample=Image.Resampling.BICUBIC)
        text = settings.image_to_text(image)
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
