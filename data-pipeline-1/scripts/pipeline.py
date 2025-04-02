
from extract import Extract
from transform import Transform
from load import Load


JSON_DATA = [
    {
        'botanist': {'email': 'gertrude.jekyll@lnhm.co.uk', 'name': 'Gertrude Jekyll', 'phone': '001-481-273-3691x127'},
        'last_watered': 'Tue, 01 Apr 2025 13:54:32 GMT',
        'name': 'Venus flytrap',
        'origin_location': ['33.95015', '-118.03917', 'South Whittier', 'US', 'America/Los_Angeles'],
        'plant_id': 1,
        'recording_taken': '2025-04-02 09:31:07',
        'soil_moisture': 30.5159720246063,
        'temperature': 12.032964339199571
    }, {
        'botanist': {'email': 'carl.linnaeus@lnhm.co.uk', 'name': 'Carl Linnaeus', 'phone': '(146)994-1635x35992'},
        'last_watered': 'Tue, 01 Apr 2025 14:10:54 GMT',
        'name': 'Corpse flower',
        'origin_location': ['7.65649', '4.92235', 'Efon-Alaaye', 'NG', 'Africa/Lagos'],
        'plant_id': 2,
        'recording_taken': '2025-04-02 09:31:11',
        'soil_moisture': 36.653553883530485,
        'temperature': 9.133961576689128
    }
]

if __name__ == "__main__":
    data = Extract.extract()
    plants = Transform.create_plant_objects(data)
    with Load.get_connection() as connection:
        # Add any new botanists
        Load.add_new_botanists(
            botanists=[plant.get_botanist() for plant in plants],
            connection=connection
        )
        # Add any new continents, countries and cities
        locations = [plant.get_location() for plant in plants]
        Load.add_new_continents(locations, connection)
        Load.add_new_countries(locations, connection)
        Load.add_new_cities(locations, connection)
        # Add any new plant types
        Load.add_new_plant_type(
            plant_types=[plant.get_plant_type() for plant in plants],
            connection=connection
        )
        # Add any new plants
        Load.add_new_plants(plants=plants, connection=connection)
