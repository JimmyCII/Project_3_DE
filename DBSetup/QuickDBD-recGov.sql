-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/j5rXl1
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "Facilities" (
    "Enabled" bool   NOT NULL,
    "FACILITYADDRESS" object   NOT NULL,
    "FacilityAccessibilityText" object   NOT NULL,
    "FacilityAdaAccess" object   NOT NULL,
    "FacilityDescription" object   NOT NULL,
    "FacilityDirections" object   NOT NULL,
    "FacilityEmail" object   NOT NULL,
    "FacilityID" object   NOT NULL,
    "FacilityLatitude" float64   NOT NULL,
    "FacilityLongitude" float64   NOT NULL,
    "FacilityMapURL" object   NOT NULL,
    "FacilityName" object   NOT NULL,
    "FacilityPhone" object   NOT NULL,
    "FacilityReservationURL" object   NOT NULL,
    "FacilityTypeDescription" object   NOT NULL,
    "FacilityUseFeeDescription" object   NOT NULL,
    "GEOJSON" object   NOT NULL,
    "Keywords" object   NOT NULL,
    "LINK" object   NOT NULL,
    "LastUpdatedDate" object   NOT NULL,
    "LegacyFacilityID" object   NOT NULL,
    "MEDIA" object   NOT NULL,
    "ORGANIZATION" object   NOT NULL,
    "OrgFacilityID" object   NOT NULL,
    "PERMITENTRANCE" object   NOT NULL,
    "ParentOrgID" object   NOT NULL,
    "ParentRecAreaID" object   NOT NULL,
    "RECAREA" object   NOT NULL,
    "Reservable" bool   NOT NULL,
    "StayLimit" object   NOT NULL,
    "TOUR" object   NOT NULL,
    CONSTRAINT "pk_Facilities" PRIMARY KEY (
        "FacilityID"
     )
);

CREATE TABLE "Campsites" (
    "CampsiteAccessible" bool   NOT NULL,
    "CampsiteID" object   NOT NULL,
    "CampsiteLatitude" float64   NOT NULL,
    "CampsiteLongitude" float64   NOT NULL,
    "CampsiteName" object   NOT NULL,
    "CampsiteReservable" bool   NOT NULL,
    "CampsiteType" object   NOT NULL,
    "CreatedDate" object   NOT NULL,
    "ENTITYMEDIA" object   NOT NULL,
    "FacilityID" object   NOT NULL,
    "LastUpdatedDate" oject   NOT NULL,
    "Loop" object   NOT NULL,
    "TypeOfUse" object   NOT NULL,
    "EquipmentName" object   NOT NULL,
    "MaxLength" float64   NOT NULL,
    "AttributeName" object   NOT NULL,
    "AttributeValue" object   NOT NULL,
    CONSTRAINT "pk_Campsites" PRIMARY KEY (
        "CampsiteID"
     )
);

CREATE TABLE "Activities" (
    "ActivityID" int64   NOT NULL,
    "ActivityName" object   NOT NULL,
    "FacilityActivityDescription" object   NOT NULL,
    "FacilityActivityFeeDescription" object   NOT NULL,
    "FacilityID" object   NOT NULL,
    CONSTRAINT "pk_Activities" PRIMARY KEY (
        "ActivityID"
     )
);

ALTER TABLE "Campsites" ADD CONSTRAINT "fk_Campsites_FacilityID" FOREIGN KEY("FacilityID")
REFERENCES "Facilities" ("FacilityID");

ALTER TABLE "Activities" ADD CONSTRAINT "fk_Activities_FacilityID" FOREIGN KEY("FacilityID")
REFERENCES "Facilities" ("FacilityID");

