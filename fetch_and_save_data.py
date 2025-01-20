import requests
import json
import os
from config import RecGov_API_Key  #Config file with API key for Recreation.gov located in the same directory and redacted from GitHub using .gitignore
import time
import datetime

base_url = 'https://ridb.recreation.gov/api/v1/'

def fetch_ridb_data(api_key, endpoint, params=None, max_records=float('inf'), states = None, full=True):
    """Fetches data from the Recreation.gov API for various endpoints, handling pagination and rate limits.

    Args:
        api_key: Your Recreation.gov API key.
        endpoint: The API endpoint to hit (e.g., 'facilities', 'activities').
        params: A dictionary of query parameters.
        max_records: The maximum number of records to fetch in total.
        states: A list of states to pull data from.
        full: boolean, if it should pull the full record or not.
    Returns:
        A list of dictionaries representing the data from the API.
    """

    headers = {
        'accept': 'application/json',
        'apikey': api_key
    }
    all_data = []
    limit = 200
    rate_limit_delay = 1.1
    if states is None:
        states = ["AZ"]
    for state in states:
      offset = 0
      while len(all_data) < max_records:
          current_params = {
            'limit': limit,
            'offset': offset,
             'state': state,
             'activity': 'Camping',
              'full': full
            }
          if params:
              current_params.update(params)
          full_url = f"{base_url}{endpoint}"
          # Create the URL string and print it
          url_string = f"{full_url}?{requests.compat.urlencode(current_params)}"
          print(f"Request URL: {url_string}")

          try:
              response = requests.get(full_url, headers=headers, params=current_params, timeout = 30)
              response.raise_for_status()
              data = response.json()

              if not data or "RECDATA" not in data:
                  print(f"No RECDATA found at offset {offset}. Ending for state {state}")
                  break

              all_data.extend(data["RECDATA"])
              offset += limit
              time.sleep(rate_limit_delay) # pause to comply with rate limit
              current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Time Stamp
              print(f"... {current_time}", end="", flush=True) # added print statement

              if data.get("METADATA", {}).get("RESULTS", {}).get("CURRENT_COUNT", 0) < limit:
                    print(f"No more records available at offset {offset} for state {state}. Ending.")
                    break
          except requests.exceptions.RequestException as e:
            print(f"Error during API request at offset {offset}: {e}")
            break

          if len(all_data) >= max_records:
            print(f"Reached maximum number of records {max_records} for state {state}. Ending.")
            break

    return all_data

def fetch_ridb_related_data(api_key, endpoint, facility_id, params=None):
    """Fetches related data from the Recreation.gov API for a specific facility.

    Args:
        api_key: Your Recreation.gov API key.
        endpoint: The API endpoint to hit (e.g., 'activities', 'campsites').
        facility_id: The ID of the facility to fetch data for.
        params: A dictionary of query parameters.
    
    Returns:
        A list of dictionaries representing the data from the API.
    """
    headers = {
        'accept': 'application/json',
        'apikey': api_key
    }
    
    full_url = f"{base_url}facilities/{facility_id}/{endpoint}"
    request_counter = 0 # Added counter to track requests
    start_time = time.time() # start time
    rate_limit = 50 # set the limit
    rate_limit_delay = 1 # set a minimum delay of 1 second for the rate limiting
    try:
      response = requests.get(full_url, headers=headers, params=params, timeout = 30)
      response.raise_for_status()
      data = response.json()
      
      
      request_counter += 1 # increment counter

      elapsed_time = time.time() - start_time # calculate elapsed time.
      if  request_counter > rate_limit and elapsed_time < 1 : # limit to 50 requests per second
            sleep_time = rate_limit_delay - elapsed_time # find how much we need to sleep.
            if sleep_time > 0: # only sleep if we need to.
                time.sleep(sleep_time)
            start_time = time.time() # set new start time
            request_counter = 0 # reset the counter

      if data and "RECDATA" in data:
        return data["RECDATA"]
      else:
        return [] # return empty list
    except requests.exceptions.RequestException as e:
      print(f"Error during API request: {e}")
      return []

if __name__ == "__main__":
    # Example 1: Fetching facilities
    facilities_params = {
      'lastupdated': '10-01-2018',
    }
    facilities_endpoint = 'facilities'
    states = ["AZ", "UT","OR"] # added a list of states
    facilities_data = fetch_ridb_data(RecGov_API_Key, facilities_endpoint, facilities_params, states = states) # Used states and added max records
   # Create a directory if it doesn't exist
    data_dir = 'json_output'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    if facilities_data:
       # Save the raw JSON data to file
      print("Starting to fetch related data...", end="", flush=True) # output message
      start_time = datetime.datetime.now() # start time
      for facility in facilities_data:
          facility_id = facility.get("FacilityID")
          if facility_id:
            # activities = fetch_ridb_related_data(RecGov_API_Key, "activities", facility_id)
            # facility['ACTIVITY'] = activities

            campsites = fetch_ridb_related_data(RecGov_API_Key, "campsites", facility_id)
            facility['CAMPSITE'] = campsites

            # events = fetch_ridb_related_data(RecGov_API_Key, "events", facility_id)
            # facility['EVENT'] = events
            current_time = datetime.datetime.now().strftime("%H:%M:%S") # time stamp
            print(f"... {current_time}", end="", flush=True)

      output_file = os.path.join(data_dir, "facilities_data.json")
      try:
          with open(output_file, 'w') as outfile:
            json.dump(facilities_data, outfile, indent=4)

          print(f"\nRaw JSON data saved to: {output_file}")
          end_time = datetime.datetime.now() #calculate end time
          elapsed_time = end_time - start_time #calculate the time
          print(f"Time taken for fetching related data: {elapsed_time}") # Print the overall time.
      except Exception as e:
          print(f"Error while saving json file: {e}")