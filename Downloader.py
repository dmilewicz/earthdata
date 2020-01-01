import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer

import tarfile

import os
import numpy as np
# File manipulation
from glob import glob
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio as rio
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

import cv2
import libtiff

from matplotlib import pyplot as plt

import re

LANDSAT_8_PATTERN = re.compile('L(C)(\d\d)_(L\d\w\w)_(\d{3})(\d{3})_(\d{8})_(\d{8})_(\d\d)_([TR]+\d*)')

class SatelliteImage():
    def __init__(self, product_id):
        self.__process_product_id(product_id)

        self.print_metadata()

    def __process_product_id(self, product_id):
        self.product_id = product_id
        m = re.search(LANDSAT_8_PATTERN, product_id)

        if not m:
            raise ValueError("Incorrectly formatted product ID")

        self.sensor = m.group(1)
        self.satellite = m.group(2)
        self.correction_level = m.group(3)
        self.wrs_path = m.group(4)
        self.wrs_row = m.group(5)
        self.acquisition_year_str = m.group(6)
        self.processing_year_str = m.group(7)
        self.collection_number = m.group(8)
        self.collection_category = m.group(9)

    def print_metadata(self):
        print(self.product_id)
        print('\tsensor: ' + self.sensor)
        print('\tsatellite: ' + self.satellite)
        print('\tcorrection_level: ' + self.correction_level)
        print('\twrs_path: ' + self.wrs_path)
        print('\twrs_row: ' + self.wrs_row)
        print('\tacquisition_year: ' + self.acquisition_year_str)
        print('\tprocessing_year: ' + self.processing_year_str)
        print('\tcollection_number: ' + self.collection_number)
        print('\tcollection_category: ' + self.collection_category)








# Initialize a new API instance and get an access key
# api = landsatxplore.api.API('dmilewicz', 'Spartan117RC1136##')
# ee = EarthExplorer('dmilewicz', 'Spartan117RC1136##')

# Request
# scenes = api.search(
#     dataset='LANDSAT_8_C1',
#     latitude=38.038826,
#     longitude=-122.661647,
#     start_date='2019-01-01',
#     end_date='2019-12-01',
#     max_cloud_cover=10)

# print('{} scenes found.'.format(len(scenes)))

# print(scenes[0].keys())

# for scene in scenes:
#     print(scene['entityId'])


# ee.download(scenes[0]['entityId'], output_dir='./data')

# api.logout()
# ee.logout()

# tt = tarfile.open("data/LC08_L1TP_045033_20190102_20190130_01_T1.tar.gz", 'r')

# tt.extractall("data/LC08_L1TP_045033_20190102_20190130_01_T1")

# print(sorted(glob("./data/L*/*.TIF")))
tifs = sorted(glob("./data/L*/*.TIF"))


# ep.plot_bands(landsat_band4[0],
#               title="Landsat Cropped Band 4\nColdsprings Fire Scar",
#               scale=False)

# plt.show()
outfile = "data/output.tif"

land_stack, land_meta = es.stack(tifs, outfile)


with rio.open(outfile) as src:
    print(src.profile)
    landsat_post_fire = src.read()


band_titles = ["Band 1", "Blue", "Green", "Red", "NIR",
               "Band 6", "Band7"]
band_titles = ["Blue", "Green", "Red"]
# ep.plot_bands(landsat_post_fire,
#               title=band_titles, cbar=False)
# plt.show()

# ep.plot_rgb(landsat_post_fire,
#             rgb=[3, 2, 1],
#             stretch=True,
#             str_clip=4,
#             title="RGB Composite Image\n clip4")

# ep.plot_rgb(landsat_post_fire,
#             rgb=[3, 2, 1],
#             stretch=True,
#             str_clip=10,
#             title="RGB Composite Image\n clip 1")



ep.hist(landsat_post_fire, colors=['b', 'g', 'r'], title=band_titles, cols=3, figsize=(8,3), hist_range=(5000,10000))



plt.show()

# im_b = cv2.imread('data/LC08_L1TP_045033_20190102_20190130_01_T1/LC08_L1TP_045033_20190102_20190130_01_T1_B1.TIF', cv2.IMREAD_GRAYSCALE)
# im_g = cv2.imread('data/LC08_L1TP_045033_20190102_20190130_01_T1/LC08_L1TP_045033_20190102_20190130_01_T1_B2.TIF', cv2.IMREAD_GRAYSCALE)
# im_r = cv2.imread('data/LC08_L1TP_045033_20190102_20190130_01_T1/LC08_L1TP_045033_20190102_20190130_01_T1_B3.TIF', cv2.IMREAD_GRAYSCALE)

# im4 = cv2.merge([im_r, im_g, im_b])

# ims = cv2.resize(im4, (800,800))

# hist = cv2.calcHist([im_b],['b'], None, [256], [0,256])
# plt.plot(hist,['b'])
# plt.hist(im_r.ravel(), 256, [0,256])
# plt.hist(im_g.ravel(), 256, [0,256])
# plt.hist(im4, ['b', 'g', 'r'], 256, [0,256])

# plt.show()

# cv2.imshow('image', im4)
# cv2.waitKey(0)


# SatelliteImage('LC08_L1TP_045033_20190102_20190130_01_T1')