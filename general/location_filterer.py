#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Region filterer for species inside a box described by MIN_LAT, MAX_LAT, MIN_LON, MAX_LON
It also eliminates repeated locations
"""

import optparse
import os
import sys
from mpl_toolkits.basemap import Basemap
from xml.etree import ElementTree as XML


### Global variables
# MIN_LAT = -60
# MAX_LAT = 90
# MIN_LON = -150
# MAX_LON = -30
BOX_FIELDS = [
    'MIN_LAT',
    'MAX_LAT',
    'MIN_LON',
    'MAX_LON'
]

##############################

def filter(lat,lon):

    """
    Filtering species per selected latitude and longitude
    """
    filters = []
    if lat.count('.') > 1: lat = fix_values(lat)
    if lon.count('.') > 1: lon = fix_values(lon)
    lat = float(lat)
    lon = float(lon)
    if filter_ocean: filters.append(bm.is_land(lon,lat))
    if filter_boxes:
        for box in boxes:
            MIN_LAT = box['MIN_LAT']
            MAX_LAT = box['MAX_LAT']
            MIN_LON = box['MIN_LON']
            MAX_LON = box['MAX_LON']
            if lat > MIN_LAT and lat < MAX_LAT and lon > MIN_LON and lon < MAX_LON and land_point:
                filters.append(True)
                break
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

def remove_ocean_points():

    """
    Removing points in the sea
    """
    global species_dict
    species_dict_copy = {}

    for species in species_dict:
        species_dict_copy[species] = []
        for pair in species_dict[species]:
            if bm.is_land(float(pair[0]),float(pair[1])):
                species_dict_copy[species].append(pair)

    species_dict = species_dict_copy

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
                        box_info[box_field] = box.find(box_field).text
                    else:
                        print('Missing '+box_field+' in box')
                        raise
                if not all(box_info.values()):
                    print('None values found in box fields')
                    raise
                boxes.append(box_info)

    except Exception as e:
        print('Error reading XML input file')
        sys.exit(1)

def main():

    global folder, filter_boxes, filter_ocean, boxes
    global species_dict, bm
    bm = Basemap(area_thresh=0)
    parser = optparse.OptionParser()
    parser.add_option('-i','--input_file',dest='input_template',help='XML template with filterer input')
    #parser.add_option('-m','--mac',dest='new_mac',help='New MAC address')
    (options,arguments) = parser.parse_args()
    input_template = options.input_template
    read_input_file(input_template)
    if folder[0] != '/':
        folder = os.getcwd() + '/'+folder
    print('########################################################')
    print('Selected folder: '+folder)
    print('########################################################')
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(folder):
        for file in f:
            files.append(os.path.join(r, file))
    print('Total number of files: '+str(len(files)))
    species_dict = {}

    headers = {}

    for file in files:
        count = 0
        print('--------------------------------------------------------')
        print('Processing species file: '+file.split('/')[-1])
        print('--------------------------------------------------------')
        filtered_because_box = 0
        repeated_elements = 0
        for line in open(file):
            if count > 0:
                data = line.strip().split(';')
                species = data[0]
                latitude = data[1]
                longitude =  data[2]
                include_it = filter(latitude,longitude)
                if include_it:
                    if species not in species_dict: species_dict[species] = []
                    pair = [latitude,longitude]
                    if pair not in species_dict[species]: species_dict[species].append(pair)
                    else:  repeated_elements +=1
                else: filtered_because_box +=1
            else: header =   line.strip()
            count+=1
        headers[species] = header
        if species in  species_dict: print('[+] Quantity of kept points: '+str(len(species_dict[species])))
        else: print('[-] All points related to species were removed')
        print('[-] Quantity of filtered points because of box or in the sea: '+str(filtered_because_box))
        print('[-] Quantity of repeated points: '+str(repeated_elements))

    #remove_repeated_elements()
    #remove_ocean_points()
    filtered_folder = folder[0:-1]+'_filtered'
    os.mkdir(filtered_folder)
    print('########################################################')
    print('Output folder: '+filtered_folder)
    print('########################################################')


    for species in species_dict:
        filtered_file = open(filtered_folder+'/'+species+'.csv','w')
        filtered_file.write(headers[species]+'\n')
        for pair in species_dict[species]:
            filtered_file.write(species+';'+pair[0]+';'+pair[1]+'\n')
        filtered_file.close()








if __name__ == "__main__":

    main()
