import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

def generate_map(data):
    # Initialize the map
    m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=4)

    # Add markers and popups to the map
    for i, row in data.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=row['Description'],
            tooltip=f"Latitude: {row['lat']}, Longitude: {row['lon']}",
            icon=folium.Icon(color=row['color'])
        ).add_to(m)

    return m

# Streamlit app
st.title('Cold Store_Merchant Exporters')
st.write('Upload Merchant_Exporters_ME.xlsx Excel file')

# File upload
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    try:
        data = pd.read_excel(uploaded_file)

        # Check for required columns
        required_columns = {'Name', 'Latitude', 'Longitude', 'Icon Color'}
        if not required_columns.issubset(data.columns):
            st.error("The uploaded file is missing one or more required columns: Name, Latitude, Longitude, Icon Color.")
        else:
            # Rename columns if necessary
            data = data.rename(columns={'Name': 'name', 'Latitude': 'lat', 'Longitude': 'lon', 'Icon Color': 'color'})

            # Convert lat and lon to numeric
            data['lat'] = pd.to_numeric(data['lat'], errors='coerce')
            data['lon'] = pd.to_numeric(data['lon'], errors='coerce')

            # Drop rows with missing lat or lon values
            data = data.dropna(subset=['lat', 'lon'])

            # Display the map
            map_data = generate_map(data)
            folium_static(map_data)
    except Exception as e:
        st.error(f"An error occurred: {e}")
