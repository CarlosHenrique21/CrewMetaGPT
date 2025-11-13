class WeatherCLIError(Exception):
    """Base class for all weather CLI errors."""
    pass


class InvalidInputError(WeatherCLIError):
    pass


class APIRequestError(WeatherCLIError):
    pass


class CacheError(WeatherCLIError):
    pass


class FavoriteError(WeatherCLIError):
    pass
