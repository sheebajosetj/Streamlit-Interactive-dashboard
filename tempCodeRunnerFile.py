import streamlit as st
import plotly.express as plt
import warnings
warnings.filterwarnings('ignore')
import os
import pandas as pd

st.set_page_config(page_title = 'Superstore!!!', page_icon = ':bar_chart:', layout = 'wide')
st.title(' :bar_chart: Sample SuperStore EDA')

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html = True) # To move the title above

fl = st.file_uploader(':file_folder: Upload a file', type = (['csv','txt','xlsx','xls']))

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename,encoding = 'ISO - 8859-1')
else:
    os.chdir(r'C:\Users\shali\Streamlit')
    df = pd.read_csv('Superstore.csv', encoding = 'ISO - 8859-1')
    
col1, col2 = st.columns((2))
df['Order Date'] = pd.to_datetime(df['Order Date'])

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date 
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()