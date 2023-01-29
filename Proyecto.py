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
from utilities1 import dataframe,plot_null_data, curvas_logs, multi_well,read_data
import welly
#import missingno as msno

st.set_option('deprecation.showPyplotGlobalUse', False)

# Insert an icon
icon = Image.open("Resources/petrofisica3.jpg")

# State the design of the app
st.set_page_config(page_title="Petrophysics", page_icon=icon)

# Insert css codes to improve the design of the app
st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
</style>""",
    unsafe_allow_html=True,
)

# Title of the app
st.title("PETROPHYSICS APP :clipboard:")

st.write("---")

st.markdown(
    """ This app is used to visualize the results of oil reservoir by petrophysics and to upload LAS files, 
to call data, and to realize petrophysical log charts ..

*Python Libraries:* Streamlit, pandas, plotly, PIL.
"""
)

# Add additional information
expander = st.expander("About")
expander.write("This app is very useful for petrophysics projects")

# Insert image
st.subheader("*PETROPHYSICS*")
image = Image.open("Resources/petrofisica.jpg")
st.image(image, width=100, use_column_width=True)

# Insert video
st.subheader("*Basic Fundamentals of Well Log Interpretation*")
video = open("Resources/Petrofísica 101. Fundamentos básicos.mp4", "rb")
st.video(video)
st.caption("Video about Well Log Interpretation")


# Sidebar
Logo = Image.open("Resources/ESPOL.png")
st.sidebar.image(Logo)

# Add title to the sidebar section
st.sidebar.title(":arrow_down: *Navigation*")

# Pages
with st.sidebar:
    options = option_menu(
        menu_title="Menu",
        options=["Home", "Data Information", "Logs Visualizations"],
        icons=["house", "sim", "graph-up"],)

# Options
if options == "Data Information":
    # number of file to upload
    n_wells = int(st.number_input("Enter the well logs files"))
    files = [
        st.file_uploader(f"Upload the las file of well {n + 1}") for n in range(n_wells)
    ]

    if files is not None:
        stringio = [StringIO(log.getvalue().decode("utf-8")) for log in files]
        datas = dataframe(stringio)
        if st.checkbox("Uploaded file dataframes"):
            st.subheader("Uploaded file dataframes")
            for data in datas:
                st.write(data)

        elif st.checkbox("Statistical summary of uploaded files"):
            st.subheader("Statistical summary of uploaded files")
            for data in datas:
                st.write(data.describe())

        elif st.checkbox("Show charts on null data"):
            st.subheader("Show charts on null data")
            for data in datas:
                st.write(data.isnull().sum())
                fig = plot_null_data(data)
                st.pyplot(fig)



elif options == "Logs Visualizations":
    n_wells = int(st.number_input("Enter the well logs files"))
    files = [
        st.file_uploader(f"Upload the las file of well {n + 1}") for n in range(n_wells)
    ]

    if files is not None:
        stringio = [StringIO(log.getvalue().decode("utf-8")) for log in files]
        datas = read_data(stringio)
        Curves = ["KLOGH", "PHIF", "SAND_FLAG", "SW", 'VSH']
        for data in datas:
            fig = curvas_logs(Curves,data,3350,3450)
            st.pyplot(fig)




