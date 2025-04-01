import pytest
from scripts.models import Botanist, Location, Record, PlantType, Plant


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
