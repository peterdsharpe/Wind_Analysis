import pandas as pd
from pathlib import Path
import os, sys

this_directory = Path(__file__).parent
sys.path.insert(0, str(this_directory.parent))

from load_data import load_data

data = load_data(
    str(this_directory.parent / "data" / "MMS-20Hz_DC8_20160712_R0.ict")
)