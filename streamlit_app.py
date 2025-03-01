import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

pastel_colors = ["#A1C4FD", "#FFC3A0", "#FF9A8B", "#D4A5A5", "#C1E1C1", "#F7CAC9", "#B5EAD7"]

def update_new_data():
    data = pd.read_csv("plot_all.csv")
    data['time'] = pd.to_datetime(data['time'])
    
    recent_data = pd.read_csv("plot_df.csv")
    recent_data.drop(columns="Unnamed: 0", inplace=True)
    recent_data['time'] = pd.to_datetime(recent_data['time'])
    
    data = pd.concat([data, recent_data]).drop_duplicates()
    data.to_csv("plot_all.csv", index=False)

def load_data_one_week():
    
    data = pd.read_csv('plot_all.csv')
    data['time'] = pd.to_datetime(data['time'])
    data['date_snapshot'] = data['date_snapshot'].apply(lambda x: datetime.strptime(str(x), "%Y%m%d").date())
    
    min_date = (datetime.now()- timedelta(7)).date()
    plot_data = data[data.date_snapshot >= min_date]
    return plot_data

st.title("🚂 SNCB train data")
# st.write(
#     "Test with train data"
# )
data = load_data_one_week()
fig = go.Figure()
fig = px.line(data, x="time", y="ongoing_trips", color='date_snapshot',
              markers=True, 
              title="Scheduled Trips by Hour",
              labels={"time": "Time (Hourly)", "ongoing_trips": "Number of On-going Trips"},
              color_discrete_sequence=pastel_colors)

st.plotly_chart(fig, use_container_width=False, template=None)