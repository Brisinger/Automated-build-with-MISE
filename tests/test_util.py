"""Unit tests for utilities.util module."""

import pytest
from utilities.util import (
    TemperatureFormatNotSupported,
    _to_float_temperature,
    convert_farenheit_to_celsius,
    convert_celsius_to_farenheit,
)


@pytest.mark.parametrize(
    "temperature, expected",
    [
        (100, 100.0),
        (36.6, 36.6),
        ("  12.5 ", 12.5),
    ],
)
def test_to_float_valid_inputs(temperature, expected):
    """Test _to_float_temperature with valid inputs (parameterized).
    
    Args:
        temperature: Input temperature value (int, float, or numeric string).
        expected: Expected float output temperature.
    """
    assert _to_float_temperature(temperature) == expected


def test_to_float_invalid_empty_string():
    """Test _to_float_temperature with an empty string."""

    with pytest.raises(TemperatureFormatNotSupported) as exc:
        _to_float_temperature("")
    assert "Empty string" in str(exc.value)


def test_to_float_invalid_string():
    """Test _to_float_temperature with a non-numeric string."""

    with pytest.raises(TemperatureFormatNotSupported) as exc:
        _to_float_temperature("abc")
    assert "is not a valid temperature" in str(exc.value)


@pytest.mark.parametrize(
    "temperature, expected",
    [
        (32, 0.0),
        (212, 100.0),
        ("212", 100.0),
    ],
)
def test_convert_fahrenheit_to_celsius(temperature, expected):
    """Test convert_farenheit_to_celsius with valid inputs.
    
    Args:
        temperature: Input temperature in Fahrenheit (int, float, or numeric string).
        expected: Expected float output temperature in Celsius.
    """

    assert convert_farenheit_to_celsius(temperature) == pytest.approx(expected)


@pytest.mark.parametrize(
    "temperature, expected",
    [
        (0, 32.0),
        (100, 212.0),
        ("100", 212.0),
    ],
)
def test_convert_celsius_to_fahrenheit(temperature, expected):
    """Test convert_celsius_to_farenheit with valid inputs.
    
    Args:
        temperature: Input temperature in Celsius (int, float, or numeric string).
        expected: Expected float output temperature in Fahrenheit.
    """

    assert convert_celsius_to_farenheit(temperature) == pytest.approx(expected)


@pytest.mark.parametrize(
    "temperature",
    [[], {}, None, object()],
)
def test_convert_invalid_inputs_raise(temperature):
    """Test conversion functions with invalid inputs.
    
    Args:
        temperature: Invalid input temperature types (list, dict, None, object).
    
    Raises:
        TemperatureFormatNotSupported: For each invalid input type.
    """

    for fn in (convert_farenheit_to_celsius, convert_celsius_to_farenheit):
        with pytest.raises(TemperatureFormatNotSupported):
            fn(temperature)
