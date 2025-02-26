import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data_hourly():
    data = pd.read_csv("plot_all.csv")
    data['time'] = pd.to_datetime(data['time'])
    
    recent_data = pd.read_csv("plot_df.csv")
    recent_data['time'] = pd.to_datetime(recent_data['time'])
    data = pd.concat([data, recent_data]).drop_duplicates()
    data.to_csv("plot_all.csv")
    return data

st.title("🚂 SNCB train data")
# st.write(
#     "Test with train data"
# )
data = load_data_hourly()
fig = go.Figure()
fig = px.line(data, x="time", y="ongoing_trips", color='date_snapshot',
              markers=True, 
              title="Scheduled Trips by Hour",
              labels={"time": "Time (Hourly)", "ongoing_trips": "Number of On-going Trips"},
              template="plotly_dark")
st.plotly_chart(fig)