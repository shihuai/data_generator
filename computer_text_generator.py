import numpy as np
import freetype
import copy
import random
import pdb
import cv2
import os

def load_fonts(lang):
    """
        Load all fonts in the fonts directories
    """

    if lang == 'cn':
        return [os.path.join('fonts/cn', font) for font in os.listdir('fonts/cn')]
    else:
        return [os.path.join('fonts/latin', font) for font in os.listdir('fonts/latin')]

class ComputerTextGenerator(object):

    def draw_text(cls, image, language, pos, text, text_size, text_color):
        '''
        draw chinese(or not) text with ttf
        :param image:     image(numpy.ndarray) to draw text
        :param pos:       where to draw text
        :param text:      the context, for chinese should b e unicode type
        :param text_size: text size
        :param text_color:text color
        :return:          image
        '''

        fonts = load_fonts(language)
        idx_list = np.arange(len(fonts))
        random.shuffle(idx_list)
        for idx in idx_list:
            font = fonts[idx]
            cls._face = freetype.Face(font)
            cls._face.set_char_size(text_size * 64)
            metrics = cls._face.size
            ascender = metrics.ascender / 64.0

            # descender = metrics.descender/64.0
            # height = metrics.height/64.0
            # linegap = height - ascender + descender
            ypos = int(ascender)
            hscale = 1.0
            matrix = freetype.Matrix(int(hscale) * 0x10000L, int(0.2 * 0x10000L), \
                                     int(0.0 * 0x10000L), int(1.1 * 0x10000L))
            cur_pen = freetype.Vector()
            pen_translate = freetype.Vector()

            cls._face.set_transform(matrix, pen_translate)
            cls._face.load_char(text)
            glyph_index = cls._face.get_char_index(text.decode('utf-8'))

            if glyph_index == 0:
                continue
            else:
                break

        if idx >= len(fonts):
            return None, None

        if not isinstance(text, unicode):
            text = text.decode('utf-8')

        img = cls._draw_string(image, pos[0], pos[1] + ypos, cur_pen, text, text_color)

        return img, font


    def _draw_string(cls, img, x_pos, y_pos, cur_pen, cur_char, color):
        '''
        draw string
        :param x_pos: text x-postion on img
        :param y_pos: text y-postion on img
        :param text:  text (unicode)
        :param color: text color
        :return:      image
        '''

        prev_char = 0
        pen = freetype.Vector()
        pen.x = x_pos << 6  # div 64
        pen.y = y_pos << 6

        image = copy.deepcopy(img)

        kerning = cls._face.get_kerning(prev_char, cur_char)
        pen.x += kerning.x
        slot = cls._face.glyph
        bitmap = slot.bitmap

        cur_pen.x = pen.x
        cur_pen.y = pen.y - slot.bitmap_top * 64
        image = cls._draw_ft_bitmap(image, bitmap, cur_pen, color)

        pen.x += slot.advance.x

        return image


    def _draw_ft_bitmap(cls, img, bitmap, pen, color):
        '''
        draw each char
        :param bitmap: bitmap
        :param pen:    pen
        :param color:  pen color e.g.(0,0,255) - red
        :return:       image
        '''
        x_pos = pen.x >> 6
        y_pos = pen.y >> 6
        cols = bitmap.width
        rows = bitmap.rows

        glyph_pixels = bitmap.buffer

        for row in range(rows):
            for col in range(cols):
                if glyph_pixels[row * cols + col] != 0:
                    if len(img.shape) == 3:
                        img[y_pos + row][x_pos + col][0] = color[0]
                        img[y_pos + row][x_pos + col][1] = color[1]
                        img[y_pos + row][x_pos + col][2] = color[2]
                    else:
                        img[y_pos + row][x_pos + col] = color[0]

        if y_pos - 5 > 0:
            y_pos -= 5
        else:
            y_pos = 0

        if x_pos - 5 > 0:
            x_pos -= 5
        else:
            x_pos = 0

        image = img[y_pos:y_pos + rows+10, x_pos:x_pos+cols+5]

        return image