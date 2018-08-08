import numpy as np
import random
import cv2

class RandomCropGenerator(object):
    def crop(self, image, height, width):
        if len(image.shape) == 3:
            row, col, ch = image.shape
        else:
            row, col = image.shape

        if row < height or col < width:
            image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
        else:
            start_x = random.randint(0, col - width)
            start_y = random.randint(0, row - height)

            image = image[start_y:start_y+height, start_x:start_x+width]

        return image