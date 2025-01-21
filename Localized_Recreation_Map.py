# import the necessary libraries  Streamlit "pip install streamlit" 
# How to run the dashboard:  Run the dashboard by executing the following command in the terminal: "streamlit run Localized_Recreation_Map.py"
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import json

API_URL = "http://127.0.0.1:8000"  # Replace if your API is running elsewhere

st.title("Recreational Facilities Map")

def get_facilities(state=None, ada_accessible=None):
    params = {}
    if state:
        params["state"] = state
    if ada_accessible is not None and ada_accessible != "":
        params["ada_accessible"] = ada_accessible
    response = requests.get(f"{API_URL}/facilities", params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Error fetching facilities: {response.status_code}")
        # st.write(response.text)
        return []

#Sidebar with filtering options
with st.sidebar:
  st.header("Filter Facilities")
  selected_state = st.selectbox("Select State", ["", "AZ", "UT", "OR"])
  ada_access_filter = st.selectbox("ADA Accessible", ["", True, False])

# Fetch Data from API
facilities = get_facilities(selected_state, ada_access_filter)

# Facility Map
st.header("Facilities Map")

if facilities:
    # st.write("Parameters for /facilities API:", {"state": selected_state, "ada_accessible": ada_access_filter})
    # st.write("Response from /facilities API:", facilities)
    if facilities and facilities[0] and "FacilityLatitude" in facilities[0] and "FacilityLongitude" in facilities[0]:
        m = folium.Map(location=[facilities[0]["FacilityLatitude"], facilities[0]["FacilityLongitude"]], zoom_start=6)

        for facility in facilities:
            if facility.get("GEOJSON") and isinstance(facility.get("GEOJSON"), dict) and facility["GEOJSON"].get("TYPE") == "Point" and facility["GEOJSON"].get("COORDINATES") and len(facility["GEOJSON"]["COORDINATES"])==2:
              try:
                geo_data = facility["GEOJSON"]
                # st.write(f"Processing GeoJSON data for {facility.get('FacilityID', 'N/A')}: {geo_data}")
                folium.GeoJson(geo_data,
                          popup=f"<b>Facility:</b> {facility.get('FacilityName', 'N/A')}<br><b>State:</b> {facility.get('AddressStateCode', 'N/A')}<br><b>Reservable:</b> {facility.get('Reservable', 'N/A')}<br><b>ADA:</b> {facility.get('FacilityAdaAccess', 'N/A')}",
                            ).add_to(m)

              except Exception as e:
                    st.write(f"Error {e} processing facility {facility.get('FacilityID', 'N/A')}")

            elif  facility.get("FacilityLatitude") != None and facility.get("FacilityLongitude") !=None:
                # st.write(f"Processing Marker for {facility.get('FacilityID', 'N/A')}, using FacilityLatitude: {facility.get('FacilityLatitude')} and FacilityLongitude: {facility.get('FacilityLongitude')}")
                folium.Marker(
                    location=[facility["FacilityLatitude"], facility["FacilityLongitude"]],
                    popup=f"<b>Facility:</b> {facility.get('FacilityName', 'N/A')}<br><b>State:</b> {facility.get('AddressStateCode', 'N/A')}<br><b>Reservable:</b> {facility.get('Reservable', 'N/A')}<br><b>ADA:</b> {facility.get('FacilityAdaAccess', 'N/A')}",
                ).add_to(m)
            else:
              st.write(f"Skipping record with id: {facility.get('FacilityID', 'N/A')} it does not have valid GEOJSON or coordinates")
        st_folium(m, width=725)
    else:
      st.write("No facilities found based on the filters")
else:
    st.write("No facilities found based on the filters")