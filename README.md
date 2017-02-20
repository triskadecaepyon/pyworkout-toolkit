# pyworkout-toolkit
pyworkout-toolkit: Python tools to process workout data and telemetry

## Summary
The pyworkout-toolkit is a Python package that provides tools for post-workout analysis of data or telemetry.  The majority of the tools cater to coaches and invidividuals who wish to utilize the data to generate metrics or exercise machine learning/data mining.  The toolkit provides parsing of the popular .TCX and .GPX formats, along with some general purpose functions that help preprocess the data for metrics, visualization, or machine learning.  

## Features
- Parsing of .TCX and .GPX formats; other formats on the way
- Caters to the Pandas DataFrame for analysis flexibility and use in Scikit-Learn
- Helper functions to correct sport-specific errors in recording
- Handling of missing data and conversion/correction of GPS units
- Exporting to popular formats such as CSV, HDF5

## Examples
Parsing of TCX files is simple:
```
from pyworkout.parsers import tcxtools
workout_data = tcxtools.TCXPandas('pyworkout/tests/data/test_dataset_1.tcx') # Create the Class Object
workout_data.parse() # Returns a dataframe
```
Other details about the TCX file can be found as well:
```
workout_data.get_sport()
'Biking'

workout_data.get_workout_startime()
'2016-10-20T22:01:26.000Z'
```
If opening multiple TCX files for large-scale reporting, it is recommended that [Dask and Dask Delayed](http://dask.pydata.org/en/latest/delayed-overview.html) be used:
```
import dask.dataframe as dd
from dask import delayed

tcx1 = delayed(tcxtools.TCXPandas('workout_1.tcx').parse()) # Delay these calculations
tcx2 = delayed(tcxtools.TCXPandas('workout_2.tcx').parse()) # Use as many as needed

total = dd.from_delayed([tc1, tc2]) # However many files you need
total.visualize() # Visualize the task graph
total.compute() # Compute it
# This returns a dataframe with all the files
```


## Getting your data
In order to get your data in TCX format, you will need to export the files from the given service.
- Instructions for [Strava](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export)
- Instructions for [Garmin](https://connect.garmin.com/features/export)

## Dependencies
- NumPy
- Pandas
- lxml
- Python 3+ (developed on 3.5)

## Installation
Local installation is supported, with pip and conda-build files included.  Currently available on pip and conda.

pip installation:
```
pip install pyworkout-toolkit
```
conda installation:
```
conda install -c triskadecaepyon pyworkout=0.0.1
```

## License
BSD

## Scope and goals
The pyworkout-toolkit aims to assist in the furthering of research in the health/wearables area by providing the tools necessary to process, correct, and analyze collected data.  The project was created to fill the gap between data aquisition on the device to the end-developer, allowing for algorithm creation, data mining, and visualization once the data has been converted.  Eventual integration with graphing libraries have been planned, with Matplotlib, Bokeh, and Datashader on the list.
