# -*- coding: UTF-8 -*-

import numpy as np
import freetype
import copy
import random
import cv2
import os

from background_generator import BackgroundGenerator
from computer_text_generator import ComputerTextGenerator
from affine_transform_generator import AffineTransformGenerator
from random_crop_generator import RandomCropGenerator


def generate_from_tuple(t):
    """
        Same as generate, but takes all parameters as one tuple
    """

    data_generator(*t)

def data_generator(index=0, text=None, language=None, out_dir=None, width=32, height=32,
                   extension='jpg', skewing_angle=0, blur=0, background_type=0, distorsion_type=0,
                   name_format=0):
    '''
    draw chinese(or not) text with ttf
    :param image:     image(numpy.ndarray) to draw text
    :param pos:       where to draw text
    :param text:      the context, for chinese should b e unicode type
    :param text_size: text size
    :param text_color:text color
    :return:          image
    '''

    if background_type == 0:
        background = BackgroundGenerator.gaussian_noise(height + 5, width + 5)
    elif background_type == 1:
        background = BackgroundGenerator.plain_white(height + 5, width + 5)
    else:
        background = BackgroundGenerator.picture()
    # print ('background', index)
    pos = (3, 3)
    text_size = 32
    text_color = [0, 0, 0]
    image, font = ComputerTextGenerator().draw_text(background, language, pos, text, text_size, text_color)

    if image is None or font is None:
        return

    # skewing image
    if skewing_angle > 0:
        if len(image.shape) == 3:
            row, col, ch = image.shape
        else:
            row, col = image.shape

        M = cv2.getRotationMatrix2D((col / 2, row / 2), skewing_angle, 1)
        skewing_img = cv2.warpAffine(image, M, (col, row),
                                     borderMode=cv2.BORDER_REPLICATE,
                                     flags=cv2.INTER_LINEAR)
    else:
        skewing_img = image

    # Affine transform
    if distorsion_type == 0:
        transform_img = skewing_img
    if distorsion_type == 1:
        transform_img = AffineTransformGenerator().right(skewing_img)
    elif distorsion_type == 2:
        transform_img = AffineTransformGenerator().left(skewing_img)

    # Gaussian Blur
    if blur:
        kernels_size = [3, 5]
        kernel_size = kernels_size[random.randint(0, 1)]
        sigma = random.uniform(0, 3)
        blur_img = cv2.GaussianBlur(transform_img, (kernel_size, kernel_size), sigma)
    else:
        blur_img = transform_img

    # normalize the image size
    if language == 'cn':
        final_res_img = RandomCropGenerator().crop(blur_img, height, width)
    else:
        final_res_img = cv2.resize(blur_img, (height, width), interpolation=cv2.INTER_LINEAR)

    fontname = os.path.basename(font).split('.')[0]
    if text == '/':
        text = 'slash'
    if name_format == 0:
        image_name = '{}_{}_{}.{}'.format(text, fontname, str(index), extension)
    elif name_format == 1:
        image_name = '{}_{}_{}.{}'.format(str(index), fontname, text, extension)
    elif name_format == 2:
        image_name = '{}.{}'.format(str(index), extension)
    else:
        print('{} is not a valid name format. Using default.'.format(name_format))
        image_name = '{}_{}_{}.{}'.format(text, fontname, str(index), extension)

    path = os.path.join(out_dir.encode('utf-8'), image_name)
    cv2.imwrite(path, final_res_img)



if __name__ == '__main__':
    # just for test

    for i in range(100):
        line = '亡'

        color_ = [0, 0, 0]  # Green
        pos = (3, 3)
        text_size = 24

        # ft = put_chinese_text('wqy-zenhei.ttc')
        # ft = put_chinese_text('fonts/cn/simhei.ttf')
        data_generator(language='cn', out_dir='./output/你/', text=line, background_type=2,
                          blur=True, distorsion_type=2, skewing_angle=10)
        # image = cv2.resize(image, (32, 32), interpolation=cv2.INTER_LINEAR)
        # print image
        # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # cv2.imshow('ss', image)
        # cv2.waitKey(0)
