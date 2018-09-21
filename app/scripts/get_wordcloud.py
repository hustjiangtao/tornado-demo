# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from wordcloud import WordCloud, ImageColorGenerator
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image


def get_wordcloud(data, mask_path=None, bg_color='white'):
    """
    generate wordcloud with given data
    > get_wordcloud(data='a,b,c,d', mask_path='./bear.png', bg_color='white')
    :param data: str
    :param mask_path: str
    :param bg_color: str
    :return: show image by plt
    """
    if not isinstance(data, str):
        return
    if not mask_path:
        mask_path = './bear.png'

    # read mask image
    mask_image = np.array(Image.open(mask_path))
    # set the wordcloud shape by args mask
    wc = WordCloud(background_color=bg_color, max_words=2000, mask=mask_image, max_font_size=50, random_state=42)
    # generate with text
    wc.generate(data)

    #  create coloring from image
    # image_colors = ImageColorGenerator(image)
    # show the image
    # get a wordcloud with the shape of the given image if a mask was provided
    plt.imshow(wc)
    plt.axis("off")
    plt.figure()
    plt.show()
