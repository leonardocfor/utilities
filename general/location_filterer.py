#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Location filterer
Developed by Leonardo Camargo-Forero
https://github.com/leonardocfor
"""

import optparse
import os
import sys
import traceback
from mpl_toolkits.basemap import Basemap
from xml.etree import ElementTree as XML


### Global variables
BOX_FIELDS = [
    'MIN_LAT',
    'MAX_LAT',
    'MIN_LON',
    'MAX_LON'
]
NAME_FIELD_POSITION = 0
LAT_FIELD_POSITION  = 1
LON_FIELD_POSITION  = 2
##############################

def filter(lat,lon):

    """
    Filtering points per selected latitude and longitude
    """
    filters = []
    if lat.count('.') > 1: lat = fix_values(lat)
    if lon.count('.') > 1: lon = fix_values(lon)
    lat = float(lat)
    lon = float(lon)
    if filter_ocean: filters.append(bm.is_land(lon,lat))
    if filter_boxes:
        within_box = False
        for box in boxes:
            MIN_LAT = box['MIN_LAT']
            MAX_LAT = box['MAX_LAT']
            MIN_LON = box['MIN_LON']
            MAX_LON = box['MAX_LON']
            if lat > MIN_LAT and lat < MAX_LAT and lon > MIN_LON and lon < MAX_LON:
                within_box = True
                break
        filters.append(within_box)
    include_it = True if all(filters) == True else False
    return include_it

def fix_values(value_to_fix):

    """
    Removing extra dots in latitudes or longitudes
    """
    correct_value = ''
    skip_dots = False
    for c in value_to_fix:
        if c != '.': correct_value+=c
        else:
            if not skip_dots:
                correct_value+=c
                skip_dots = True
    return correct_value

def read_input_file(input_template):

    """
    Reading XML input file
    """
    global folder, filter_boxes, filter_ocean, boxes
    boxes = []
    try:
        tree=XML.parse(input_template)
        root=tree.getroot()
        if root.find('folder') is not None:
            folder = root.find('folder').text
        else:
            print('Missing folder with CSV files')
            raise
        if root.find('filter_boxes') is not None:
            filter_boxes = False if (root.find('filter_boxes').text).upper() == 'FALSE' else True
        if root.find('filter_ocean') is not None:
            filter_ocean = False if (root.find('filter_ocean').text).upper() == 'FALSE' else True

        if filter_boxes:
            for box in root.findall('box'):
                box_info = {}
                for box_field in BOX_FIELDS:
                    if box.find(box_field) is not None:
                        box_info[box_field] = float(box.find(box_field).text)
                    else:
                        print('Missing '+box_field+' in box')
                        raise
                if not all(box_info.values()):
                    print('None values found in box fields')
                    raise
                boxes.append(box_info)

    except Exception as e:
        print('Error reading XML input file')
        traceback.print_exc()
        sys.exit(1)

def main():

    global folder, filter_boxes, filter_ocean, boxes
    global points_dict, bm
    bm = Basemap(area_thresh=0)
    parser = optparse.OptionParser()
    parser.add_option('-i','--input_file',dest='input_template',help='XML template with filterer input')
    #parser.add_option('-m','--mac',dest='new_mac',help='New MAC address')
    (options,arguments) = parser.parse_args()
    input_template = options.input_template
    if not input_template: print('Missing input XML file '); sys.exit(1)
    read_input_file(input_template)
    if folder[0] != '/':
        folder = os.getcwd() + '/'+folder
    print('########################################################')
    print('Location filterer :D')
    print('Input XML file: '+input_template)
    print('Selected folder: '+folder)
    print('########################################################')
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(folder):
        for file in f:
            files.append(os.path.join(r, file))
    print('Total number of files: '+str(len(files)))
    points_dict = {}

    headers = {}

    for file in files:
        count = 0
        print('--------------------------------------------------------')
        print('Processing data file: '+file.split('/')[-1])
        print('--------------------------------------------------------')
        filtered_because_box = 0
        repeated_elements = 0
        for line in open(file):
            if count > 0:
                data = line.strip().split(';')
                point_name = data[NAME_FIELD_POSITION]
                latitude = data[LAT_FIELD_POSITION]
                longitude =  data[LON_FIELD_POSITION]
                include_it = filter(latitude,longitude)
                if include_it:
                    if point_name not in points_dict: points_dict[point_name] = []
                    pair = [latitude,longitude]
                    if pair not in points_dict[point_name]: points_dict[point_name].append(pair)
                    else:  repeated_elements +=1
                else: filtered_because_box +=1
            else: header =   line.strip()
            count+=1
        headers[point_name] = header
        print('[*] Total quantity of points '+str(count-1))
        if point_name in  points_dict: print('[+] Quantity of kept points: '+str(len(points_dict[point_name])))
        else: print('[-] All points related to '+point_name+' were removed')
        print('[-] Quantity of filtered points because out of box or in the sea: '+str(filtered_because_box))
        print('[-] Quantity of repeated points: '+str(repeated_elements))

    filtered_folder = folder[0:-1]+'_filtered'
    os.mkdir(filtered_folder)
    print('########################################################')
    print('Output folder: '+filtered_folder)
    print('########################################################')


    for point_name in points_dict:
        filtered_file = open(filtered_folder+'/'+point_name+'.csv','w')
        filtered_file.write(headers[point_name]+'\n')
        for pair in points_dict[point_name]:
            filtered_file.write(point_name+';'+pair[0]+';'+pair[1]+'\n')
        filtered_file.close()

if __name__ == "__main__":

    main()
