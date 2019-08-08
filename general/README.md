# Utilities

Software utilities for data manipulation

----
### 1. location_filterer.py
----

Filter location-based data (latitude,longitude) using geographic boxes. The software processes CSV files found in a folder and produced a filtered file per input file. Filtering is done based on two approaches: 

 * Boxes: A box is defined with a min and max laitude and a min and max longitude

 * Sea: A point in the sea can be filtered out 
 
Usage 

```python
./location_filterer.py -i <input_file.xml>
```
A template of <input_file.xml> can be found in [here](https://github.com/leonardocfor/utilities/blob/master/general/templates/location_filterer.xml). See an example of the Americas here:

```xml
<?xml version='1.0'?>

<filter>
  <folder>data/rvfsdarreglados/</folder>
  <filter_boxes>true</filter_boxes>
  <filter_ocean>true</filter_ocean>
  <!-- Include as many box tags as required -->
  <box>
    <MIN_LAT>-60</MIN_LAT>
    <MAX_LAT>90</MAX_LAT>
    <MIN_LON>-150</MIN_LON>
    <MAX_LON>-30</MAX_LON>
  </box>
</filter>
```

Each CSV file is to be composed of lines where fields are separed with semicolons. Modify NAME_FIELD_POSITION, LAT_FIELD_POSITION and LON_FIELD_POSITION in the script accordingly. Currently a line in a CSV file is assumed to be of the form: <name_of_the_point>;<latitude>;<longitude>
