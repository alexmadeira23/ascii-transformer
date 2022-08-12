import math

CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."

class Settings:

    def __init__(self):
        self._resolution = 1
        self._inverted = False
        self._chars = CHARS + ' '

    def set_resolution(self, res):
        self._resolution = res

    def get_chars_size(self):
        return len(self._chars)

    def change_light(self, value: int):
        spaces = ''
        for _ in range(value):
            spaces = spaces + ' ' 
        if self._inverted:
            self._chars = spaces + CHARS
        else:
            self._chars = CHARS + spaces

    def invert(self):
        self._inverted = not self._inverted
        self._chars = self._chars[::-1]

BLACK_BACKGROUND = True

#CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.          "

CHARS_SIZE = len(CHARS)
MAX_INTENSITY = 255

RED_CONTRIBUTION = 0.3
GREEN_CONTRIBUTION = 0.59
BLUE_CONTRIBUTION = 0.11

if BLACK_BACKGROUND:
    CHARS = CHARS[::-1]

def get_grayscale(r, g, b):
    return RED_CONTRIBUTION * r + GREEN_CONTRIBUTION * g + BLUE_CONTRIBUTION * b

def get_char(settings: Settings, v):
    chars = settings._chars
    chars_size = len(chars)
    index = math.floor(v * (chars_size - 1) / MAX_INTENSITY)
    return chars[index]

def image_to_text(settings: Settings, img):
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
            line += get_char(settings, grayscale)

        if text == "":
            text = text + line
        else:
            text = text + "\n" + line
    
    return text