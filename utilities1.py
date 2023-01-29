import numpy as np
import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly_express as px
from scipy import stats
from streamlit_option_menu import option_menu
from PIL import Image
from collections import namedtuple
from io import StringIO
import warnings
import lasio
from pathlib import Path
import welly

archivo1 = Path("Data/VOLVE-PETROPHYSICAL_INTERPRETATION/15_9-F-1 A/WLC_PETRO_COMPUTED_OUTPUT_1.LAS")
archivo2 = Path("Data/VOLVE-PETROPHYSICAL_INTERPRETATION/15_9-F-1 B/WLC_PETRO_COMPUTED_OUTPUT_1.LAS")
archivo3 = Path("Data/VOLVE-PETROPHYSICAL_INTERPRETATION/15_9-F-1 C/WLC_PETRO_COMPUTED_OUTPUT_1.LAS")

files = [archivo1,archivo2,archivo3]
#data = []
def dataframe(files):
    data = []
    for i in files:
        log = lasio.read(i)
        df = log.df()
        data.append(df)
    return(data)

data = dataframe(files)
lasio.read(files[0]).data
