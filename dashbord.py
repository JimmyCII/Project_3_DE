# import the necessary libraries  Streamlit "pip install streamlit" 
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import json

API_URL = "http://127.0.0.1:8000"  # Replace if your API is running elsewhere

st.title("Recreational Facilities Dashboard")

def get_facilities(state=None, ada_accessible=None, group_sites=None):
  params = {}
  if state:
    params["state"] = state
  if ada_accessible is not None:
    params["ada_accessible"] = ada_accessible
  if group_sites is not None:
    params["group_sites"] = group_sites
  response = requests.get(f"{API_URL}/facilities", params=params)
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"Error fetching facilities: {response.status_code}")
    return []

def get_campsites(group_sites = None):
    params = {}
    if group_sites is not None:
        params["group_sites"] = group_sites
    response = requests.get(f"{API_URL}/campsites", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching campsites: {response.status_code}")
        return []

#Sidebar with filtering options
with st.sidebar:
  st.header("Filter Facilities")
  selected_state = st.text_input("Filter by State (e.g., 'Utah')")
  ada_access_filter = st.checkbox("Show ADA Accessible Facilities")
  group_sites_filter = st.checkbox("Show Facilities with Group Sites")


# Fetch Data from API
facilities = get_facilities(selected_state, ada_access_filter, group_sites_filter)
campsites = get_campsites(group_sites = group_sites_filter)

# Facility Map
st.header("Facilities Map")

if facilities:
  m = folium.Map(location=[facilities[0]["FacilityLatitude"], facilities[0]["FacilityLongitude"]], zoom_start=6)

  for facility in facilities:
      if facility["GEOJSON"]:
         try:
              geo_data = facility["GEOJSON"]
              folium.GeoJson(geo_data,
                           popup=f"<b>Facility:</b> {facility['FacilityName']}<br><b>Reservable:</b> {facility['Reservable']}<br><b>ADA:</b> {facility['FacilityAdaAccess']}",
                          ).add_to(m)
         except Exception as e:
             print(f"Error processing geojson data for {facility['FacilityID']}: {e}")
      else:
          folium.Marker(
              location=[facility["FacilityLatitude"], facility["FacilityLongitude"]],
              popup=f"<b>Facility:</b> {facility['FacilityName']}<br><b>Reservable:</b> {facility['Reservable']}<br><b>ADA:</b> {facility['FacilityAdaAccess']}",
          ).add_to(m)
  st_folium(m, width=725)
else:
  st.write("No facilities found based on the filters")


if campsites:
  st.header("Campsites with Group Sites")

  for site in campsites:
      if site["AttributeName"] and site["AttributeValue"] and site["MaxLength"]:
       st.write(f"Campsite: {site['CampsiteName']}, Type: {site['TypeOfUse']}, Max Group size: {site['AttributeValue']}, Max Length {site['MaxLength']}, reservable: {site['CampsiteReservable']} for facility: {site['FacilityID']}")
      else:
       st.write(f"Campsite: {site['CampsiteName']}, Type: {site['TypeOfUse']}, reservable: {site['CampsiteReservable']} for facility: {site['FacilityID']}")
else:
     st.write("No campsites with group sites based on the filters")