"""
Tools to process TCX files,
specifically for parsing and
converting to other formats.
"""

import numpy as np
import pandas as pd
from lxml import objectify
import dateutil.parser
import logging

TPXNS = "{https://www8.garmin.com/xmlschemas/ActivityExtensionv2}TPX"
LXNS = "{https://www8.garmin.com/xmlschemas/ActivityExtensionv2}LX"


class TCXPandas(object):
    """
    Class for Parsing .TCX files to Pandas DataFrames.

    Parameters
    ----------
    tcx_file : string, path object,
               the path to the tcx file

    """

    def __init__(self, tcx_file, **kwds):
        self.__filehandle__ = tcx_file
        self.tcx = None
        self.activity = None
        self.dataframe = None

        logging.basicConfig(filename="TCXconversion.log", level=logging.DEBUG)

    def parse(self):
        """
        Parse specified TCX file into a DataFrame
        Return a Dataframe and sets Dataframe and sets
        the self.dataframe object in the TCXParser.
        """

        self.tcx = objectify.parse(open(self.__filehandle__))
        self.activity = self.tcx.getroot().Activities.Activity
        self.dataframe = pd.DataFrame(self._traverse_laps_())
        return self.dataframe

    def get_activity_timestamp(self):
        """
        Returns the TCX file timestamp if parsed
        """
        if self.activity is None:
            return None
        else:
            return self.activity.Id

    def get_sport(self):
        """
        Returns the specified sport of the TCX file
        """
        if self.activity is None:
            return None
        else:
            return self.activity.attrib['Sport']

    def get_workout_startime(self):
        """
        Returns the starting timestamp of the specified TCX file
        """
        if self.activity is None:
            return None
        else:
            return self.activity.Lap.items()[0][1]

    def _traverse_laps_(self):

        # New iterator method to align with lxml standard
        return_array = []
        for laps in self.activity.Lap:
            for tracks in laps.Track:
                for trackingpoints in tracks.Trackpoint:
                    return_dict = {}
                    return_dict['time'] = dateutil.parser.parse(str(trackingpoints.Time))

                    try:
                        return_dict['latitude'] = \
                            np.float(trackingpoints.Position.LatitudeDegrees)
                    except AttributeError:
                        pass #TODO log this

                    try:
                        return_dict['longitude'] = \
                            np.float(trackingpoints.Position.LongitudeDegrees)
                    except AttributeError:
                        pass #TODO log this

                    try:
                        return_dict['altitude'] = np.float(trackingpoints.AltitudeMeters)
                    except AttributeError:
                        pass #TODO log this

                    try:
                        return_dict['distance'] = np.float(trackingpoints.DistanceMeters)
                    except AttributeError:
                        pass #TODO log this

                    try:
                        return_dict['hr'] = np.float(trackingpoints.HeartRateBpm.Value)
                    except AttributeError:
                        pass #TODO log this

                    try:
                        return_dict['speed'] = \
                            np.float(trackingpoints.Extensions[TPXNS].Speed)
                    except AttributeError:
                        pass #TODO log this

                    if self.get_sport == 'Running':
                        try:
                            return_dict['cadence'] = \
                                np.float(trackingpoints.Extensions[TPXNS].RunCadence)
                        except AttributeError:
                            pass #TODO log this
                    else: # self.activity.attrib['Sport'] == 'Biking':
                        try:
                            return_dict['cadence'] = np.float(trackingpoints.Cadence)
                        except AttributeError:
                            pass #TODO log this

                        try:
                            return_dict['power'] = \
                                np.float(trackingpoints.Extensions[TPXNS].Watts)
                        except AttributeError:
                            pass #TODO log this

                    return_array.append(return_dict)
                return return_array
