# import the necessary libraries  Streamlit "pip install streamlit" 
# How to run the dashboard:  Run the dashboard by executing the following command in the terminal: "streamlit run inDevelopment_dashboard.py"
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import json

API_URL = "http://127.0.0.1:8000"  # Replace if your API is running elsewhere

st.title("Recreational Facilities Dashboard")

def get_facilities(state=None, ada_accessible=None):
  params = {}
  if state:
    params["state"] = state
  if ada_accessible is not None:
    params["ada_accessible"] = ada_accessible
  response = requests.get(f"{API_URL}/facilities", params=params)
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"Error fetching facilities: {response.status_code}")
    return []

def get_campsites(state = None):
    params = {}

    if state:
        params["state"] = state
    response = requests.get(f"{API_URL}/campsites", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching campsites: {response.status_code}")
        return []
def get_activities(state = None):
    params = {}
    if state:
        params["state"] = state
    response = requests.get(f"{API_URL}/activities", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching activities: {response.status_code}")
        return []
def get_all_facilities():
    response = requests.get(f"{API_URL}/all_facilities")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching all facilities: {response.status_code}")
        return []

def get_all_campsites():
    response = requests.get(f"{API_URL}/all_campsites")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching all campsites: {response.status_code}")
        return []

def get_all_activities():
    response = requests.get(f"{API_URL}/all_activities")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching all activities: {response.status_code}")
        return []

def get_all_campsite_attributes():
  response = requests.get(f"{API_URL}/all_campsite_attributes")
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"Error fetching all campsite attributes: {response.status_code}")
    return []
def get_all_permitted_equipment():
  response = requests.get(f"{API_URL}/all_permitted_equipment")
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"Error fetching all permitted equipment: {response.status_code}")
    return []
def get_all_facility_addresses():
  response = requests.get(f"{API_URL}/all_facility_addresses")
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"Error fetching all facility addresses: {response.status_code}")
    return []


#Sidebar with filtering options
with st.sidebar:
  st.header("Filter Facilities")
  selected_state = st.text_input("Filter by State (e.g., 'AZ')")
  ada_access_filter = st.checkbox("Show ADA Accessible Facilities")


# Fetch Data from API
facilities = get_facilities(selected_state, ada_access_filter)
campsites = get_campsites(state=selected_state)
activities = get_activities(state = selected_state)

all_facilities = get_all_facilities()
all_campsites = get_all_campsites()
all_activities = get_all_activities()
all_campsite_attributes = get_all_campsite_attributes()
all_permitted_equipment = get_all_permitted_equipment()
all_facility_addresses = get_all_facility_addresses()


# Facility Map
st.header("Facilities Map")

if facilities:
  m = folium.Map(location=[facilities[0]["FacilityLatitude"], facilities[0]["FacilityLongitude"]], zoom_start=6)

  for facility in facilities:
      if facility["GEOJSON"]:
         try:
              geo_data = facility["GEOJSON"]
              folium.GeoJson(geo_data,
                           popup=f"<b>Facility:</b> {facility['FacilityName']}<br><b>State:</b> {facility['AddressStateCode']}<br><b>Reservable:</b> {facility['Reservable']}<br><b>ADA:</b> {facility['FacilityAdaAccess']}",
                          ).add_to(m)
         except Exception as e:
             print(f"Error processing geojson data for {facility['FacilityID']}: {e}")
      else:
          folium.Marker(
              location=[facility["FacilityLatitude"], facility["FacilityLongitude"]],
              popup=f"<b>Facility:</b> {facility['FacilityName']}<br><b>State:</b> {facility['AddressStateCode']}<br><b>Reservable:</b> {facility['Reservable']}<br><b>ADA:</b> {facility['FacilityAdaAccess']}",
          ).add_to(m)
  st_folium(m, width=725)
else:
  st.write("No facilities found based on the filters")

if campsites:
  st.header("Campsites")
  for site in campsites:
    if site["AttributeName"] and site["AttributeValue"] and site["MaxLength"]:
        st.write(f"Campsite: {site['CampsiteName']}, State: {site['AddressStateCode']},  Type: {site['TypeOfUse']}, Max Group size: {site['AttributeValue']}, Max Length {site['MaxLength']}, reservable: {site['CampsiteReservable']} for facility: {site['FacilityID']}")
    else:
       st.write(f"Campsite: {site['CampsiteName']}, State: {site['AddressStateCode']}, Type: {site['TypeOfUse']}, reservable: {site['CampsiteReservable']} for facility: {site['FacilityID']}")
else:
  st.write("No campsites found based on the filters")

if activities:
  st.header("Activities")
  for activity in activities:
      st.write(f"Activity: {activity['ActivityName']}, Type: {activity['FacilityActivityDescription']} for facility: {activity['FacilityID']} in state: {activity['AddressStateCode']}")
else:
  st.write("No activities found based on the filters")

if all_facilities:
    st.header("All facilities")
    st.write(all_facilities)

if all_campsites:
     st.header("All campsites")
     st.write(all_campsites)

if all_activities:
    st.header("All activities")
    st.write(all_activities)

if all_campsite_attributes:
    st.header("All Campsite Attributes")
    st.write(all_campsite_attributes)

if all_permitted_equipment:
   st.header("All Permitted Equipment")
   st.write(all_permitted_equipment)

if all_facility_addresses:
   st.header("All Facility Addresses")
   st.write(all_facility_addresses)