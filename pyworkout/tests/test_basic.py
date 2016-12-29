import unittest
import importlib
import pyworkout
from pyworkout.parsers import tcxtools
"""
Please note that these tests only work in Python 3.5+ at the moment.
"""

class TestBasicObject(unittest.TestCase):

    def test_import_of_module(self):
        library = importlib.util.find_spec("pyworkout")
        self.assertTrue(library is not None)

    def test_get_sport_none(self):
        tcxclass = tcxtools.TCXPandas('pyworkout/tests/data/test_dataset_1.tcx')
        #with self.assertRaises(AttributeError):
        #  tcxclass.get_sport()
        self.assertTrue(tcxclass.get_sport() is None)

    def test_get_start_time_none(self):
        tcxclass = tcxtools.TCXPandas('pyworkout/tests/data/test_dataset_1.tcx')
        self.assertTrue(tcxclass.get_workout_startime() is None)


if __name__ == '__main__':
    unittest.main()
