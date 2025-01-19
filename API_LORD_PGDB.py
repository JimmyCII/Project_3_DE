# Importing the required libraries:  Check env for libraries, pip ls.  If missing install the following libraries: "pip install fastapi" and "pip install psycopg2"
# How to run the API:  Run the API by executing the following command in the terminal: "uvicorn API_LORD_PGDB:app --reload"
from fastapi import FastAPI, HTTPException
import psycopg2
from typing import List, Dict
import json

app = FastAPI()

# Database connection configuration
DB_HOST = "localhost"  
DB_NAME = "LORD"       
DB_USER = "postgres"      
DB_PASSWORD = "pgadmin"   # Replace with your actual database password

# Function to try connection to the database and returne conn if successful and error if not

def get_db_connection():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

@app.get("/facilities", response_model=List[Dict])
async def read_facilities(state: str = None, ada_accessible: bool = None, group_sites: bool = None):
  print("starting read_facilities()")
  conn = get_db_connection()
  print("connection established")
  cur = conn.cursor()
  print("cursor created")
  query = """
        SELECT
            "FacilityID",
            "FacilityName",
            "FacilityLatitude",
            "FacilityLongitude",
            "GEOJSON",
            "FacilityAdaAccess",
            "RECAREA",
            "Reservable"
        FROM "Facilities"
      """
  print("query definition: ", query)
  conditions = []
  if state:
       print("state filter:", state)
       conditions.append(f""" "RECAREA" LIKE '%{state}%'""")

  if ada_accessible is not None:
        print("ada_accessible filter:", ada_accessible)
        if ada_accessible == True:
            conditions.append(""" "FacilityAdaAccess" LIKE '%Y%' """)
        else:
           conditions.append(""" "FacilityAdaAccess" NOT LIKE '%Y%' """)

  if group_sites is not None:
       print("group_sites filter:", group_sites)
       if group_sites == True:
          conditions.append(""" "FacilityTypeDescription" LIKE '%Group Site%' """)
       else:
          conditions.append(""" "FacilityTypeDescription" NOT LIKE '%Group Site%' """)

  if conditions:
      query += " WHERE " + " AND ".join(conditions)
  print("Query to execute:", query)    
  cur.execute(query)
  print("Query executed")
  rows = cur.fetchall()
  print("Fetched rows")
  conn.close()
  print("Connection closed")

  facilities = []
  for row in rows:
      facility = {
          "FacilityID":row[0],
          "FacilityName":row[1],
           "FacilityLatitude":row[2],
          "FacilityLongitude":row[3],
          "GEOJSON": json.loads(row[4]) if row[4] else None,
          "FacilityAdaAccess": row[5],
          "RECAREA": row[6],
          "Reservable": row[7],
      }
      facilities.append(facility)
  return facilities

@app.get("/campsites", response_model=List[Dict])
async def read_campsites(group_sites:bool = None):
  conn = get_db_connection()
  cur = conn.cursor()
  query = """
      SELECT
          "CampsiteID",
          "CampsiteName",
          "CampsiteLatitude",
          "CampsiteLongitude",
          "CampsiteReservable",
          "FacilityID",
          "TypeOfUse",
          "AttributeName",
           "AttributeValue",
           "MaxLength"

      FROM "Campsites"
    """

  conditions = []
  if group_sites is not None:
      if group_sites == True:
          conditions.append(""" "AttributeName" LIKE '%Group Site Size%' """)
      else:
          conditions.append(""" "AttributeName" NOT LIKE '%Group Site Size%' """)

  if conditions:
    query += " WHERE " + " AND ".join(conditions)

  cur.execute(query)
  rows = cur.fetchall()
  conn.close()

  campsites = []
  for row in rows:
      campsite = {
          "CampsiteID":row[0],
          "CampsiteName":row[1],
          "CampsiteLatitude":row[2],
          "CampsiteLongitude":row[3],
          "CampsiteReservable":row[4],
          "FacilityID":row[5],
          "TypeOfUse": row[6],
          "AttributeName": row[7],
          "AttributeValue": row[8],
          "MaxLength": row[9]
      }
      campsites.append(campsite)
  return campsites