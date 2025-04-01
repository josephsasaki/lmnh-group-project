import pytest
from scripts.models import Botanist, Location, Record, PlantType, Plant


FULL_RAW_JSON = {
    "botanist": {
        "email": "test.test@lnhm.co.uk",
        "name": "Test Test",
        "phone": "07517966650"
    },
    "images": {
        "license": 451,
        "license_name": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "medium_url": "https://test.com/storage/image/image.jpg",
        "original_url": "https://test.com/storage/image/orig_image.jpg",
        "regular_url": "https://test.com/storage/image/image.jpg",
        "small_url": "https://test.com/storage/image/image.jpg",
        "thumbnail": "https://test.com/storage/image/image.jpg",
    },
    "last_watered": "Mon, 31 Mar 2025 13:23:01 GMT",
    "name": "Palm Tree",
    "origin_location": [
        "5.27247",
        "-3.59625",
        "Bonoua",
        "CI",
        "Africa/Abidjan"
    ],
    "plant_id": 8,
    "recording_taken": "2025-04-01 07:38:10",
    "scientific_name": ["Arecaceae"],
    "soil_moisture": 34.68277436878728,
    "temperature": 11.541849271315279
}


class TestBotanist:

    def test_botanist_init():
        raw_json = {
            "email": "test.test@lmnh.com",
            "name": "Test Test",
            "phone": "07517966650"
        }
        botanist = Botanist(raw_json)
        assert botanist._Botanist__email == "test.test@lmnh.com"
        assert botanist._Botanist__name == "Test Test"
        assert botanist._Botanist__phone == "07517966650"

    def test_botanist_missing_email():
        raw_json = {
            "name": "Test Test",
            "phone": "07517966650"
        }
        with pytest.raises(ValueError):
            botanist = Botanist(raw_json)

    def test_botanist_missing_name():
        raw_json = {
            "email": "test.test@lmnh.com",
            "phone": "07517966650"
        }
        with pytest.raises(ValueError):
            botanist = Botanist(raw_json)

    def test_botanist_missing_phone():
        raw_json = {
            "name": "Test Test",
            "email": "test.test@lmnh.com",
        }
        with pytest.raises(ValueError):
            botanist = Botanist(raw_json)

    def test_botanist_invalid_email():
        raw_json = {
            "email": "test.test",
            "name": "Test Test",
            "phone": "07517966650",
        }
        with pytest.raises(ValueError):
            botanist = Botanist(raw_json)

    def test_botanist_invalid_name():
        raw_json = {
            "email": "test.test@lmnh.com",
            "name": "",
            "phone": "07517966650",
        }
        with pytest.raises(ValueError):
            botanist = Botanist(raw_json)

    def test_botanist_invalid_phone():
        raw_json = {
            "email": "test.test@lmnh.com",
            "name": "Test Test",
            "phone": "5739",
        }
        with pytest.raises(ValueError):
            botanist = Botanist(raw_json)

    def test_botanist_invalid_phone():
        raw_json = {
            "email": "test.test@lmnh.com",
            "name": "Test Test",
            "phone": "5739",
        }
        with pytest.raises(ValueError):
            botanist = Botanist(raw_json)


class TestLocation:

    def test_location_init():
        raw_json = [
            "5.27247",
            "-3.59625",
            "Bonoua",
            "CI",
            "Africa/Abidjan"
        ]
        location = Location(raw_json)
        assert location._Location__latitude == 5.27247
        assert location._Location__longitude == -3.59625
        assert location._Location__city == "Bonoua"
        assert location._Location__country == "CI"
        assert location._Location__capital == "Abidjan"
        assert location._Location__continent == "Africa"

    def test_location_missing_latitude():
        raw_json = [
            "-3.59625",
            "Bonoua",
            "CI",
            "Africa/Abidjan"
        ]
        with pytest.raises(ValueError):
            location = Location(raw_json)

    def test_location_missing_longitude():
        raw_json = [
            "5.27247"
            "Bonoua",
            "CI",
            "Africa/Abidjan"
        ]
        with pytest.raises(ValueError):
            location = Location(raw_json)

    def test_location_missing_city():
        raw_json = [
            "5.27247"
            "-3.59625",
            "CI",
            "Africa/Abidjan"
        ]
        with pytest.raises(ValueError):
            location = Location(raw_json)

    def test_location_missing_country():
        raw_json = [
            "5.27247"
            "-3.59625",
            "Bonoua",
            "Africa/Abidjan"
        ]
        with pytest.raises(ValueError):
            location = Location(raw_json)

    def test_location_missing_continent():
        raw_json = [
            "5.27247"
            "-3.59625",
            "Bonoua",
            "CI",
            "/Abidjan"
        ]
        with pytest.raises(ValueError):
            location = Location(raw_json)

    def test_location_missing_capital():
        raw_json = [
            "5.27247"
            "-3.59625",
            "Bonoua",
            "CI",
            "Africa/"
        ]
        with pytest.raises(ValueError):
            location = Location(raw_json)

    def test_location_missing_continent_and_capital():
        raw_json = [
            "5.27247"
            "-3.59625",
            "Bonoua",
            "CI",
        ]
        with pytest.raises(ValueError):
            location = Location(raw_json)


class TestRecord:

    def test_record_init():
        raw_json = {
            "soil_moisture": 34.68277436878728,
            "temperature": 11.541849271315279,
            "recording_taken": "2025-04-01 07:38:10",
        }
        record = Record(raw_json)
        assert record._Record__soil_moisture == 34.68
        assert record._Record__temperature == 11.54
        assert record._Record__taken.year == 2025
        assert record._Record__taken.month == 4
        assert record._Record__taken.day == 1
        assert record._Record__taken.hour == 7
        assert record._Record__taken.minute == 38
        assert record._Record__taken.second == 10

    def test_record_missing_soil_moisture():
        raw_json = {
            "soil_moisture": 34.68277436878728,
            "temperature": 11.541849271315279,
            "recording_taken": "2025-04-01 07:38:10",
        }
        with pytest.raises(ValueError):
            record = Record(raw_json)

    def test_record_missing_soil_moisture():
        raw_json = {
            "temperature": 11.541849271315279,
            "recording_taken": "2025-04-01 07:38:10",
        }
        with pytest.raises(ValueError):
            record = Record(raw_json)

    def test_record_missing_temperature():
        raw_json = {
            "soil_moisture": 34.68277436878728,
            "recording_taken": "2025-04-01 07:38:10",
        }
        with pytest.raises(ValueError):
            record = Record(raw_json)

    def test_record_missing_recording_taken():
        raw_json = {
            "soil_moisture": 34.68277436878728,
            "temperature": 11.541849271315279,
        }
        with pytest.raises(ValueError):
            record = Record(raw_json)

    def test_record_invalid_soil_moisture():
        raw_json = {
            "soil_moisture": 34.68277436878728,
            "temperature": 11.541849271315279,
            "recording_taken": "2025-04-01 07:38:10",
        }
        with pytest.raises(ValueError):
            record = Record(raw_json)


class TestPlantType:

    def test_plant_type_init():
        raw_json = {
            "name": "Palm Tree",
            "scientific_name": "Arecaceae",
            "images": {
                "license": 451,
                "license_name": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
                "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                "medium_url": "https://test.com/storage/image/image.jpg",
                "original_url": "https://test.com/storage/image/orig_image.jpg",
                "regular_url": "https://test.com/storage/image/image.jpg",
                "small_url": "https://test.com/storage/image/image.jpg",
                "thumbnail": "https://test.com/storage/image/image.jpg",
            },
        }
        plant_type = PlantType(raw_json)
        assert plant_type._PlantType__name == "Palm Tree"
        assert plant_type._PlantType__scientific_name == "Arecaceae"
        assert plant_type._PlantType__image_url == "https://test.com/storage/image/orig_image.jpg"

    def test_plant_missing_name():
        raw_json = {
            "scientific_name": "Arecaceae",
            "images": {
                "license": 451,
                "license_name": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
                "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                "medium_url": "https://test.com/storage/image/image.jpg",
                "original_url": "https://test.com/storage/image/orig_image.jpg",
                "regular_url": "https://test.com/storage/image/image.jpg",
                "small_url": "https://test.com/storage/image/image.jpg",
                "thumbnail": "https://test.com/storage/image/image.jpg",
            },
        }
        with pytest.raises(ValueError):
            PlantType(raw_json)

    def test_plant_missing_scientific_name_allowed():
        raw_json = {
            "name": "Palm Tree",
            "images": {
                "license": 451,
                "license_name": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
                "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                "medium_url": "https://test.com/storage/image/image.jpg",
                "original_url": "https://test.com/storage/image/orig_image.jpg",
                "regular_url": "https://test.com/storage/image/image.jpg",
                "small_url": "https://test.com/storage/image/image.jpg",
                "thumbnail": "https://test.com/storage/image/image.jpg",
            },
        }
        plant_type = PlantType(raw_json)
        assert plant_type._PlantType__name == "Palm Tree"
        assert plant_type._PlantType__scientific_name is None

    def test_plant_type_missing_image_allowed():
        raw_json = {
            "name": "Palm Tree",
            "scientific_name": "Arecaceae",
        }
        plant_type = PlantType(raw_json)
        assert plant_type._PlantType__name == "Palm Tree"
        assert plant_type._PlantType__scientific_name == "Arecaceae"
        assert plant_type._PlantType__image_url is None


class TestPlant():

    def test_plant_init_botanist():
        raw_json = FULL_RAW_JSON
        plant = Plant(raw_json)
        assert plant._Plant__botanist._Botanist__email == "test.test@lnhm.co.uk"
        assert plant._Plant__botanist._Botanist__name == "Test Test"
        assert plant._Plant__botanist._Botanist__phone == "07517966650"

    def test_plant_init_location():
        raw_json = FULL_RAW_JSON
        plant = Plant(raw_json)
        assert plant._Plant__location._Location__latitude == 5.27247
        assert plant._Plant__location._Location__longitude == -3.59625
        assert plant._Plant__location._Location__city == "Bonoua"
        assert plant._Plant__location._Location__country == "CI"
        assert plant._Plant__location._Location__capital == "Abidjan"
        assert plant._Plant__location._Location__continent == "Africa"

    def test_plant_init_record():
        raw_json = FULL_RAW_JSON
        plant = Plant(raw_json)
        assert plant._Plant__record._Record__soil_moisture == 34.68
        assert plant._Plant__record._Record__temperature == 11.54
        assert plant._Plant__record._Record__taken.year == 2025
        assert plant._Plant__record._Record__taken.month == 4
        assert plant._Plant__record._Record__taken.day == 1
        assert plant._Plant__record._Record__taken.hour == 7
        assert plant._Plant__record._Record__taken.minute == 38
        assert plant._Plant__record._Record__taken.second == 10

    def test_plant_init_plant_type():
        raw_json = FULL_RAW_JSON
        plant = Plant(raw_json)
        assert plant._Plant__plant_type._PlantType__name == "Palm Tree"
        assert plant._Plant__plant_type._PlantType__scientific_name == "Arecaceae"

    def test_plant_init():
        raw_json = FULL_RAW_JSON
        plant = Plant(raw_json)
        assert plant._Plant__plant_number == 8
        assert plant._Plant__last_watered.year == 2025
        assert plant._Plant__last_watered.month == 31
        assert plant._Plant__last_watered.day == 3
        assert plant._Plant__last_watered.hour == 13
        assert plant._Plant__last_watered.minute == 23
        assert plant._Plant__last_watered.second == 1
