from pyworkout.parsers import *
import os
import sys


def _main():
    __version__ = "0.0.2"
    __doc__ = """
    Pyworkout-toolkit module
    Allows for analysis of TCXfiles from workout data and 
    converts them into Pandas dataframes for easier data analysis
    Has utilities and helper functions to assist in parsing
    and data analysis of such workout data.
    Run `python -m pyworkout -h` for command line options.
    """
    import argparse
    
    parser = argparse.ArgumentParser(prog="python -m pyworkout", description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('filename', help="filename of workout file")
    parser.add_argument('args', nargs=argparse.REMAINDER,
                        help="Command line arguments")
    args = parser.parse_args()
    sys.argv = [args.filename] + args.args
