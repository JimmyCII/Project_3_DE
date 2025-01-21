TRUNCATE TABLE "CampSiteAttribute" CASCADE;
TRUNCATE TABLE "PermittedEquipment" CASCADE;
TRUNCATE TABLE "Campsites" CASCADE;
TRUNCATE TABLE "Activities" CASCADE;
TRUNCATE TABLE "Facilities" CASCADE;

DROP TABLE "CampSiteAttribute";
DROP TABLE "PermittedEquipment";
DROP TABLE "Campsites";
DROP TABLE "Activities";
DROP TABLE "Facilities";

CREATE TABLE "Facilities" (
    "FACILITYADDRESS" TEXT   NULL,
    "FacilityAdaAccess" TEXT NULL,
    "FacilityDescription" TEXT   NULL,
    "FacilityDirections" TEXT   NULL,
    "FacilityEmail" TEXT   NULL,
    "FacilityID" TEXT   NOT NULL,
    "FacilityLatitude" FLOAT  NULL,
    "FacilityLongitude" FLOAT NULL,
    "FacilityMapURL" TEXT   NULL,
    "FacilityName" TEXT   NULL,
    "FacilityPhone" TEXT  NULL,
    "FacilityReservationURL" TEXT NULL,
    "FacilityTypeDescription" TEXT NULL,
    "FacilityUseFeeDescription" TEXT NULL,
    "GEOJSON" TEXT   NULL,
    "Keywords" TEXT  NULL,
    "LastUpdatedDate" TEXT   NULL,
    "LegacyFacilityID" TEXT  NULL,
    "OrgFacilityID" TEXT   NULL,
    "ParentOrgID" TEXT   NULL,
    "ParentRecAreaID" TEXT   NULL,
    "Reservable" BOOLEAN   NULL,
    "StayLimit" TEXT   NULL,
    
    CONSTRAINT "pk_Facilities" PRIMARY KEY (
        "FacilityID"
     )
);

CREATE TABLE "Campsites" (
    "CampsiteAccessible" BOOLEAN   NULL,
    "CampsiteID" TEXT   NOT NULL,
    "CampsiteLatitude" FLOAT   NULL,
    "CampsiteLongitude" FLOAT   NULL,
    "CampsiteName" TEXT   NULL,
    "CampsiteReservable" BOOLEAN   NULL,
    "CampsiteType" TEXT   NULL,
    "FacilityID" TEXT   NULL,
    "LastUpdatedDate" TEXT   NULL,
    "Loop" TEXT   NULL,
    "TypeOfUse" TEXT   NULL,
    CONSTRAINT "pk_Campsites" PRIMARY KEY (
        "CampsiteID"
     )
);

CREATE TABLE "Activities" (
    "ActivityID" INT   NOT NULL,
    "ActivityName" TEXT  NOT NULL,
    "FacilityActivityDescription" TEXT   NULL,
    "FacilityID" TEXT   NOT NULL
);

CREATE TABLE "CampSiteAttribute" (
    "AttributeName" TEXT   NOT NULL,
    "AttributeValue" TEXT   NULL,
    "CampsiteID" TEXT   NOT NULL
);

CREATE TABLE "PermittedEquipment" (
    "EquipmentName" TEXT   NOT NULL,
    "MaxLength " INT   Not NULL,
    "CampsiteID" TEXT   NOT NULL
);

CREATE TABLE "FacilityAddresses" (
    "AddressCountryCode" TEXT    NULL,
    "AddressStateCode" TEXT   NULL,
    "City" TEXT   NULL,
    "FacilityAddressID" TEXT   NULL,
    "FacilityID" TEXT   NULL,
    "FacilityStreetAddress1" TEXT    NULL,
    "FacilityStreetAddress2" TEXT    NULL,
    "FacilityStreetAddress3" TEXT    NULL,
    "LastUpdatedDate" Text  NULL,
    "PostalCode" TEXT   NULL
);

ALTER TABLE "Campsites" ADD CONSTRAINT "fk_Campsites_FacilityID" FOREIGN KEY("FacilityID")
REFERENCES "Facilities" ("FacilityID");

ALTER TABLE "Activities" ADD CONSTRAINT "fk_Activities_FacilityID" FOREIGN KEY("FacilityID")
REFERENCES "Facilities" ("FacilityID");

ALTER TABLE "CampSiteAttribute" ADD CONSTRAINT "fk_CampSiteAttribute_CampsiteID" FOREIGN KEY("CampsiteID")
REFERENCES "Campsites" ("CampsiteID");

ALTER TABLE "PermittedEquipment" ADD CONSTRAINT "fk_PermittedEquipment_PermittedEquipment" FOREIGN KEY("CampsiteID")
REFERENCES "Campsites" ("CampsiteID");

ALTER TABLE "FacilityAddresses" ADD CONSTRAINT "fk_FacilityAddresses_FacilityID" FOREIGN KEY("FacilityID")
REFERENCES "Facilities" ("FacilityID");


SELECT 'Facilities' AS table_name, COUNT(*) AS row_count FROM "Facilities"
UNION ALL
SELECT 'Campsites' AS table_name, COUNT(*) AS row_count FROM "Campsites"
UNION ALL
SELECT 'CampSiteAttribute' AS table_name, COUNT(*) AS row_count FROM "CampSiteAttribute"
UNION ALL
SELECT 'Activities' AS table_name, COUNT(*) AS row_count FROM "Activities"
UNION ALL
SELECT 'PermittedEquipment' AS table_name, COUNT(*) AS row_count FROM "PermittedEquipment"
UNION ALL
SELECT 'FacilityAddresses' AS table_name, COUNT(*) AS row_count FROM "FacilityAddresses";

SELECT
	f."FacilityName",
	f."FacilityTypeDescription",
	f."FacilityPhone",
	f."GEOJSON",
	f."Reservable",
	a."FacilityStreetAddress1",
	a."FacilityStreetAddress2",
	a."City",
	a."AddressStateCode",
	a."PostalCode",
	c."CampsiteAccessible",
	c."CampsiteName",
	c."CampsiteReservable",
	c."CampsiteType",
	c."Loop",
	c."TypeOfUse"
FROM
	"Facilities" AS f	
JOIN 
	"FacilityAddresses" AS a ON f."FacilityID" =a."FacilityID"
JOIN	
	"Campsites" AS c on f."FacilityID" =c."FacilityID"
WHERE
	a."AddressStateCode" ='AZ' and c."CampsiteAccessible" = 'true'
	

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

UPDATE "Facilities"
SET "GEOJSON" = replace("GEOJSON", '''', '"');

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
         LEFT JOIN "FacilityAddresses" AS a ON f."FacilityID" = a."FacilityID";


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
        WHERE f."GEOJSON" IS NULL OR json_typeof(f."GEOJSON"::JSON)='object'


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
        WHERE f."FacilityLongitude" !=0;