import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def load_data_one_week():
    
    data = pd.read_csv('plot_all.csv')
    data['time'] = pd.to_datetime(data['time'])
    data['date_snapshot'] = data['date_snapshot'].apply(lambda x: datetime.strptime(str(x), "%Y%m%d").date())
    
    min_date = (datetime.now()- timedelta(7)).date()
    plot_data = data[data.date_snapshot >= min_date]
    return plot_data
def load_webcam_location():

    geo_data = pd.read_csv('webcam_info_06042025.csv')
    sample_df = geo_data.head(51)[geo_data.head(51).evaluate=='ok'][['city','latitude','longitude','num_imgs']]
    
    return sample_df

def load_delay_data():
    data = pd.read_csv('mean_delay.csv', parse_dates=['snap_time'])
    min_date = datetime.now() - timedelta(7)
    plot_data = data[data.snap_time >= min_date]
    return plot_data

# Sidebar for inputs
with st.sidebar:
    st.write("### Selection for Graph")
    st.write("Select which graph you want like to see")
    selected_graph = st.selectbox("Select graph to display:", ('🚂 SNCB train data','🗻 Webcam location'))


data = load_data_one_week()
delay_data = load_delay_data()


fig = px.line(data, x="time", y="ongoing_trips", color='date_snapshot',
              markers=True, 
              title="Scheduled Trips by Hour",
              labels={"time": "Time (Hourly)", "ongoing_trips": "Number of On-going Trips"},
              template = 'seaborn')

fig_delay = go.Figure()
fig_delay.add_scatter(x=delay_data['snap_time'], y=delay_data['arrival_delay'], name='Mean Arrival Delay')
fig_delay.add_scatter(x=delay_data['snap_time'], y=delay_data['departure_delay'], name='Mean Departure Delay')
fig_delay.update_layout(title="Arrival and Departure Delay by Quarter-Hour in recent 7 days",
                        xaxis_title="Time",
                        yaxis_title="Delay (seconds)")

geo_data = load_webcam_location()
fig2 = go.Figure()
fig2 = px.density_map(geo_data, lat='latitude', lon='longitude', z='num_imgs', radius=10,
                        center=dict(lat=50, lon=4),zoom=5,color_continuous_scale="rainbow",
                        map_style="streets")

if 'train' in selected_graph:
    st.title("🚂 SNCB train data")
    st.plotly_chart(fig, use_container_width=False)
    st.plotly_chart(fig_delay, use_container_width=False)
else:
    st.title("🗻 Webcam map - Top 40 webcams")
    st.plotly_chart(fig2, use_container_width=False)