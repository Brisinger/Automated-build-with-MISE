"""
  Utility functions for temperature conversion.
  This module provides functions to convert temperatures between Fahrenheit and Celsius.
"""


class TemperatureFormatNotSupported(Exception):
    """Raised when the provided argument is not a supported format for temperature conversion.
    
    This exception is used to indicate that the input argument 
    cannot be interpreted as a valid temperature."""

def _to_float_temperature(value) -> float:
    """Validate and convert the input to a float temperature. 
    Accepts int, float, and numeric strings; raises TemperatureFormatNotSupported otherwise.

    Args:
        value (int|float|str): The input temperature value.
            Can be an int, float, or a numeric string.

    Returns:
        float: The temperature as a float.

    Examples:
        >>> _to_float_temperature(100)
        100.0
        >>> _to_float_temperature("36.6")
        36.6
        >>> _to_float_temperature("abc")
        Traceback (most recent call last):
            ...
        TemperatureFormatNotSupported: String 'abc' is not a valid temperature
        >>> _to_float_temperature([])
        Traceback (most recent call last):
            ...
        TemperatureFormatNotSupported: Type 'list' is not a valid temperature

    Raises:
        TemperatureFormatNotSupported: If the argument cannot be parsed as a
            numeric temperature.
        
    Note: This is an internal helper function and should not be used directly.
    """
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        if stripped == "":
            raise TemperatureFormatNotSupported("Empty string is not a valid temperature")
        try:
            return float(stripped)
        except ValueError as exc:
            raise TemperatureFormatNotSupported(
                f"String {stripped!r} is not a valid temperature"
            ) from exc
    raise TemperatureFormatNotSupported(f"Type '{type(value).__name__}' is not a valid temperature")

def convert_farenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius.

    Args:
        fahrenheit (int|float|str): Temperature in Fahrenheit.
            Can be an int/float or a numeric string.

    Returns:
        float: Temperature in Celsius.

    Examples:
        >>> convert_farenheit_to_celsius(32)
        0.0
        >>> convert_farenheit_to_celsius("212")
        100.0
        >>> convert_farenheit_to_celsius("abc")
        Traceback (most recent call last):
            ...
        TemperatureFormatNotSupported: String 'abc' is not a valid temperature
        >>> convert_farenheit_to_celsius([])
        Traceback (most recent call last):
            ...
        TemperatureFormatNotSupported: Type 'list' is not a valid temperature

    Raises:
        TemperatureFormatNotSupported: If the argument cannot be parsed as a
            numeric temperature.

    Note: Formula: (F - 32) * 5/9
    """
    fahrenheit_val = _to_float_temperature(fahrenheit)
    return (fahrenheit_val - 32) * 5.0 / 9.0

def convert_celsius_to_farenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit.

    Args:
        celsius (int|float|str): Temperature in Celsius.
            Can be an int/float or a numeric string.

    Returns:
        float: Temperature in Fahrenheit.

    Examples:
        >>> convert_celsius_to_farenheit(0)
        32.0
        >>> convert_celsius_to_farenheit("100")
        212.0
        >>> convert_celsius_to_farenheit("abc")
        Traceback (most recent call last):
            ...
        TemperatureFormatNotSupported: String 'abc' is not a valid temperature
        >>> convert_celsius_to_farenheit([])
        Traceback (most recent call last):
            ...
        TemperatureFormatNotSupported: Type 'list' is not a valid temperature

    Raises:
        TemperatureFormatNotSupported: If the argument cannot be parsed as a
            numeric temperature.

    Note: Formula: (C * 9/5) + 32
    """
    celsius_val = _to_float_temperature(celsius)
    return (celsius_val * 9.0 / 5.0) + 32


if __name__ == "__main__":  # pragma: no cover
    # To run the module directly, use: python utilities/util.py
    # This will print: 100 Celsius is 212.0 Farenheit.
    print("100 Celsius is", convert_celsius_to_farenheit(100), "Farenheit.")
