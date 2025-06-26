import os

import dotenv


class EnvironmentUtils:
    """Utility class for environment variable management.

    Provides methods to read environment variables, typically from a .env file,
    using the dotenv package. This class is intended to centralize environment
    configuration access for the application.
    """

    @staticmethod
    def read_env_var(key: str) -> str:
        dotenv.load_dotenv(dotenv.find_dotenv('.env'))
        return os.getenv(key)
