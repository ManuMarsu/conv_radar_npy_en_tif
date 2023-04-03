# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:48:07 2023

@author: manuel.collongues
Cerema / Laboratoire de Nancy / ERTD
"""

import numpy as np
import os
from osgeo import gdal, osr
import datetime

def write_geotiff(data, dates, output_folder):
    # Dimensions des données
    num_dates, dim1, dim2 = data.shape

    # Créez un répertoire de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    # Paramètres spatiaux (exemple - à adapter selon vos besoins)
    upper_left_x = -5.842
    upper_left_y = 51.896
    pixel_size = 0.01
    geotransform = (upper_left_x, pixel_size, 0, upper_left_y, 0, -pixel_size)
    projection = osr.SpatialReference()
    projection.ImportFromEPSG(4326)  # WGS84

    # Parcourir les dates et écrire les fichiers GeoTIFF
    for i in range(num_dates):
        date = dates[i]
        print(date)
        j = str(date).replace(":", "_")

        driver2 = gdal.GetDriverByName("GTiff")
        filename = f"{j}.tif"
        dataset2 = driver2.Create(filename, dim2, dim1, 1, gdal.GDT_Int16)
        dataset2.GetRasterBand(1).WriteArray(data[i, :, :])
        
        # Configuration des paramètres spatiaux
        dataset2.SetGeoTransform(geotransform)
        dataset2.SetProjection(projection.ExportToWkt())

        dataset2.FlushCache()
        dataset2 = None


file_paths = ["data", "dates", "miss_dates"]  
data = {}
for file in file_paths:

    data[file] = np.load(f"{file}.npy", allow_pickle=True)
    print(file, list(data[file].shape))

write_geotiff(data["data"], data["dates"], "rasters")
