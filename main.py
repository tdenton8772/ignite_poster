#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 08:45:43 2018

@author: tdenton
"""

import json
from contextlib import closing
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os

def get_config():
    with closing(open("configuration.json")) as f:
        data = f.read()
        config = json.loads(data)
        return config

def set_headers(im):
    #sets the first header
    header_1 = ImageDraw.Draw(im)
    size_x, size_y = header_1.textsize(config['main']['heading_1']['text'], 
                         ImageFont.truetype(config['main']['heading_1']['font']['font_family'], 
                                 config['main']['heading_1']['font']['font_size']))
    x_pos = (config['main']['poster']['width'] / 2) - (size_x / 2) + config['main']['heading_1']['position']['x'] 
    y_pos = config['main']['heading_1']['position']['y'] + config['main']['poster']['margin']
    header_1.text((x_pos, y_pos), 
                   config['main']['heading_1']['text'], 
                   config['main']['heading_1']['font']['color'], 
                   ImageFont.truetype(config['main']['heading_1']['font']['font_family'], 
                                     config['main']['heading_1']['font']['font_size']))
    
    #sets the second header
    header_2 = ImageDraw.Draw(im)
    size_x, size_y = header_2.textsize(config['main']['heading_2']['text'], 
                         ImageFont.truetype(config['main']['heading_2']['font']['font_family'], 
                                 config['main']['heading_2']['font']['font_size']))
    x_pos = (config['main']['poster']['width'] / 2) - (size_x / 2) + config['main']['heading_2']['position']['x']
    y_pos = config['main']['heading_2']['position']['y'] + config['main']['poster']['margin']
    
    header_1.text((x_pos, y_pos), 
                   config['main']['heading_2']['text'], 
                   config['main']['heading_2']['font']['color'], 
                   ImageFont.truetype(config['main']['heading_2']['font']['font_family'], 
                                     config['main']['heading_2']['font']['font_size']))
    return im

def set_image_one(im):
    img_1 = Image.open(config['main']['image_1']['path'])
    img_1 = img_1.resize((config['main']['image_1']['height'], config['main']['image_1']['width']))
    im.paste(img_1, (config['main']['image_1']['position']['x'] + config['main']['poster']['margin'], config['main']['image_1']['position']['y']+ config['main']['poster']['margin']))
    return im
    
def set_image_two(im):
    img_2 = Image.open(config['main']['image_2']['path'])
    img_2 = img_2.resize((config['main']['image_2']['height'], config['main']['image_1']['width']))
    x_pos = config['main']['poster']['width'] - config['main']['image_1']['width'] - config['main']['poster']['margin']
    im.paste(img_2, (x_pos, config['main']['image_2']['position']['y']+ config['main']['poster']['margin']))
    return im

def process_image(file_name):
    img = Image.open("{}{}".format(config['images']['path'], file_name))
    img = img.resize((config['images']['width'],config['images']['height']))
    if config['images']['caption'] == True:
        name = file_name.split(".")[0].split(" ")
        name = "{} {}".format(name[0], name[1])
        height = int(config['images']['height'] + (config['images']['height'] * .25) + (config['images']['padding']*2))
        width = int(config['images']['width'] + (config['images']['padding']*2))
        base_img = Image.new("RGB", (width, height), config['main']['poster']['background_color'])
        text = ImageDraw.Draw(base_img)
        size_x, size_y = text.textsize(name, 
                         ImageFont.truetype(config['images']['font']['font_family'], 
                                 config['images']['font']['font_size']))
        x_pos = (width / 2) - (size_x / 2)
        y_pos = height - config['images']['padding'] - size_y
        text.text((x_pos, y_pos), 
                  name, 
                  config['images']['font']['color'], 
                  ImageFont.truetype(config['images']['font']['font_family'], 
                                     config['images']['font']['font_size']))
        base_img.paste(img, (config['images']['padding'], config['images']['padding']))
    else:
        name = file_name.split(".")[0].split(" ")
        name = "{} {}".format(name[0], name[1])
        height = int(config['images']['height'] + (config['images']['padding']*2))
        width = int(config['images']['width'] + (config['images']['padding']*2))
        base_img = Image.new("RGB", (width, height), config['main']['poster']['background_color'])
        base_img.paste(img, (config['images']['padding'], config['images']['padding']))    
    
    return base_img
def get_images(im):
    file_names = []
    for root, dirs, files in os.walk(config['images']['path']):  
        for filename in files:
            file_names.append(filename)
    for index, _file in enumerate(file_names):
        img = process_image(_file)
        
        row = index / config['collage_grid']['columns']
        column = index % config['collage_grid']['columns']
        
        x_pos = int(((config['main']['poster']['width'] / config['collage_grid']['columns']) * column) + config['main']['poster']['margin'])
        y_pos = int(config['collage_grid']['start_y'] + (row * config['images']['height']* 1.5) + (config['images']['padding']*2))
        im.paste(img, (x_pos, y_pos))
    return im

if __name__=="__main__":
    config = get_config()
    im = Image.new("RGB", (config['main']['poster']['width'],config['main']['poster']['height']), config['main']['poster']['background_color'])
    im = set_headers(im)
    im = set_image_one(im)
    im = set_image_two(im)
    im = get_images(im)
    im.show()
    im.save(config['file_name'])