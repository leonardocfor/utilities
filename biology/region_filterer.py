#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Region filterer for species inside a box described by MIN_LAT, MAX_LAT, MIN_LON, MAX_LON
It also eliminates repeated locations
"""

import optparse
import os


### Global variables
MIN_LAT = -60
MAX_LAT = 90
MIN_LON = -150
MAX_LON = -30
##############################

def filter(lat,lon):

    """
    Filtering species per selected latitude and longitude
    """
    if lat.count('.') > 1: lat = fix_values(lat)
    if lon.count('.') > 1: lon = fix_values(lon)
    lat = float(lat)
    lon = float(lon)
    include_it = False
    if lat > MIN_LAT and lat < MAX_LAT and lon > MIN_LON and lon < MAX_LON:
        include_it = True
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

def remove_repeated_elements():

    """
    Remove repeated locations per species
    """
    global species_dict
    species_dict_copy = {}
    for species in species_dict:
        species_dict_copy[species] = []
        for pair in species_dict[species]:
            if pair not in species_dict_copy[species]:
                species_dict_copy[species].append(pair)

    species_dict = species_dict_copy

def main():

    global species_dict
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
        print('Processing species file: '+file.split('/')[-1])
        print('--------------------------------------------------------')
        for line in open(file):
            if count > 0:
                data = line.strip().split(';')
                species = data[0]
                latitude = data[1]
                longitude =  data[2]
                include_it = filter(latitude,longitude)
                if include_it:
                    if species not in species_dict: species_dict[species] = []
                    species_dict[species].append([latitude,longitude])
            else: header =   line.strip()
            count+=1
        headers[species] = header

    remove_repeated_elements()

    filtered_folder = folder[0:-1]+'_filtered'
    os.mkdir(filtered_folder)
    print('Output folder: '+filtered_folder)


    for species in species_dict:
        filtered_file = open(filtered_folder+'/'+species+'.csv','w')
        filtered_file.write(headers[species]+'\n')
        for pair in species_dict[species]:
            filtered_file.write(species+';'+pair[0]+';'+pair[1]+'\n')
        filtered_file.close()








if __name__ == "__main__":

	main()
