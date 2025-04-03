import pytest
from unittest.mock import MagicMock, patch
from load import DatabaseManager
from models import Plant


@pytest.fixture
def mock_plants():
    mock_plant = MagicMock(spec=Plant)
    mock_plant.get_location.return_value.get_continent_values.return_value = (
        "Africa",)
    mock_plant.get_location.return_value.get_country_values.return_value = (
        "Kenya", "Nairobi", "Africa")
    mock_plant.get_location.return_value.get_city_values.return_value = (
        "Nairobi", 1.0, 36.0, "Kenya")
    mock_plant.get_botanist.return_value.get_values.return_value = (
        "John Doe", "john@example.com", "123-456-7890")
    mock_plant.get_plant_type.return_value.get_values.return_value = (
        "Fern", "Pteridophyta", "url")
    mock_plant.get_values.return_value = (
        1, "Fern", "John Doe", "Nairobi", "2025-03-01")
    mock_plant.get_record_values.return_value = (
        1, 20.5, 30.2, "2025-03-01T12:00:00")
    return [mock_plant] * 5


@patch("load.pymssql.connect")
def test_load_all(mock_connect, mock_plants):
    mock_connection = mock_connect.return_value
    mock_cursor = mock_connection.cursor.return_value
    db_manager = DatabaseManager(mock_plants)

    db_manager.load_all()

    assert mock_cursor.executemany.call_count == 7
    # Expecting one commit after all operations
    assert mock_cursor.commit.call_count == 1

    expected_calls = [
        (db_manager.BOTANIST_UPSERT, [
         plant.get_botanist().get_values() for plant in mock_plants]),
        (db_manager.CONTINENT_UPSERT, [
         plant.get_location().get_continent_values() for plant in mock_plants]),
        (db_manager.COUNTRY_UPSERT, [
         plant.get_location().get_country_values() for plant in mock_plants]),
        (db_manager.CITY_UPSERT, [
         plant.get_location().get_city_values() for plant in mock_plants]),
        (db_manager.PLANT_TYPE_UPSERT, [
         plant.get_plant_type().get_values() for plant in mock_plants]),
        (db_manager.PLANT_UPSERT, [plant.get_values()
         for plant in mock_plants]),
        (db_manager.RECORDING_INSERT, [
         plant.get_record_values() for plant in mock_plants]),
    ]

    for query, values in expected_calls:
        mock_cursor.executemany.assert_any_call(query, values)

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()
