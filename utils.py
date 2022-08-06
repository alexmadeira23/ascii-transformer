import math

black_background = True

#chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.                           "

chars_size = len(chars)
max_intensity = 255

RED_CONTRIBUTION = 0.3
GREEN_CONTRIBUTION = 0.59
BLUE_CONTRIBUTION = 0.11

if black_background:
    chars = chars[::-1]

def get_grayscale(r, g, b):
    return RED_CONTRIBUTION * r + GREEN_CONTRIBUTION * g + BLUE_CONTRIBUTION * b

def get_char(v):
    index = math.floor(v * (chars_size - 1) / max_intensity)
    return chars[index]

def get_new_size(size, res_decrease):
    return (math.floor(size[0] / res_decrease), math.floor(size[1] / res_decrease))

def main():
    pass

if __name__ == "__main__":
    main()