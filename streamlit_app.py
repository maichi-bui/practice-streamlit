import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data_hourly():
    data = pd.read_csv("plot_all.csv")
    data['time'] = pd.to_datetime(data['time'])
    
    return data

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
data = load_data_hourly()
fig = go.Figure()
fig = px.line(data, x="time", y="ongoing_trips", color='date_snapshot',
              markers=True, 
              title="Scheduled Trips by Hour",
              labels={"time": "Time (Hourly)", "ongoing_trips": "Number of On-going Trips"},
              template="plotly_dark")
fig.show()