import sys
import click
from config import Config
from api_client import get_current_weather, get_forecast
from data_processor import format_current_weather, format_forecast
from cache_manager import CacheManager
from favorites_manager import FavoritesManager
from errors import WeatherCLIError


@click.group()
def cli():
    """CLI Weather Forecast Tool"""
    pass


@cli.command()
@click.argument('location', required=True)
@click.option('--unit', default=None, help='Temperature unit: celsius or fahrenheit')
def current(location, unit):
    """Get current weather for a location"""
    config = Config()
    cache = CacheManager()
    favorites = FavoritesManager()

    unit = unit or config.default_unit

    # Check if location is favorite shortcut
    location_str = favorites.get_location_by_name(location) or location

    # Check cache first
    try:
        cached = cache.get_cached(location_str, unit)
        if cached:
            click.echo('Using cached data:')
            click.echo(format_current_weather(cached))
            return
    except Exception:
        pass  # Ignore cache errors silently

    # Fetch current weather
    try:
        data = get_current_weather(location_str, unit)
        cache.set_cache(location_str, unit, data)
        click.echo(format_current_weather(data))
    except WeatherCLIError as e:
        click.echo(f'Error: {e}', err=True)
        sys.exit(1)


@cli.command()
@click.argument('location', required=True)
@click.option('--days', default=3, show_default=True, help='Number of forecast days')
@click.option('--unit', default=None, help='Temperature unit: celsius or fahrenheit')
def forecast(location, days, unit):
    """Get weather forecast for a location"""
    config = Config()
    cache = CacheManager()
    favorites = FavoritesManager()

    unit = unit or config.default_unit
    location_str = favorites.get_location_by_name(location) or location

    # Check cache first
    try:
        cached = cache.get_cached_forecast(location_str, unit, days)
        if cached:
            click.echo('Using cached data:')
            click.echo(format_forecast(cached))
            return
    except Exception:
        pass  # Ignore cache errors silently

    try:
        data = get_forecast(location_str, days, unit)
        cache.set_cache_forecast(location_str, unit, days, data)
        click.echo(format_forecast(data))
    except WeatherCLIError as e:
        click.echo(f'Error: {e}', err=True)
        sys.exit(1)


@cli.group()
def favorites():
    """Manage favorite locations"""
    pass


@favorites.command('list')
def list_favorites():
    """List favorite locations"""
    favorites = FavoritesManager()
    favs = favorites.list_favorites()
    if not favs:
        click.echo('No favorite locations saved.')
        return
    for fav in favs:
        click.echo(f'{fav["name"]}: {fav["location"]}')


@favorites.command('add')
@click.argument('name', required=True)
@click.argument('location', required=True)
def add_favorite(name, location):
    """Add a new favorite location"""
    favorites = FavoritesManager()
    try:
        favorites.add_favorite(name, location)
        click.echo(f'Added favorite: {name} -> {location}')
    except WeatherCLIError as e:
        click.echo(f'Error: {e}', err=True)
        sys.exit(1)


@favorites.command('remove')
@click.argument('name', required=True)
def remove_favorite(name):
    """Remove a favorite location by name"""
    favorites = FavoritesManager()
    try:
        favorites.remove_favorite(name)
        click.echo(f'Removed favorite: {name}')
    except WeatherCLIError as e:
        click.echo(f'Error: {e}', err=True)
        sys.exit(1)


@cli.command()
def help():
    click.echo(cli.get_help(click.Context(cli)))


if __name__ == '__main__':
    cli()
