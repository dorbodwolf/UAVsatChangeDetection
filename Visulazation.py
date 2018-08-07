#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 17:12
# @Author  : Aries
# @Site    : 
# @File    : Visulazation.py
# @Software: PyCharm Community Edition

import Config
import os
import matplotlib.pyplot as plt
import numpy as np



def visul_arr_rgb(arr):
    plt.imshow(arr)  # plotting by columns
    print(np.max(arr), np.min(arr), np.std(arr))
    plt.show()
    pass


def visul_npy(npy):
    arr = np.load(npy)
    plt.imshow(arr)  # plotting by columns
    plt.gray()
    print(np.max(arr), np.min(arr), np.std(arr))
    plt.show()
    pass


if __name__ == '__main__':
    visul_npy(os.path.join(Config.data, "diffmap.npy"))
    pass