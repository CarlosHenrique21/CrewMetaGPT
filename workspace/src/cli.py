import argparse
from src.api_client import WeatherAPIClient
from src.utils import print_current_weather, print_forecast
from src.config import Config


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CLI Weather Forecast Tool: fetch current weather and forecast.",
        formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Current weather command
    parser_current = subparsers.add_parser('current', help='Show current weather')
    parser_current.add_argument('location', type=str, help='Location name or coordinates (lat,lon)')
    parser_current.add_argument('--units', type=str, choices=['metric', 'imperial'], default=Config.get_default_units(), help='Units for temperature (default: metric)')

    # Forecast command
    parser_forecast = subparsers.add_parser('forecast', help='Show weather forecast')
    parser_forecast.add_argument('location', type=str, help='Location name or coordinates (lat,lon)')
    parser_forecast.add_argument('--units', type=str, choices=['metric', 'imperial'], default=Config.get_default_units(), help='Units for temperature (default: metric)')
    parser_forecast.add_argument('--days', type=int, default=5, choices=range(1, 6), help='Number of forecast days (1-5)')

    # Help command (custom to list usage)
    subparsers.add_parser('help', help='Show help message')

    return parser.parse_args()


def parse_location(location_str):
    # Support either city name "London" or coordinates "lat,lon"
    if ',' in location_str:
        parts = location_str.split(',')
        if len(parts) != 2:
            raise ValueError("Invalid coordinates format. Use lat,lon")
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return {"lat": lat, "lon": lon}
        except ValueError:
            raise ValueError("Coordinates must be valid floats.")
    else:
        return location_str.strip()


def main():
    args = parse_arguments()

    if args.command == 'help':
        print_help()
        return

    client = WeatherAPIClient()

    try:
        location = parse_location(args.location)
    except ValueError as e:
        print(f"Error parsing location: {e}")
        return

    if args.command == 'current':
        try:
            weather = client.fetch_current_weather(location)
            print_current_weather(weather, units=args.units, location_name=args.location)
        except Exception as e:
            print(f"Error fetching current weather: {e}")
    elif args.command == 'forecast':
        try:
            forecast_days = client.fetch_forecast(location, days=args.days)
            print_forecast(forecast_days, units=args.units, location_name=args.location)
        except Exception as e:
            print(f"Error fetching forecast: {e}")


def print_help():
    help_text = """
CLI Weather Forecast Tool

Usage:
  weather current <location> [--units metric|imperial]
  weather forecast <location> [--units metric|imperial] [--days 1-5]
  weather help

Commands:
  current   Show current weather for the specified location (city name or lat,lon).
  forecast  Show 5-day forecast for the specified location.
  help      Show this help message.

Examples:
  weather current London
  weather current 48.85,2.35 --units imperial
  weather forecast New York --days 3
"""
    print(help_text)


if __name__ == '__main__':
    main()
