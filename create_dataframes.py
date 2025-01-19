import pandas as pd
import json
import os

def create_dataframe(data, data_key="RECDATA"):
    """Creates a pandas DataFrame from the extracted API data.

    Args:
        data: The list of dictionaries representing the data.
        data_key: The key to use when accessing the data (default is 'RECDATA')

    Returns:
        A pandas DataFrame containing the API data or an empty DataFrame if there was an error.
    """

    if data:
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()
    
def process_facilities_data(facilities_data):
    """Creates multiple DataFrames from the facilities data and related data.

    Args:
        facilities_data: The list of dictionaries representing the facilities from the API.

    Returns:
        A tuple containing the facilities_df, activities_df, campsites_df, and events_df.
    """
    if not facilities_data:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    facilities_df = create_dataframe(facilities_data)
    facility_address_data = []
    activities_data = []
    campsites_data = []
    # events_data = []
    
    permitted_equipment_data = []  # Initialize permitted equipment data
    campsite_attribute_db = []

    for facility in facilities_data:
        facility_id = facility.get('FacilityID')
        if facility_id:
            if 'ACTIVITY' in facility and facility["ACTIVITY"] : #Check if there is data
                for act in facility["ACTIVITY"]:
                    act['FacilityID'] = facility_id
                    activities_data.append(act)

            if 'CAMPSITE' in facility and facility["CAMPSITE"]: #Check if there is data
              for camp in facility["CAMPSITE"]:
                    camp_id = camp.get('CampsiteID')
                    if camp_id:
                        camp['FacilityID'] = facility_id #assign the facility id as a foreign key to be used in tables
                        # Flatten Permitted Equipment data
                        for equipment in camp.get('PERMITTEDEQUIPMENT', []):
                             equipment['CampsiteID'] = camp_id
                             permitted_equipment_data.append(equipment) # adds permitted equipment data into the list
                        for attribute in camp.get('ATTRIBUTES', []):
                            attribute['CampsiteID'] = camp_id
                            campsite_attribute_db.append(attribute) #add the campsite attributes to the list
                        campsites_data.append(camp)
            # if 'EVENT' in facility and facility["EVENT"]: #Check if there is data
            #   for event in facility["EVENT"]:
            #     event['FacilityID'] = facility_id
            #     events_data.append(event)
            if facility.get('FACILITYADDRESS'):  #check that list is not empty
              for address in facility.get('FACILITYADDRESS'):
                address['FacilityID'] = facility_id
                facility_address_data.append(address)
    
    facilities_df = facilities_df.drop(columns = ["ACTIVITY", "CAMPSITE", "EVENT"], errors = 'ignore') #Drop the columns that have blank data

    activities_df = create_dataframe(activities_data)
    campsites_df = create_dataframe(campsites_data)
    # events_df = create_dataframe(events_data)
    permitted_equipment_df = create_dataframe(permitted_equipment_data) # Creates a DF for the permitted equipment
    campsite_attributes_df = create_dataframe(campsite_attribute_db) # Creates a DF for the campsite attributes
    facility_address_df = create_dataframe(facility_address_data)

    # Merge Permitted Equipment Back to the Campsite Table (using a left join)
    #campsites_df = pd.merge(campsites_df, permitted_equipment_df, on="CampsiteID", how='left', suffixes=('', '_permit'))
    #campsites_df = pd.merge(campsites_df, campsite_attributes_df, on="CampsiteID", how='left', suffixes = ('', '_attrib'))
    facilities_df = pd.merge(facilities_df, facility_address_df, on="FacilityID", how='left', suffixes = ('', '_address'))
     # Drop nested columns from campsites table
    campsites_df = campsites_df.drop(columns = ['ENTITYMEDIA', 'PERMITTEDEQUIPMENT', 'ATTRIBUTES','CreatedDate'], errors ='ignore')
    facilities_df = facilities_df.drop(columns = ['FacilityAccessibilityText', 'Enabled', 'LINK', 'MEDIA', 'ORGANIZATION', 'PERMITENTRANCE', 'RECAREA', 'TOUR', 'FacilityAddressType', 'LastUpdatedDate_address'], errors ='ignore')
    activities_df = activities_df.drop(columns = ['FacilityActivityFeeDescription'], errors ='ignore')

    return facilities_df, activities_df, campsites_df, permitted_equipment_df, campsite_attributes_df


def output_to_csv(df, filename):
    """Outputs a Pandas DataFrame to a CSV file.

    Args:
        df: The Pandas DataFrame to output.
        filename: The name of the CSV file to create.
    """
    if not df.empty:
      # Create the CSV Output Folder if it doesn't already exist
      output_dir = 'csv_output'
      if not os.path.exists(output_dir):
          os.makedirs(output_dir) # Creates a new directory

      output_file = os.path.join(output_dir, filename) # Create a path to output file
      df.to_csv(output_file, index=False)
      print(f"DataFrame successfully output to: {output_file}")
    else:
      print("Dataframe was empty and was not output to file.")


if __name__ == "__main__":
    # Load data from file
    data_dir = 'json_output'
    input_file = os.path.join(data_dir, "facilities_data.json")

    try:
      with open(input_file, 'r') as infile:
        facilities_data = json.load(infile)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please check that the script {input_file} was already run.")
        exit()
        

    if facilities_data:
        facilities_df, activities_df, campsites_df, permitted_equipment_df, campsite_attributes_df  = process_facilities_data(facilities_data)

        if not facilities_df.empty:
            print("Facilities DataFrame:")
            facilities_df.info()
            print(facilities_df.head())
            output_to_csv(facilities_df, "facilities.csv")
        else:
            print("Failed to create the facilities Dataframe")
        if not activities_df.empty:
            print("\nActivities DataFrame:")
            activities_df.info()
            print(activities_df.head())
            output_to_csv(activities_df, "activities.csv")
        else:
           print("\nFailed to create the activities Dataframe")
        if not campsites_df.empty:
            print("\nCampsites DataFrame:")
            campsites_df.info()
            print(campsites_df.head())
            output_to_csv(campsites_df, "campsites.csv")
        else:
           print("\nFailed to create the campsites Dataframe")
        # if not events_df.empty:
        #    print("\nEvents DataFrame:")
        #    events_df.info()
        #    print(events_df.head())
        #    output_to_csv(events_df, "events.csv")
        # else:
        #    print("\nEvents Dataframe empty, CSV not created")
        if not permitted_equipment_df.empty:
            print("\nPermitted Equipment DataFrame:")
            permitted_equipment_df.info()
            print(permitted_equipment_df.head())
            output_to_csv(permitted_equipment_df, "permitted_equipment.csv")
        else:
           print("\nFailed to create the permitted equipment Dataframe")
        if not campsite_attributes_df.empty:
            print("\nCampsite Attributes DataFrame:")
            campsite_attributes_df.info()
            print(campsite_attributes_df.head())
            output_to_csv(campsite_attributes_df, "campsite_attributes.csv")
        else:
           print("\nFailed to create the campsite attributes Dataframe")


