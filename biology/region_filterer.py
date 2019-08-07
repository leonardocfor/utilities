#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Region filterer for species inside a box described by MIN_LAT, MAX_LAT, MIN_LON, MAX_LON
It also eliminates repeated locations
"""

import optparse
import os
from mpl_toolkits.basemap import Basemap


### Global variables
##############################

def filter(lat,lon):

    """
    Filtering species per selected latitude and longitude
    """
    if lat.count('.') > 1: lat = fix_values(lat)
    if lon.count('.') > 1: lon = fix_values(lon)
    lat = float(lat)
    lon = float(lon)
    land_point = bm.is_land(lon,lat)
    include_it = False
    if land_point: include_it = True
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

def main():

    global species_dict, bm
    bm = Basemap(area_thresh=0)
    parser = optparse.OptionParser()
    parser.add_option('-f','--folder',dest='folder',help='Folder with CSV files')
    #parser.add_option('-m','--mac',dest='new_mac',help='New MAC address')
    (options,arguments) = parser.parse_args()
    folder = options.folder
    #new_mac = options.new_mac
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
