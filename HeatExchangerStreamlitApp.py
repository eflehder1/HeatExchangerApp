import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from math import pi
import numpy as np

# Function to create a radar chart
def create_radar_chart(df, params):
    categories = list(df)[1:]
    N = len(categories)

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories)

    for i in range(len(df)):
        data = df.iloc[i].drop('Group').tolist()
        data += data[:1]
        ax.plot(angles, data, linewidth=1, linestyle='solid', label=df['Group'][i])
        ax.fill(angles, data, alpha=0.1)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    return plt

# Streamlit app
st.title("Heat Exchanger Design Analysis")

# File uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Display data
    st.write(data)

    # Select parameters for radar chart
    params = st.multiselect("Select parameters for radar chart", data.columns.tolist(), default=data.columns.tolist())

    # Create box plot
    st.subheader("Box Plot")
    selected_param_for_boxplot = st.selectbox("Select Parameter for Box Plot", data.columns.tolist())
    fig = px.box(data, y=selected_param_for_boxplot)
    st.plotly_chart(fig)

    # Filter data for radar chart
    radar_data = data[params]
    st.subheader("Radar Chart")
    radar_fig = create_radar_chart(radar_data, params)
    st.pyplot(radar_fig)
