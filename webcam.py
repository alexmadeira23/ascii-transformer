import cv2
from PIL import Image
import numpy as np
from views import *

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()

    if not ret:
        print("failed to grab frame")
        break
  
    # flip the image
    flip = cv2.flip(frame,1)

    cv2.imshow("test", flip)
    image = Image.fromarray(flip)
    image.thumbnail(get_new_size(image.size[0], image.size[1], 7), resample=Image.Resampling.BICUBIC)
    print_ascii(image)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()

cv2.destroyAllWindows()