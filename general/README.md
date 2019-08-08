# Utilities

Software utilities for data manipulation

----
### 1. location_filterer.py
----

Filter location-based data (latitude,longitude) using geographic boxes. The software processes CSV files located in a folder and produced a filtered file per input. Filtering is done based on two approaches: 

 * Boxes: A box is defined with a min and max laitude and a min and max longitude

 * Sea: A point in the sea can be removed
 
Usage 

```
./location_filterer.py -i <input_file.xml>
```
A template of <input_file.xml> can be found in [here](https://github.com/leonardocfor/utilities/blob/master/general/templates/location_filterer.xml). Each CSV file is to be composed of lines where fields are separed with semicolons. Modify NAME_FIELD_POSITION, LAT_FIELD_POSITION and LON_FIELD_POSITION in the script accordingly. Currently a line in a CSV file is assumed to be of the form: <name_of_the_point>;<latitude>;<longitude>
