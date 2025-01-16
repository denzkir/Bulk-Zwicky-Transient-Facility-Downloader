# Bulk Zwicky Transient Facility Frames Downloader 
## A simple script to search for and download ZTF frames from the IPAC archive, convert them to TIFF, and standardize their sizes for stacking.

## I have always wondered what ZTF images would look like when stacked in each separate ZTF filter: Sloan g', Sloan r', Sloan i', and then converted to RGB. For this task, I needed a way to list all images ZTF have produced for a part of the sky, download them, cut them to the same size, and do all of it with a selection of parameters such as exposure time, magnitude limit, etc. So here it is, along with a gallery section below if you want to see images I produced with this script.

## Features

#### __1. Bulk downloading FITS files from the ZTF archive by specifying:__
#### 1.1 J2000d Coordinates: coordinates you want to use as the center of the search region.
#### 1.2 Radius of search: This value along with coordinates will determine the polygon in the sky that is required to be in the image in order for it to be downloaded.
#### 1.3 Filter zr, zg or zi
#### 1.4 Minimum acceptable mag limit for frames: It is useful for determining the quality of each frame as mag limit is impacted by factors like humidity, moon phase, etc. when the frame was captured.
#### 1.5 Exposure Time: Most ZTF images are 30s frames, but you can change it to 300s as ZTF also generates them from time to time.
#### 1.6 (Optional) Amount of frames to download: If it is set to "0", the script will download all frames that meet the requirements.
#### 2. __Automatic conversion of downloaded FITS files into TIF files as it is an easier file format to work with when using image editing software.__
#### 3. __Standardization of image sizes.__ When considering all downloaded images, it is often the case that they will vary in their sizes. For example, most images are 450x450, but some are 451x450 and some are 449x451. I don't know the exact mechanism behind it, but by using "standardize_image_sizes", you can input an edge length of the square. So, for example, you can change the size of all images to 440x440. It is important as, for example, DeepSkyStacker struggles with stacking images with different sizes.

## Installation
1. Clone this repository and install dependencies:
   ```
   pip install -r requirements.txt
2. Ensure you have Python 3, PIL (Pillow), Astropy, Requests, Pandas, and NumPy available in your environment. 

## Usage
1. Edit the variables in main.py (coordinates, radius, exposure time, etc.) to suit your needs.
2. Run the script
3. The script will output your images in the output folder [it will save them as fits, tif, standardized_size tifs]

## Gallery of images I made by using frames extracted with this script:
### M51 galaxy: zg 286x30s, zr 433x30s, zi 70x30s 
### ![image png 68343a859dbcf2863e4772419c24f9e0](https://github.com/user-attachments/assets/cbd57876-5f8f-4edf-bb3c-ddc5803df284)
### M82 galaxy, zg 166x30s, zr 351x30s, zi 2x30s
### ![FINAL_SLABY_BO_SLABY_ALE_NIE_MAM_SILY png f68c7892804931b16ccf1e26ef121b37](https://github.com/user-attachments/assets/ba7803f7-2f99-454e-a1c7-7fc1eb442baf)
### Hubble Deep Field, zr 283x30s. GIF overlays Hubble image of HDF and image made with ZTF data (HDF)
### ![image gif 0e85cf673130e42f9b94caea85d932b4 (1)](https://github.com/user-attachments/assets/d2257bb3-2983-4163-821f-835d6af21134)
### Horse Head Nebula, zg 12x30s, zr 47x30s, 1x30s
### ![image png 3511abcf29ab600d86f795861580ce2f (1)](https://github.com/user-attachments/assets/1b7afcfb-94f8-40d2-94e7-4a2e7af77914)

## Attributions:
1. ZTF Science Data Processing System: Masci et al. (2019)
2. ZTF Technical Specifications and Survey Design: Bellm et al. (2019)
3. Libraries used: re, os, glob, sys, PIL (Pillow), Astropy, NumPy, Pandas  

