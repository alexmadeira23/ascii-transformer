from PIL import Image
from tkinter import filedialog
import PySimpleGUI as sg
import cv2
import math
from threading import Thread
from logic import Settings

THEME = 'GrayGrayGray'

SELECT = 'Select image'
TRANSFORM = 'Transform image'
WEBCAM = 'Webcam'
QUIT = 'Quit'
INVERT = 'Invert'
RESOLUTION = 'Resolution decrease:'
LIGHT = 'Light:'

RESOLUTION_KEY = '-RESOLUTION-'
LIGHT_KEY = '-LIGHT-'
OUTPUT_KEY = '-OUTPUT-'

TEXT_SIZE = 15
TEXT_PAD = ((0, 0), (16, 0))
SLIDER_RANGE = (1, 100)


sg.theme(THEME)


def app():

    # Auxiliary functions

    def choose_image_action():
        settings.turn_webcam_off()
        file_path = filedialog.askopenfilename()
        if file_path != '':
            settings._current_image = Image.open(file_path)
            transform_image()

    def resolution_release_action():
        settings._resolution = values[RESOLUTION_KEY]
        transform_image()

    def light_release_action():
        settings.change_light(int(values[LIGHT_KEY]))
        transform_image()

    def invert_action():
        settings.invert()
        transform_image()

    def webcam_action():
        if not settings._webcam_on:
            settings.turn_webcam_on()
            Thread(target=lambda: webcam_job(
                window[OUTPUT_KEY], settings, show_video=False), daemon=True).start()
        else:
            settings.turn_webcam_off()

    def transform_image():
        current_image = settings._current_image
        resolution = settings._resolution
        webcam_off = not settings._webcam_on
        if current_image != None and webcam_off:
            copy = current_image.copy()
            copy.thumbnail(get_new_size(current_image.size,
                           resolution), resample=Image.Resampling.BICUBIC)
            text = settings.image_to_text(copy)
            window[OUTPUT_KEY].update(text)

    # App procedure

    settings = Settings()

    layout = [
        [sg.Text(RESOLUTION, size=TEXT_SIZE, pad=TEXT_PAD, justification='center'),
         sg.Slider(range=SLIDER_RANGE, expand_x=True, orientation='h', key=RESOLUTION_KEY)],

        [sg.Text(LIGHT, size=TEXT_SIZE, pad=TEXT_PAD, justification='center'),
         sg.Slider(range=SLIDER_RANGE, expand_x=True, orientation='h', key=LIGHT_KEY)],

        [sg.Button(INVERT, expand_x=True,)],

        [sg.Multiline(disabled=True, expand_x=True, expand_y=True,
                      background_color='black', text_color='white', font='consolas', key=OUTPUT_KEY)],

        [sg.Button(SELECT, expand_x=True), sg.Button(
            WEBCAM, expand_x=True), sg.Button(QUIT, expand_x=True)]
    ]

    window = sg.Window(
        title='Ascii Transformer',
        layout=layout,
        resizable=True,
        finalize=True
    )

    window.Maximize()
    window[RESOLUTION_KEY].bind('<ButtonRelease-1>', ' Release')
    window[LIGHT_KEY].bind('<ButtonRelease-1>', ' Release')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == QUIT:
            break

        elif event == SELECT:
            choose_image_action()

        elif event == RESOLUTION_KEY + ' Release':
            resolution_release_action()

        elif event == LIGHT_KEY + ' Release':
            light_release_action()

        elif event == INVERT:
            invert_action()

        elif event == WEBCAM:
            webcam_action()

        else:
            continue

    window.close()


def webcam_job(output=None, settings=None, show_video=False):
    cam = cv2.VideoCapture(0)

    while settings._webcam_on:
        ret, frame = cam.read()

        if not ret:
            print('failed to grab frame')
            break

        flipped = cv2.flip(frame, 1)

        if show_video:
            cv2.imshow('Camera', flipped)

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


if __name__ == '__main__':
    main()
