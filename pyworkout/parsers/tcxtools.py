"""
Tools to process TCX files,
specifically for parsing and
converting to other formats.
"""

import numpy as np
import pandas as pd
from lxml import objectify


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
        # TODO: get API version, do API checks, etc
        # TODO: get author version

    def parse(self):
        """
        Parse specified TCX file into a DataFrame
        Return a Dataframe and sets Dataframe and sets
        the self.dataframe object in the TCXParser.
        """

        self.tcx = objectify.parse(open(self.__filehandle__))
        self.activity = self.tcx.getroot().Activities.Activity
        # TODO: Maybe make this privite to the class
        lap_data = self._traverse_laps_()
        mid_frame = []
        for laps in lap_data:
            mid_frame.append(pd.DataFrame(laps))

        self.dataframe = pd.concat(mid_frame)
        return self.dataframe

    def _get_xml_children_(root_xml):
        return root_xml.getchildren()

    def get_activity_timestamp(self):
        """
        Returns the TCX file timestamp if parsed
        """
        if self.activity is None:
            return None
        else:
            return self.activity.Id

    def _traverse_laps_(self):
        lap_totals = []
        for laps in self.activity.Lap.getnext():
            laps_list = self._traverse_tracks_(laps)
            lap_totals.append(laps_list)
        return lap_totals


    def _traverse_tracks_(self, lap_items):
        trackingpoints = self._traverse_trackingpoints_(lap_items.Track)
        return trackingpoints

    def _traverse_trackingpoints_(self, track_items):
        return_array = []
        for trackingpoints in track_items.Trackpoint.getnext():
            # TODO: Write sport specific checks to prevent extra features
            return_dict = {}
            return_dict['time'] = np.str(trackingpoints.Time)
            try:
                return_dict['altitude'] = np.float(trackingpoints.AltitudeMeters)
            except AttributeError:
                None

            try:
                return_dict['cadence'] = np.float(trackingpoints.Cadence)
            except AttributeError:
                None

            try:
                return_dict['distance'] = np.float(trackingpoints.DistanceMeters)
            except AttributeError:
                None

            try:
                return_dict['hr'] = np.float(trackingpoints.HeartRateBpm.Value)
            except AttributeError:
                return_dict['hr'] = 0

            try:
                return_dict['latitude'] = \
                    np.float(trackingpoints.Position.LatitudeDegrees)
            except AttributeError:
                return_dict['latitude'] = 0

            try:
                return_dict['longitude'] = \
                    np.float(trackingpoints.Position.LongitudeDegrees)
            except AttributeError:
                return_dict['longitude'] = 0

            try:
                return_dict['power'] = \
                    np.float(trackingpoints.Extensions.getchildren()[0].Watts)
            except AttributeError:
                return_dict['power'] = 0

            try:
                return_dict['speed'] = \
                    np.float(trackingpoints.Extensions.getchildren()[0].Speed)
            except AttributeError:
                return_dict['speed'] = 0
            return_array.append(return_dict)

        return return_array

    def get_sport(self):
        """
        Returns the specified sport of the TCX file
        """
        if self.activity is None:
            return None
        else:
            return self.activity.items()[0][1]

    def get_workout_startime(self):
        """
        Returns the starting timestamp of the specified TCX file
        """
        if self.activity is None:
            return None
        else:
            return self.activity.Lap.items()[0][1]
