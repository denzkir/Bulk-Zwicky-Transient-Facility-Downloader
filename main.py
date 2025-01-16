#### ZBulk Zwicky Transient Facility Frames Downloader v1.1
'''
This script downloads ZTF frames from the IPAC archive and converts them to TIFF format
It also standardizes the image sizes to a square shape as some of the stacking software requires all images to be the same size (e.g. DeepSkyStacker)
The script uses the astropy and PIL libraries to convert the FITS files to TIFF

This script was created by user "MandelbrotEnjoyer"
Frames are provided by IPAC archive
Libraries used: requests, re, os, glob, sys, PIL, astropy, numpy, pandas
'''
import requests
import re
import os
import glob
import sys
from PIL import Image
from astropy.io import fits
import numpy
import pandas as pd

# Search criteria
suffix = 'sciimg.fits'  # Replace with desired suffix based on your needs, sciimg.fits is the science image
filtercode = 'zr'  # Specify the filter code 'zg' or 'zr' or 'zi' 
seeing = "<2" # specify the seeing limit [TO BE IMPLEMENTED]
maglimit = "19"  # (more than) Specify magnitude limit
coords = "65.4868657 +19.5339984"  # Specify the coordinates of your object in RA and DEC in J2000d format 
radius = "0.001"  # specify the radius of the search in degrees
limitAmount = 0  # specify the amount of images to download, set 0 to download all images
expTime = "30"  # specify the exposure time 300 or 30
image_size = "600"  # specify the size of the image in arcsec [ZTF scale is approx 1 arcsec/pixel]
ignore_download = False # set to True to ignore downloading frames

standarize_image_sizes = 550 # set to edge length of the square image you want to create. set to 0 to disable [less than image_size]

def frames_list_lookup(ra, dec, radius):
    filtercode_list = []
    exptime_list = []
    filefracday_list = []
    seeing_list = []
    airmass_list = []
    maglimit_list = []
    ccdid_list = []
    qid_list = []
    imgtypecode_list = []
    field_list = []

    base_url = f'https://irsa.ipac.caltech.edu/ibe/search/ztf/products/sci?POS={ra},{dec}&SIZE={radius}'
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.text
        image_list = data.split("\n")
        header = image_list[0:94]
        del image_list[0:94]
        for i in range(0, len(image_list)):
            image_list_item = image_list[i]
            image_list_item = re.sub('\s+',' ',image_list_item).split(" ")
            try:
                del image_list_item[0]
                del image_list_item[0]
                filtercode_list.append(image_list_item[10])
                exptime_list.append(image_list_item[20])
                filefracday_list.append(image_list_item[21])
                seeing_list.append(image_list_item[22])
                airmass_list.append(image_list_item[23])
                maglimit_list.append(image_list_item[26])
                ccdid_list.append(image_list_item[6])
                qid_list.append(image_list_item[7])
                imgtypecode_list.append(image_list_item[16])
                field_list.append(image_list_item[5])
            except IndexError:
                print("index error, skipping row")

        print(f'Found {len(filtercode_list)} frames')
        print("ZG: " + str(filtercode_list.count("zg")))
        print("ZR: " + str(filtercode_list.count("zr")))
        print("ZI: " + str(filtercode_list.count("zi")))

        return filtercode_list, exptime_list, filefracday_list, seeing_list, airmass_list, maglimit_list, ccdid_list, qid_list, imgtypecode_list, field_list
    else:
        print(f'Failed to retrieve frames: {response.status_code}')
        return None

### Script start ###
ra, dec = coords.split()
filtercode_list, exptime_list, filefracday_list, seeing_list, airmass_list, maglimit_list, ccdid_list, qid_list, imgtypecode_list, field_list = frames_list_lookup(ra, dec, radius)
downloadedFrames = 0
for i in range(0, len(filefracday_list)):
    if limitAmount != 0 and downloadedFrames == limitAmount or ignore_download == True:
        print(f'Downloaded selected amount of frames. Downloaded {downloadedFrames} frames')
        break
    print("File "+str(i)+" out of " + str(len(filefracday_list)))
    if filtercode_list[i] == filtercode and str(exptime_list[i]) == expTime and float(seeing_list[i])<float(2) and float(maglimit_list[i])>float(maglimit):
        year = filefracday_list[i][0:4]
        month = filefracday_list[i][4:6]
        day = filefracday_list[i][6:8]
        fracday = filefracday_list[i][8:len(filefracday_list[i])]
        filefracday = filefracday_list[i]
        qid = qid_list[i]
        imgtypecode = imgtypecode_list[i]
        paddedfield = "000000"[0:int(6-len(field_list[i]))]+field_list[i]
        paddedccdid = "00"[0:int(2-len(ccdid_list[i]))]+ccdid_list[i]
        filtercode = filtercode_list[i]
        base_url = 'https://irsa.ipac.caltech.edu/ibe/data/ztf/products/sci/'
        url = (
        f"{base_url}{year}/{month}{day}/{fracday}/"
        f"ztf_{filefracday}_{paddedfield}_{filtercode}_c{paddedccdid}_{imgtypecode}_q{qid}_{suffix}"
        f"?center={ra},{dec}&size={image_size}arcsec"
        )
        print(url)
        response = requests.get(url)
        with open("output/"+str(filtercode)+" "+str(str(i)+" "+str(day)+"-"+str(month)+"-"+str(year))+".fits", "wb") as f:
            f.write(response.content)
            downloadedFrames = downloadedFrames + 1

#create a list of .fits files in the output directory
fits_files = glob.glob("output/*.fits")

#convert files to TIFF with astropy and PIL
for fits_file in fits_files:
    # skip if name + ".tif" not in os.listdir("output"):
    name, ext = os.path.splitext(fits_file)
    if os.path.exists(name + ".tif"):
        continue
    img = fits.open(fits_file)
    img.info()
    data = img[0].data
    width = data.shape[1]
    height = data.shape[0]
    outputArray = numpy.array(data, dtype=numpy.int16)
    output = Image.fromarray(outputArray.reshape((height, width)), "I;16")
    output.save(name + ".tif")
    img.close()

tif_files = glob.glob("output/*.TIF")

if standarize_image_sizes != 0:
    sizePx = standarize_image_sizes
    path = 'output/' 
    # create a list of .tif files in the output directory.
    tif_files = os.listdir(path)
    # ensure all files are .tif
    tif_files = [str(path) + tif_file for tif_file in tif_files if tif_file.endswith(".tif")]
    print("Number of images: ", len(tif_files))
    # check size of each image and remove last rows and columns of pixels so every image is in the desired size.
    image_sizes = []
    for tif_file in tif_files:
        name, ext = os.path.splitext(tif_file) #
        img = Image.open(tif_file)
        width, height = img.size
        if width < sizePx or height < sizePx:
            os.remove(tif_file)
        else:
            img = img.crop((0, 0, sizePx, sizePx))
            img.save(path+"Standarized_size_"+name.split("/")[1] + ".tif") # Temporary fix
            image_sizes.append([name, width, height])