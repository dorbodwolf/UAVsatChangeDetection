#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 16:35
# @Author  : Deyu
# @Site    : 
# @File    : Image.py
# @Software: PyCharm Community Edition

from osgeo import gdal, osr
import os


def reprojection(geo_dem):
    """
    gdal reprojection
    :param dem:
    :return:
    """
    cmd = "gdalwarp -t_srs '+proj=utm +zone=43N +datum=WGS84' -dstnodata -9999 " \
          "-overwrite {} {}_toUTM.tif".format(geo_dem, geo_dem[:-4])
    os.system(cmd)

def resampling(utm_dem):
    """
    down sampling dem data for better visualize
    :param utm_dem:
    :return:
    """
    cmd = "gdal_translate -tr 500 500 -r cubic -a_nodata 0 " \
          "-stats {} {}_resamp.tif".format(utm_dem, utm_dem[:-4])
    os.system(cmd)


def img2array(img):
    """
    read dems to array by gdal
    :param imgfn path of geotiff
    :return narray of geotiff
    """
    img_data = gdal.Open(img)
    img_array = img_data.ReadAsArray()
    return img_array

def read_tif_metadata(tifffile):
    """
    read tiff imggt
    :param tifffile:
    :return:
    """
    imgds = gdal.Open(tifffile)
    imggt = imgds.GetGeoTransform()
    print('raster geotransform coeffs:', imggt[0], imggt[1], imggt[2], imggt[3], imggt[4], imggt[5])
    band = imgds.GetRasterBand(1)
    b = band.ReadAsArray()
    return imggt

def array2rasterUTM(newRasterfn, panTransform, array):
    """
    :param newRasterfn:
    :param panTransform: imggt
    :param array:
    :return:
    """
    cols = array.shape[1]
    rows = array.shape[0]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((panTransform[0], panTransform[1], panTransform[2], panTransform[3],
                               panTransform[4], panTransform[5]))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(32652) #utm 52n
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

def array2rasterwgs84(newRasterfn, panTransform, array):
    """

    :param newRasterfn:
    :param panTransform: imggt
    :param array:
    :return:
    """
    cols = array.shape[1]
    rows = array.shape[0]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((panTransform[0], panTransform[1], panTransform[2], panTransform[3],
                               panTransform[4], panTransform[5]))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

if __name__ == '__main__':
    pass