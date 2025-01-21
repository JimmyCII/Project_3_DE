# Importing the required libraries:  Check env for libraries, pip ls.  If missing install the following libraries: "pip install fastapi" and "pip install psycopg2"
# How to run the API:  Run the API by executing the following command in the terminal: "uvicorn API_LORD_PGDB:app --reload"
from fastapi import FastAPI, HTTPException
import psycopg2
from typing import List, Dict
import json
# import os
# from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_redoc_html
import re
from config import DBpassword

app = FastAPI(description="API Endpoints for recreational facilities")

# Database connection configuration
DB_HOST = "localhost"  
DB_NAME = "LORD"       
DB_USER = "postgres"      
DB_PASSWORD = DBpassword  # Replace with your actual database password

# Function to try connection to the database and returne conn if successful and error if not

def get_db_connection():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

def create_full_description(summary, path, base_url = "http://127.0.0.1:8000"):
    return f'{summary} {base_url}{path}'

@app.get("/", response_class=HTMLResponse, summary="Welcome page with API documentation")
async def root():
    api_endpoints = []
    for route in app.routes:
        if route.path not in ("/openapi.json", "/docs", "/favicon.ico", "/docs/oauth2-redirect", "/"):
           methods = ", ".join(route.methods)
           description = getattr(route, "summary", route.path)
           full_description = create_full_description(description, route.path)
           api_endpoints.append((route.path, methods, full_description))
    html_content = f"""
        <html>
        <head>
            <title>Welcome to the API!</title>
            <style>
                .endpoint-item {{
                    margin-bottom: 10px;
                }}
                .endpoint-item span {{
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>Welcome to the API!</h1>
            <p>Available API Endpoints:</p>
            <div>
             {''.join([f'<div class="endpoint-item"><span>{methods}:</span> <a href="{path}">{description}</a></div>' for path, methods, description in api_endpoints])}
            </div>
        </body>
        </html>
        """
    return HTMLResponse(content=html_content)

@app.get("/redoc", include_in_schema=False, summary="link to API documentation")
async def redoc():
    return get_redoc_html(
        openapi_url="/openapi.json", title="API documentation"
    )

@app.get("/facilities", response_model=List[Dict], summary="Read Facilities (optional filters by state and ADA accessibility)")
async def read_facilities(state: str = None, ada_accessible: bool = None):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT
            f."FacilityID",
            f."FacilityName",
            f."FacilityLatitude",
            f."FacilityLongitude",
            f."GEOJSON",
            f."FacilityAdaAccess",
            a."AddressStateCode",
            f."Reservable"
        FROM "Facilities" AS f
        LEFT JOIN "FacilityAddresses" AS a ON f."FacilityID" = a."FacilityID"
        WHERE f."FacilityLongitude" !=0 
    """

    conditions = []
    if state:
      conditions.append(f""" a."AddressStateCode" = '{state}'""")

    if ada_accessible is not None:
        if ada_accessible == True:
            conditions.append(""" f."FacilityAdaAccess" LIKE '%Y%' """)
        else:
           conditions.append(""" f."FacilityAdaAccess" NOT LIKE '%Y%' """)


    if conditions:
      query += " AND " + " AND ".join(conditions)
    print(f"SQL Query: {query}") 
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    facilities = []
    for row in rows:
       if row[2] != 0.0 or row[3] != 0.0 :
        try:
          geojson = row[4] if row[4] else None
          if geojson and isinstance(geojson, str):
             geojson = re.sub(r"null", r"None", geojson, flags=re.IGNORECASE)
             geojson = json.dumps(json.loads(geojson)) if geojson else None
            #  geojson = json.loads(geojson)
          else:
            geojson = None
        except json.JSONDecodeError:
           geojson = None

        facility = {
            "FacilityID":row[0],
            "FacilityName":row[1],
            "FacilityLatitude":row[2],
            "FacilityLongitude":row[3],
            "GEOJSON": geojson,
            "FacilityAdaAccess": row[5],
            "AddressStateCode":row[6],
            "Reservable": row[7],
        }
        facilities.append(facility)
      
    return facilities      

@app.get("/campsites", response_model=List[Dict], summary="Read Campsites (optional filters by state)")
async def read_campsites(state:str = None):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
          SELECT
                c."CampsiteID",
                c."CampsiteName",
                c."CampsiteLatitude",
                c."CampsiteLongitude",
                c."CampsiteReservable",
                c."FacilityID",
                c."TypeOfUse",
                a."AttributeName",
                a."AttributeValue",
                fa."AddressStateCode"
        FROM "Campsites" AS c
          LEFT JOIN "CampSiteAttribute" AS a ON c."CampsiteID" = a."CampsiteID"
          LEFT JOIN "Facilities" AS f on c."FacilityID" = f."FacilityID"
          LEFT JOIN "FacilityAddresses" AS fa ON f."FacilityID" = fa."FacilityID"
    """
    conditions = []

    if state:
        conditions.append(f""" fa."AddressStateCode" = '{state}'""")

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
            "AddressStateCode": row[9]
        }
        campsites.append(campsite)
    return campsites

@app.get("/activities", response_model=List[Dict], summary="Read Activities (optional filters by state)")
async def read_activities(state: str = None):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT
          a."ActivityID",
          a."ActivityName",
          a."FacilityActivityDescription",
          f."FacilityID",
          fa."AddressStateCode"
        FROM "Activities" AS a
          LEFT JOIN "Facilities" AS f ON a."FacilityID" = f."FacilityID"
          LEFT JOIN "FacilityAddresses" AS fa ON f."FacilityID" = fa."FacilityID"
    """
    conditions = []
    if state:
        conditions.append(f""" fa."AddressStateCode" = '{state}'""")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    activities = []
    for row in rows:
        activity = {
            "ActivityID":row[0],
            "ActivityName":row[1],
            "FacilityActivityDescription":row[2],
            "FacilityID": row[3],
             "AddressStateCode": row[4]
        }
        activities.append(activity)
    return activities

@app.get("/all_facilities", response_model=List[Dict], summary="Read all Facilities")
async def read_all_facilities():
    conn = get_db_connection()
    cur = conn.cursor()
    query = """ SELECT * FROM "Facilities" """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    facilities = []
    column_names = [desc[0] for desc in cur.description]
    for row in rows:
      facilities.append(dict(zip(column_names, row)))

    return facilities

@app.get("/all_campsites", response_model=List[Dict], summary="Read all Campsites")
async def read_all_campsites():
    conn = get_db_connection()
    cur = conn.cursor()
    query = """ SELECT * FROM "Campsites" """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    campsites = []
    column_names = [desc[0] for desc in cur.description]
    for row in rows:
      campsites.append(dict(zip(column_names, row)))
    return campsites

@app.get("/all_activities", response_model=List[Dict], summary="Read all Activities")
async def read_all_activities():
    conn = get_db_connection()
    cur = conn.cursor()
    query = """ SELECT * FROM "Activities" """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    activities = []
    column_names = [desc[0] for desc in cur.description]
    for row in rows:
       activities.append(dict(zip(column_names, row)))
    return activities

@app.get("/all_campsite_attributes", response_model=List[Dict], summary="Read all Camp Site Attributes")
async def read_all_campsite_attributes():
    conn = get_db_connection()
    cur = conn.cursor()
    query = """ SELECT * FROM "CampSiteAttribute" """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    campsite_attributes = []
    column_names = [desc[0] for desc in cur.description]
    for row in rows:
      campsite_attributes.append(dict(zip(column_names, row)))
    return campsite_attributes

@app.get("/all_permitted_equipment", response_model=List[Dict], summary="Read all Permitted Equipment")
async def read_all_permitted_equipment():
    conn = get_db_connection()
    cur = conn.cursor()
    query = """ SELECT * FROM "PermittedEquipment" """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    permitted_equipment = []
    column_names = [desc[0] for desc in cur.description]
    for row in rows:
      permitted_equipment.append(dict(zip(column_names, row)))
    return permitted_equipment

@app.get("/all_facility_addresses", response_model=List[Dict], summary="Read all Facility Addresses")
async def read_all_facility_addresses():
    conn = get_db_connection()
    cur = conn.cursor()
    query = """ SELECT * FROM "FacilityAddresses" """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    facility_addresses = []
    column_names = [desc[0] for desc in cur.description]
    for row in rows:
        facility_addresses.append(dict(zip(column_names, row)))
    return facility_addresses