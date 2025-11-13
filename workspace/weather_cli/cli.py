import argparse
from weather_service import WeatherService

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Weather CLI Tool")
    parser.add_argument("location", type=str, help="Location to fetch weather data for")
    
    args = parser.parse_args()
    service = WeatherService()
    
    # Fetch current weather
    weather_data = service.get_current_weather(args.location)
    print(weather_data)

if __name__ == "__main__":
    main()
