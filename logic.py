import math

CHARS = ".'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

MAX_INTENSITY = 255

RED_CONTRIBUTION = 0.3
GREEN_CONTRIBUTION = 0.59
BLUE_CONTRIBUTION = 0.11


def get_grayscale(r, g, b):
    return RED_CONTRIBUTION * r + GREEN_CONTRIBUTION * g + BLUE_CONTRIBUTION * b


class Settings:

    def __init__(self):
        self._resolution = 1
        self._inverted = False
        self._chars = ' ' + CHARS
        self._webcam_on = False
        self._current_image = None

    def switch_webcam(self):
        self._webcam_on = not self._webcam_on

    def change_light(self, value):
        spaces = ''
        for _ in range(value):
            spaces = spaces + ' '
        if self._inverted:
            self._chars = CHARS + spaces
        else:
            self._chars = spaces + CHARS

    def invert(self):
        self._inverted = not self._inverted
        self._chars = self._chars[::-1]

    def image_to_text(self, img):
        text = ""

        width = img.size[0]
        height = img.size[1]

        px = img.load()

        for y in range(height):
            line = ""

            for x in range(width):
                pixel = px[x, y]
                r, g, b = pixel[0], pixel[1], pixel[2]
                grayscale = get_grayscale(r, g, b)
                line += self.__get_char(grayscale)

            if text == "":
                text = text + line
            else:
                text = text + "\n" + line

        return text

    def __get_char(self, v):
        chars = self._chars
        chars_size = len(chars)
        index = math.floor(v * (chars_size - 1) / MAX_INTENSITY)
        return chars[index]
