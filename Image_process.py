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


def rgb2hsi(rgb_lwpImg):
    """

    :param rgb_lwpImg: arrays of input RGB Image
    :return:
    """
    rows = int(rgb_lwpImg.shape[0])
    cols = int(rgb_lwpImg.shape[1])
    b, g, r = cv2.split(rgb_lwpImg)
    # 归一化到[0,1]
    b = b / 255.0
    g = g / 255.0
    r = r / 255.0
    hsi_lwpImg = rgb_lwpImg.copy()
    H, S, I = cv2.split(hsi_lwpImg)
    for i in range(rows):
        for j in range(cols):
            num = 0.5 * ((r[i, j]-g[i, j])+(r[i, j]-b[i, j]))
            den = np.sqrt((r[i, j]-g[i, j])**2+(r[i, j]-b[i, j])*(g[i, j]-b[i, j]))
            theta = float(np.arccos(num/den))

            if den == 0:
                    H = 0
            elif b[i, j] <= g[i, j]:
                H = theta
            else:
                H = 2*3.14169265 - theta

            min_RGB = min(min(b[i, j], g[i, j]), r[i, j])
            sum = b[i, j]+g[i, j]+r[i, j]
            if sum == 0:
                S = 0
            else:
                S = 1 - 3*min_RGB/sum

            H = H/(2*3.14159265)
            I = sum/3.0
            # 输出HSI图像，扩充到255以方便显示，一般H分量在[0,2pi]之间，S和I在[0,1]之间
            hsi_lwpImg[i, j, 0] = H*255
            hsi_lwpImg[i, j, 1] = S*255
            hsi_lwpImg[i, j, 2] = I*255
    return hsi_lwpImg


def band_9_neibour_layers_ignoreedge(bandarr):
    """
    drop edge pixels for faster diff map generation
    :param bandarr:
    :return:
    """
    pass
    ul = np.zeros((bandarr.shape[0], bandarr.shape[1]), dtype='f')
    up = np.zeros_like(ul)
    ur = np.zeros_like(ul)
    left = np.zeros_like(ul)
    right = np.zeros_like(ul)
    dl = np.zeros_like(ul)
    down = np.zeros_like(ul)
    dr = np.zeros_like(ul)
    for i in range(1, bandarr.shape[0]-1):
        for j in range(1, bandarr.shape[1]-1):
            ul[i, j] = bandarr[i - 1, j - 1]
            up[i, j] = bandarr[i - 1, j]
            left[i, j] = bandarr[i, j - 1]
            dl[i, j] = bandarr[i + 1, j - 1]
            ur[i, j] = bandarr[i - 1, j + 1]
            right[i, j] = bandarr[i, j+1]
            down[i, j] = bandarr[i + 1, j]
            dr[i, j] = bandarr[i + 1, j + 1]
    #print(np.stack((bandarr, ul, up, ur, left, right, dl, down, dr)).shape)
    returnarr = np.moveaxis(np.stack((bandarr, ul, up, ur, left, right, dl, down, dr)), 0, 2)
    print(returnarr.shape)
    return returnarr

def band_9_neibour_layers(bandarr):
    """
    input band, return stacked layers of pixels' 9-neighbourhood
    :param bandarr:
    :return:
    """
    #print(bandarr.shape[0], bandarr.shape[1])
    ul = np.zeros((bandarr.shape[0], bandarr.shape[1]), dtype='f')
    up = np.zeros_like(ul)
    ur = np.zeros_like(ul)
    left = np.zeros_like(ul)
    right = np.zeros_like(ul)
    dl = np.zeros_like(ul)
    down = np.zeros_like(ul)
    dr = np.zeros_like(ul)
    for i in range(bandarr.shape[0]):
        for j in range(bandarr.shape[1]):
            if i < 1 or j < 1:
                ul[i, j] = -1
            else:
                ul[i, j] = bandarr[i - 1, j - 1]
            if i < 1:
                up[i, j] = -1
            else:
                up[i, j] = bandarr[i - 1, j]
            if j < 1:
                left[i, j] = -1
            else:
                left[i, j] = bandarr[i, j - 1]
            if j < 1 or i == bandarr.shape[0]-1:
                dl[i, j] = -1
            else:
                dl[i, j] = bandarr[i + 1, j - 1]
            if i < 1 or j == bandarr.shape[1]-1:
                ur[i, j] = -1
            else:
                ur[i, j] = bandarr[i - 1, j + 1]
            if j == bandarr.shape[1]-1:
                right[i, j] = -1
            else:
                right[i, j] = bandarr[i, j+1]
            if i == bandarr.shape[0]-1:
                down[i, j] = -1
            else:
                down[i, j] = bandarr[i + 1, j]
            if i == bandarr.shape[0]-1 or j == bandarr.shape[1]-1:
                dr[i, j] = -1
            else:
                dr[i, j] = bandarr[i + 1, j + 1]
    #print(np.stack((bandarr, ul, up, ur, left, right, dl, down, dr)).shape)
    returnarr = np.moveaxis(np.stack((bandarr, ul, up, ur, left, right, dl, down, dr)), 0, 2)
    print(returnarr.shape)
    return returnarr

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
    grad_x = cv2.Sobel(src, -1, 1, 0, ksize=kernel_size)
    grad_y = cv2.Sobel(src, -1, 0, 1, ksize=kernel_size)
    grad = cv2.Sobel(src, -1, 1, 1, ksize=kernel_size)
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


