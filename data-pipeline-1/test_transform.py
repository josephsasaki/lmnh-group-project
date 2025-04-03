import pytest
from transform import PlantRecordingFactory


@pytest.fixture
def json_response_list():
    return [
        {
            "botanist": {
                "email": "gertrude.jekyll@lnhm.co.uk",
                "name": "Gertrude Jekyll",
                "phone": "001-481-273-3691x127"
            },
            "images": {
                "license": 4,
                "license_name": "Attribution License",
                "license_url": "https://creativecommons.org/licenses/by/2.0/",
                "medium_url": "https://perenual.com/storage/species_image/2015_colocasia_esculenta/medium/24325097844_14719030a3_b.jpg",
                "original_url": "https://perenual.com/storage/species_image/2015_colocasia_esculenta/og/24325097844_14719030a3_b.jpg",
                "regular_url": "https://perenual.com/storage/species_image/2015_colocasia_esculenta/regular/24325097844_14719030a3_b.jpg",
                "small_url": "https://perenual.com/storage/species_image/2015_colocasia_esculenta/small/24325097844_14719030a3_b.jpg",
                "thumbnail": "https://perenual.com/storage/species_image/2015_colocasia_esculenta/thumbnail/24325097844_14719030a3_b.jpg"
            },
            "last_watered": "Mon, 31 Mar 2025 14:17:54 GMT",
            "name": "Colocasia Esculenta",
            "origin_location": [
                "29.65163",
                "-82.32483",
                "Gainesville",
                "US",
                "America/New_York"
            ],
            "plant_id": 14,
            "recording_taken": "2025-04-01 14:12:18",
            "scientific_name": [
                "Colocasia esculenta"
            ],
            "soil_moisture": 19.035973523047986,
            "temperature": 13.110190553320937
        },
        {
            "botanist": {
                "email": "eliza.andrews@lnhm.co.uk",
                "name": "Eliza Andrews",
                "phone": "(846)669-6651x75948"
            },
            "last_watered": "Tue, 01 Apr 2025 13:13:51 GMT",
            "name": "Brugmansia X Candida",
            "origin_location": [
                "32.5007",
                "-94.74049",
                "Longview",
                "US",
                "America/Chicago"
            ],
            "plant_id": 12,
            "recording_taken": "2025-04-01 16:35:10",
            "soil_moisture": 88.13393716797643,
            "temperature": 12.839847474341976
        },
        {
            "botanist": {
                "email": "carl.linnaeus@lnhm.co.uk",
                "name": "Carl Linnaeus",
                "phone": "(146)994-1635x35992"
            },
            "last_watered": "Tue, 01 Apr 2025 14:29:39 GMT",
            "name": "Manihot Esculenta ‘Variegata’",
            "origin_location": [
                "51.30001",
                "13.10984",
                "Oschatz",
                "DE",
                "Europe/Berlin"
            ],
            "plant_id": 18,
            "recording_taken": "2025-04-01 16:35:36",
            "soil_moisture": 92.662749492233,
            "temperature": 9.071194098251544
        }
    ]


def test_list_with_multiple_responses(json_response_list):
    factory = PlantRecordingFactory(json_response_list)
    plant_list = factory.produce_plant_objects()
    assert len(plant_list) == 3
    assert plant_list[0]._Plant__botanist._Botanist__name == "Gertrude Jekyll"
    assert plant_list[1]._Plant__plant_type._PlantType__image_url == None
    assert plant_list[2]._Plant__last_watered.day == 1
    assert plant_list[2]._Plant__last_watered.month == 4
    assert plant_list[2]._Plant__last_watered.hour == 14


def test_list_with_multiple_responses_ignore_error(json_response_list):
    factory = PlantRecordingFactory(json_response_list + [{"very": "invalid"}])
    plant_list = factory.produce_plant_objects()
    assert len(plant_list) == 3
    assert plant_list[0]._Plant__botanist._Botanist__name == "Gertrude Jekyll"
    assert plant_list[1]._Plant__plant_type._PlantType__image_url == None
    assert plant_list[2]._Plant__last_watered.day == 1
    assert plant_list[2]._Plant__last_watered.month == 4
    assert plant_list[2]._Plant__last_watered.hour == 14


def test_list_one_response(json_response_list):
    factory = PlantRecordingFactory(json_response_list[:1])
    plant_list = factory.produce_plant_objects()
    assert len(plant_list) == 1
    assert plant_list[0]._Plant__botanist._Botanist__name == "Gertrude Jekyll"
    assert plant_list[0]._Plant__last_watered.day == 31
    assert plant_list[0]._Plant__last_watered.month == 3
    assert plant_list[0]._Plant__location._Location__continent == "America"
    assert plant_list[0]._Plant__location._Location__country == "United States of America"


def test_empty_list():
    factory = PlantRecordingFactory([])
    plant_list = factory.produce_plant_objects()
    assert len(plant_list) == 0
