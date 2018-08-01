#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/27 14:07
# @Author  : Deyu.Tian
# @Site    : ChangGuang Satellite
# @File    : Potential_changes.py
# @Software: PyCharm Community Edition

import Image
import Image_process
import numpy as np
import sys
import os
import Config


def getPCC(diff_map):
    pass


def normalize_arr(inarr):
    """
    normalize array to [0, 1]
    :param inarr:
    :return:
    """
    return (inarr-np.max(inarr))/(np.max(inarr)-np.min(inarr))
    pass


def diff_map_matrix(imsatpath, imuavpath, w=0):
    """
    use matrix to faster computation
    :param imsatpath:卫星图像的路径
    :param imuavpath:无人机图像的路径
    :param w:搜索邻域块的大小
    :return:两幅图像的差值图
    """
    if w == 0 or w % 2 == 0:
        print("use this function like below: \n"
              "diff_map(imsatpath, imuavpath, w)\n need param w of search box,"
              " its must be odd like 1, 3, 5, 7, 9,.etc.")
        sys.exit(1)
    imsatarr, imuavarr = np.moveaxis(Image.img2array(imsatpath), 0, 2), np.moveaxis(Image.img2array(imuavpath), 0, 2)
    print(imsatarr.shape, imuavarr.shape)
    imsat_desc, imuav_desc = descriptor(imsatarr), descriptor(imuavarr)
    print("features of IMUAV and IMSAT have generated successed, "
          "now compute difference maps with matrix ways!")
    diffarr = np.zeros((imuavarr.shape[0], imuavarr.shape[1]), dtype='f')
    for i in xrange((w-1)/2, imuav_desc.shape[0]-(w-1)/2):
        for j in xrange((w-1)/2, imuav_desc.shape[1]-(w-1)/2):
            xmin, xmax = j-(w-1)/2, j+(w-1)/2+1
            ymin, ymax = i-(w-1)/2, i+(w-1)/2+1
            v = imuav_desc[ymin:ymax, xmin:xmax]
            v_2d = v.reshape((v.shape[0] * v.shape[1]), v.shape[2])
            u = imuav_desc[i, j].reshape(1, imuav_desc[i, j].shape[0])
            diffarr[i, j] = np.min(np.linalg.norm(v_2d - u, axis=0))
    np.save(os.path.join(Config.data, "diffmap.npy"), diffarr)
    return diffarr


def diff_map(imsatpath, imuavpath, w=0):
    """
    input imuav and imsat, return different map
    :param imsatpath:
    :param imuavpath:
    :param w:search box in imsat, w must be odd
    :return:
    """
    if w == 0 or w % 2 == 0:
        print("use this function like below: \n"
              "diff_map(imsatpath, imuavpath, w)\n need param w of search box,"
              " its must be odd like 1, 3, 5, 7, 9,.etc.")
        sys.exit(1)
    imsatarr, imuavarr = np.moveaxis(Image.img2array(imsatpath), 0, 2), np.moveaxis(Image.img2array(imuavpath), 0, 2)
    print(imsatarr.shape, imuavarr.shape)
    imsat_desc, imuav_desc = descriptor(imsatarr), descriptor(imuavarr)
    print("descriptors of IMUAV and IMSAT have generated successed, now compute difference maps!")
    diffarr = np.zeros((imuavarr.shape[0], imuavarr.shape[1]), dtype='f')
    for i in range(imuav_desc.shape[0]):
        for j in range(imuav_desc.shape[1]):
            xmin, xmax = int(j-(w-1)/2), int(j+(w-1)/2+1)
            ymin, ymax = int(i-(w-1)/2), int(i+(w-1)/2+1)
            distsset = []
            for x in range(xmin, xmax):
                for y in range(ymin, ymax):
                    if imuav_desc.shape[1] > x > 0 and 0 < y < imuav_desc.shape[0]:
                        distsset.append(np.linalg.norm(imsat_desc[x, y] - imuav_desc[i, j])) #norm1 of vector/matrix
            diffarr[i, j] = min(distsset)
    np.save(os.path.join(Config.data, "diffmap.npy"), diffarr)
    return diffarr


def descriptor(rgbarr):
    """
    input rgbarr, return relative 36d features set
    :param rgbarr:
    :return:
    """
    desc = np.zeros((rgbarr.shape[0], rgbarr.shape[1], 36), dtype='i')
    print(desc.shape)

    # desc[:, :, 0:9] = Image_process.band_9_neibour_layers(rgbarr[:, :, 0])
    # desc[:, :, 9:18] = Image_process.band_9_neibour_layers(rgbarr[:, :, 1])
    # desc[:, :, 18:27] = Image_process.band_9_neibour_layers(rgbarr[:, :, 2])
    #
    # luminate = rgbarr[:, :, 0] * 0.299 + rgbarr[:, :, 1] * 0.587 + rgbarr[:, :, 2] * 0.114
    # desc[:, :, 27:36] = getIG(np.uint8(luminate)) #if( sdepth == CV_16S && ddepth == CV_32F)
    # print("max of IG is ", np.max(desc[:, :, 27:36]))

    return desc


def getIG(lumimgarr):
    """
    get IG(stacked layers of pixel-and-its 9-neibours' gradients )
    :param lumimgarr:array of Y
    :return:stacked band layers of gradients
    """
    gradient = Image_process.sobel(lumimgarr, kernel_size=7)
    return Image_process.band_9_neibour_layers(gradient)


if __name__ == '__main__':
    diff_map_matrix(Config.ImSat, Config.ImUAV, 11)
    # imsatarr, imuavarr = np.moveaxis(Image.img2array(Config.ImSat), 0, 2), \
    #                      np.moveaxis(Image.img2array(Config.ImUAV), 0, 2)
    # print(imsatarr.shape, imuavarr.shape)
    # descriptor(imsatarr)