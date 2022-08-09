import math

BLACK_BACKGROUND = True

#CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.          "

CHARS_SIZE = len(CHARS)
MAX_INTENSITY = 255

RED_CONTRIBUTION = 0.3
GREEN_CONTRIBUTION = 0.59
BLUE_CONTRIBUTION = 0.11

if BLACK_BACKGROUND:
    CHARS = CHARS[::-1]

def get_grayscale(r, g, b):
    return RED_CONTRIBUTION * r + GREEN_CONTRIBUTION * g + BLUE_CONTRIBUTION * b

def get_char(v):
    index = math.floor(v * (CHARS_SIZE - 1) / MAX_INTENSITY)
    return CHARS[index]

def image_to_text(img):
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
            line += get_char(grayscale)

        if text == "":
            text = text + line
        else:
            text = text + "\n" + line
    
    return text