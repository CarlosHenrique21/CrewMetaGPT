from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

UNIT_SYMBOLS = {
    "metric": "°C",
    "imperial": "°F"
}

WEATHER_CONDITION_COLORS = {
    "clear": "yellow",
    "clouds": "bright_white",
    "rain": "blue",
    "drizzle": "cyan",
    "thunderstorm": "magenta",
    "snow": "white",
    "mist": "grey66",
    "fog": "grey50"
}

def colorize_condition(condition):
    """Returns colored text for weather condition."""
    lower_condition = condition.lower()
    for key, color in WEATHER_CONDITION_COLORS.items():
        if key in lower_condition:
            return Text(condition, style=color)
    return Text(condition)  # Default no color

def print_current_weather(weather_data, units="metric", location_name=None):
    """Print formatted current weather."""
    unit_symbol = UNIT_SYMBOLS.get(units, "°C")

    console.print(f"[bold underline]Current Weather{(' in ' + location_name) if location_name else ''}[/bold underline]")

    table = Table(show_header=False, box=None)
    table.add_row("Temperature:", f"{weather_data.temperature:.1f}{unit_symbol}")
    table.add_row("Humidity:", f"{weather_data.humidity}%")
    table.add_row("Wind Speed:", f"{weather_data.wind_speed} m/s")
    cond_text = colorize_condition(weather_data.condition_description)
    table.add_row("Condition:", cond_text)

    if weather_data.sunrise_time:
        table.add_row("Sunrise:", weather_data.sunrise_time.strftime("%H:%M"))
    if weather_data.sunset_time:
        table.add_row("Sunset:", weather_data.sunset_time.strftime("%H:%M"))

    console.print(table)


def print_forecast(forecast_days, units="metric", location_name=None):
    """Print formatted forecast weather."""
    unit_symbol = UNIT_SYMBOLS.get(units, "°C")

    console.print(f"[bold underline]Forecast{(' for ' + location_name) if location_name else ''}[/bold underline]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date")
    table.add_column("Temp")
    table.add_column("Humidity")
    table.add_column("Wind (m/s)")
    table.add_column("Condition")

    for day in forecast_days:
        cond_text = colorize_condition(day.condition_description)
        table.add_row(
            day.date.strftime("%Y-%m-%d"),
            f"{day.temperature:.1f}{unit_symbol}",
            f"{day.humidity}%",
            f"{day.wind_speed:.1f}",
            cond_text
        )

    console.print(table)
