import pytest
from unittest.mock import patch, MagicMock
from weather import fetch_weather, parse_weather, display_weather

MOCK_API_RESPONSE = {
    "name": "Sao Paulo",
    "sys": {"country": "BR"},
    "main": {"temp": 28.4, "feels_like": 26.1, "humidity": 65},
    "weather": [{"description": "céu limpo"}],
    "wind": {"speed": 3.5},
}


@patch("weather.requests.get")
def test_fetch_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_API_RESPONSE
    mock_get.return_value = mock_response

    result = fetch_weather("Sao Paulo")
    assert result["name"] == "Sao Paulo"


@patch("weather.requests.get")
def test_fetch_weather_city_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="not found"):
        fetch_weather("CidadeInexistente")


@patch("weather.requests.get")
def test_fetch_weather_invalid_api_key(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    with pytest.raises(EnvironmentError, match="Invalid API key"):
        fetch_weather("London")


def test_parse_weather():
    result = parse_weather(MOCK_API_RESPONSE)
    assert result["city"] == "Sao Paulo"
    assert result["country"] == "BR"
    assert result["temp"] == 28
    assert result["feels_like"] == 26
    assert result["humidity"] == 65
    assert result["wind_speed"] == 13  # 3.5 * 3.6 = 12.6 → 13


def test_parse_weather_description_capitalized():
    result = parse_weather(MOCK_API_RESPONSE)
    assert result["description"][0].isupper()


def test_display_weather(capsys):
    weather = {
        "city": "Sao Paulo",
        "country": "BR",
        "temp": 28,
        "feels_like": 26,
        "description": "Ceu limpo",
        "humidity": 65,
        "wind_speed": 13,
    }
    display_weather(weather)
    captured = capsys.readouterr()
    assert "Sao Paulo" in captured.out
    assert "28°C" in captured.out
    assert "65%" in captured.out
