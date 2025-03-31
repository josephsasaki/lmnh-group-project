DROP TABLE IF EXISTS record;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS plant_type;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS continent;

CREATE TABLE continent (
    continent_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    continent_name VARCHAR(50) UNIQUE
),

CREATE TABLE country (
    country_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    country_name VARCHAR(50) UNIQUE,
    country_capital VARCHAR(50) UNIQUE,
    continent_id SMALLINT NOT NULL,
    CONSTRAINT fk_country_continent FOREIGN KEY (continent_id) 
        REFERENCES continent (continent_id) 
),

CREATE TABLE city (
    city_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    city_name VARCHAR(50) UNIQUE,
    city_latitude FLOAT,
    city_longitude FLOAT,
    country_id SMALLINT NOT NULL,
    CONSTRAINT fk_city_country FOREIGN KEY (country_id) 
        REFERENCES country (country_id) 
),

CREATE TABLE plant_type (
    plant_type_id SMALLINT PRIMARY KEY,
    plant_type_name VARCHAR(100),
    plant_type_scientific_name VARCHAR(100),
    plant_image_url VARCHAR(100)
),

CREATE TABLE botanist(
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    botanist_name VARCHAR(50),
    botanist_email VARCHAR(100),
    botanist_phone VARCHAR(50)
),

CREATE TABLE plant(
    plant_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    plant_type_id SMALLINT NOT NULL,
    botanist_id SMALLINT NOT NULL,
    city_id SMALLINT NOT NULL,
    plant_last_watered DATETIME,
    CONSTRAINT fk_plant_plant_type FOREIGN KEY (plant_type_id) 
        REFERENCES plant_type (plant_type_id),
    CONSTRAINT fk_plant_botanist FOREIGN KEY (botanist_id) 
        REFERENCES botanist (botanist_id),
    CONSTRAINT fk_plant_city FOREIGN KEY (city_id) 
        REFERENCES city (city_id) 
),

CREATE TABLE record(
    record_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    record_soil_temperature FLOAT,
    record_temperature FLOAT,
    record_time DATETIME
)



