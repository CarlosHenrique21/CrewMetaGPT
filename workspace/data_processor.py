from datetime import datetime
from errors import InvalidInputError


def format_current_weather(data):
    """
    Given raw API data for current weather, format it into a readable string.
    """
    try:
        location = f"{data['name']}, {data['sys']['country']}"
        weather = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        sunrise_ts = data['sys']['sunrise']
        sunset_ts = data['sys']['sunset']

        sunrise = datetime.fromtimestamp(sunrise_ts).strftime('%H:%M')
        sunset = datetime.fromtimestamp(sunset_ts).strftime('%H:%M')

        report = (
            f"Current weather for {location}\n"
            f"Condition: {weather}\n"
            f"Temperature: {temp}°\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}"
        )
        return report
    except (KeyError, IndexError) as e:
        raise InvalidInputError('Received malformed weather data') from e


def format_forecast(data):
    """
    Format forecast data for next several days into a readable string.

    OpenWeatherMap forecast gives 3-hour intervals; we will summarize by day.
    """
    try:
        city = data['city']['name']
        country = data['city']['country']
        list_data = data['list']

        from collections import defaultdict
        daily_summary = defaultdict(list)

        # Group data by date
        for entry in list_data:
            dt_txt = entry['dt_txt']  # '2024-06-10 12:00:00'
            date_str = dt_txt.split(' ')[0]
            daily_summary[date_str].append(entry)

        report_lines = [f'Weather forecast for {city}, {country}:']

        # Limit to first 3 days (or as many as provided)
        days = list(daily_summary.keys())[:3]

        for day in days:
            entries = daily_summary[day]
            temps = [e['main']['temp'] for e in entries]
            conditions = [e['weather'][0]['description'] for e in entries]
            humidities = [e['main']['humidity'] for e in entries]

            avg_temp = sum(temps) / len(temps)
            avg_humidity = sum(humidities) / len(humidities)
            # Most common condition
            from collections import Counter
            condition = Counter(conditions).most_common(1)[0][0].capitalize()

            report_lines.append(
                f"{day}: {condition}, Avg Temp: {avg_temp:.1f}°, Avg Humidity: {avg_humidity:.0f}%"
            )

        return '\n'.join(report_lines)

    except (KeyError, IndexError) as e:
        raise InvalidInputError('Received malformed forecast data') from e
