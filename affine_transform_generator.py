import cv2
import math
import random
import os
import numpy as np

class AffineTransformGenerator(object):
    def left(self, skewing_img):
        # to the left

        if len(skewing_img.shape) == 3:
            row, col, ch = skewing_img.shape
        else:
            row, col = skewing_img.shape

        points_1 = np.float32([[0, 0], [0, row - 1], [col - 1, row - 1]])
        points_2 = np.float32([[0, row * random.uniform(0, 0.4)],
                               [col * random.uniform(0, 0.27), row * random.uniform(0.85, 0.95)],
                               [col - 1, row * random.uniform(0.7, 0.95)]])
        M = cv2.getAffineTransform(points_1, points_2)
        transform_img = cv2.warpAffine(skewing_img, M, (col, row),
                                       borderMode=cv2.BORDER_REPLICATE,
                                       flags=cv2.INTER_LINEAR)

        return transform_img

    def right(self, skewing_img):
        # to the right

        if len(skewing_img.shape) == 3:
            row, col, ch = skewing_img.shape
        else:
            row, col = skewing_img.shape

        points_1 = np.float32([[0, 0], [col - 1, 0], [0, row - 1]])
        points_2 = np.float32([[col * random.uniform(0, 0.35), row * random.uniform(0, 0.35)],
                               [col * random.uniform(0.85, 0.95), row * random.uniform(0, 0.27)],
                               [col * random.uniform(0, 0.27), row * random.uniform(0.85, 0.95)]])
        M = cv2.getAffineTransform(points_1, points_2)
        transform_img = cv2.warpAffine(skewing_img, M, (col, row),
                                       borderMode=cv2.BORDER_REPLICATE,
                                       flags=cv2.INTER_LINEAR)

        return transform_img