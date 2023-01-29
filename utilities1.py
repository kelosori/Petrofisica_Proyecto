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

def read_data(files):
    rd = []
    for i in files:
        data = welly.Well.from_las(i)
        rd.append(data)
    return rd

def plot_null_data(data):
    null_data = data.isnull().sum()
    null_data.plot(kind='bar',
                 stacked='True',  # Muestra las barras apiladas
                 alpha=0.4,  # nivel de transparencia
                 width=0.9,  # Grosor de las barras para dejar espacio entre ellas
                 figsize=(9, 4),title="Plot of null data",subplots=True)

def curvas_logs(curvas, log, inicio, final):
    fig, axes = plt.subplots(1, len(curvas), figsize=(20,10))
    for ind, curva in enumerate(curvas):
        segmento = log.data[curva].to_basis(start=inicio, stop=final)
        if curva == 'SAND_FLAG':
            segmento.plot_2d(ax= axes[ind])
        else:
            segmento.plot(ax=axes[ind])
        axes[ind].set_title(curva)
    axes[0].set_ylabel('Depth (m)', fontsize=14)
    fig.suptitle('Petrophysical Logs', fontsize=16)
    plt.tight_layout()

def temp_1(fig,
           df_log,
           perm_col,
           phi_col,
           sw_col,
           ref_limits=(None, None)):

    axs = fig.subplots(nrows=1,
                       ncols=3,
                       sharey=True,
                       gridspec_kw={"wspace": 0})

    logs_to_plot = {'green': perm_col, 'blue': phi_col, 'red': sw_col}

    for ax, (color, log) in zip(axs, logs_to_plot.items()):
        ax.plot(df_log[log], df_log.index, color=color)
        ax.set_title(log)
        ax.xaxis.tick_top()

    axs[0].set_ylim(ref_limits[0], ref_limits[1])
    axs[0].invert_yaxis()
    axs[0].set_ylabel("Depth (m)")

def multi_well(figsize, data, template):
    fig_all = plt.figure(figsize=figsize)
    subfigs = fig_all.subfigures(1, len(data), wspace=2)
    for idx, (well_name, df) in enumerate(data.items()):
        template(subfigs[idx], df, "KLOGH", "PHIF", "SW")
        subfigs[idx].suptitle(well_name)