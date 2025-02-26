import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def load_data_hourly():
    data = pd.read_csv("plot_all.csv")
    data['time'] = pd.to_datetime(data['time'])
    
    recent_data = pd.read_csv("plot_df.csv")
    recent_data.drop(columns="Unnamed: 0", inplace=True)
    recent_data['time'] = pd.to_datetime(recent_data['time'])
    
    data = pd.concat([data, recent_data]).drop_duplicates()
    data.to_csv("plot_all.csv", index=False)
    data['date_snapshot'] = data['date_snapshot'].apply(lambda x: datetime.strptime(str(x), "%Y%m%d").date())
    
    min_date = (datetime.now()- timedelta(7)).date()
    plot_data = data[data.date_snapshot >= min_date]
    return plot_data

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