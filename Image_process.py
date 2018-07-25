#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 16:39
# @Author  : Deyu Tian
# @Site    : 
# @File    : Image_process.py
# @Software: PyCharm Community Edition

import cv2
import math
import numpy as np

def draw_hist(impath):
    """

    :param impath:
    :return:
    """
    img = cv2.imread(impath)
    h = np.zeros((300, 256, 1))

    bins = np.arange(256).reshape(256, 1)
    color = [(255, 0, 0)]

    hist_item = cv2.calcHist(img, 0, None, [256], [0, 255])
    cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
    hist = np.int32(np.around(hist_item))
    pts = np.column_stack((bins, hist))
    cv2.polylines(h, [pts], False, color)

    h = np.flipud(h)

    cv2.imshow('colorhist', h)
    cv2.waitKey(0)
    pass

def neibour_8_grab():
    pass

def neibour_4_grab():
    pass

def rescaler():
    pass

def unimodal_thre_rosin():
    """
    rosin's methods
    :return:
    """
    pass

def unimodal_thre_T_point():
    """
    T-point algrithom
    :return:
    """
    pass

def bimodal_threshood():
    pass

def sobel(src, kernel_size):
    """
    :param: src: input lumination grayscale image
    :param:kernel_size: 1 3 5 7
    :return: output gradients
    """
    if kernel_size != 1 or kernel_size != 3 or kernel_size != 5 or kernel_size != 7:
        print("INPUT Params ERROR: kernel_size must be 1 or 3 or 5 or 7!")
    grad_x = cv2.Sobel(src,-1, 1, 0, ksize=kernel_size)
    grad_y = cv2.Sobel(src,-1, 0, 1, ksize=kernel_size)
    grad = cv2.Sobel(src,-1, 1, 1, ksize=kernel_size)
    grad_bi = math.sqrt(math.pow(grad_x, 2) + math.pow(grad_y, 2))
    if grad == grad_bi:
        print("got gradiation without seperate by x and y!")
        return grad
    else:
        print("need seperately x and y grad to generate total gradiation!")
        return grad_bi

def conn_4_neibour(img):
    """

    :param img:
    :return:
    """
    ret, labels = cv2.connectedComponents(img, connectivity=4)

    # Map component labels to hue val
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue == 0] = 0

    cv2.imshow('labeled.png', labeled_img)
    cv2.waitKey()
    pass

