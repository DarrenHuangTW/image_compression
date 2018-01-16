# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:19:39 2018

@author: Darren Huang
"""

# =============================================================================
# Upload a list of images and download both original and compressed versions.
# Mega Folder -- img_list.txt
#             -- original_image_folder
#             -- compressed_image_folder
# =============================================================================

import os
import urllib
import tinify
import sys
import csv


def img_downloader(imglist, directory):
    """
    imglist: a text file composed of all images that are going to be downloaded
    directory: create a folder to store the downloaded images
    """
    f = open('img_list.txt', 'r', encoding='utf-8')
    img_list = f.read().splitlines()
    f.close()
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    os.chdir(directory)
    
    for imgurl in img_list:
        img_name = imgurl.split('/')[-1]
        unicode_imgurl = imgurl.replace(img_name, urllib.parse.quote(img_name))
    
        f = open(img_name, 'wb')
        f.write(urllib.request.urlopen(unicode_imgurl).read())
        f.close()
        
    file_size()
    
def get_script_path():
    """Get the directory of current running script"""
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def img_compressor(ori_dir, comp_dir, key):
    """
    ori_dir: the folder of original quality images
    comp_dir: the destination of downloaded compressed images
    """
    tinify.key = key
    
    os.chdir(get_script_path())
    if not os.path.exists(comp_dir):
        os.makedirs(comp_dir)

    original_image_folder = os.path.abspath(ori_dir)
    compressed_image_folder = os.path.abspath(comp_dir)
    
    os.chdir(compressed_image_folder)
    for img in os.listdir(original_image_folder):
        img_path = original_image_folder+"\\" +img
        try:
            source = tinify.from_file(img_path)
            source.to_file("compressed_"+img)
        except:
            file = open('failed.txt', 'a', encoding = 'utf-8')        
            file.write("failed: {} \n".format(img))     
            file.close()
            
    file_size()

def file_size():
    csv_list = []
    for filename in os.listdir(os.getcwd()):
        filesize = os.path.getsize(filename)
        if os.path.isfile(filename):
            filetype = filename.split('.')[-1]
        else:
            filetype = 'folder'
        csv_list.append([filename, filesize, filetype])
    
    csv = open('filesize.csv', 'w', encoding='utf-8')
    csv.write("file_name, file_size, file_type\n")
    for fn, fs, ft in csv_list:
        csv.write("{},{},{}\n".format(fn, fs, ft))

                    
key = 'C6DN694NX0iL1mKjRj6reDCKTXtFMtqP'    #Get your own API key at https://tinypng.com/developers
img_downloader("img_list.txt", "original_images")
img_compressor("original_images", "compressed_images", key) 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
