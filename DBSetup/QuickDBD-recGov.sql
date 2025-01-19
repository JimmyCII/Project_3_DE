-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/j5rXl1
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


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

