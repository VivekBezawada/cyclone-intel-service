CREATE DATABASE "cyclone-intel";
\c "cyclone-intel"
CREATE TABLE cyclone_info(
    cyclone_id TEXT PRIMARY KEY NOT NULL,
    cyclone_name TEXT NOT NULL,
    region TEXT NOT NULL,
    cyclone_status BOOLEAN DEFAULT TRUE
);
\d
CREATE TABLE track_data(
    cyclone_id TEXT REFERENCES cyclone_info(cyclone_id),
    synoptic_time BIGINT NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    intensity INT,
    UNIQUE(cyclone_id, synoptic_time)
);
\d
CREATE TABLE forecast_data(
    cyclone_id TEXT REFERENCES cyclone_info(cyclone_id),
    forecast_time BIGINT NOT NULL,
    predicted_time BIGINT NOT NULL
    latitude FLOAT,
    longitude FLOAT,
    intensity INT,
    UNIQUE(cyclone_id, forecast_time)
);
\d