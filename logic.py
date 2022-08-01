import math

black_background = True

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

if black_background:
    chars = chars[::-1]

chars_size = len(chars)

max_intensity = 255

def average(lst):
    return sum(lst) / len(lst)

def get_grayscale(r, g, b):
    return 0.3 * r + 0.59 * g + 0.11 * b

def get_char(v):
    index = math.floor(v * (chars_size - 1) / max_intensity)
    return chars[index]

def main():
    print(get_char(254))
    print(get_char(200))
    print(get_char(0))

if __name__ == "__main__":
    main()