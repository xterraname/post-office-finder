import json
import os

def load_config(config_path: str) -> dict:
    """
    Load configuration from a JSON file.

    Args:
        config_path (str): The path to the configuration JSON file.

    Returns:
        dict: The configuration data.
    """
    with open(config_path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)


# Get the absolute path to the directory where this file is located
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Build the full path to the config.json file
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
# Load configuration data from the file
CONFIG = load_config(CONFIG_PATH)


def get_token(mode: str = "local") -> str:
    """
    Retrieve the bot token based on the specified mode.

    Args:
        mode (str): The mode to use ('local' or 'dev'). Defaults to "local".

    Returns:
        str: The bot token.

    Raises:
        KeyError: If the token is not found for the specified mode.
    """
    try:
        return CONFIG['bot'][mode]['token']
    except KeyError as e:
        raise KeyError(f"Token for mode '{mode}' not found in the configuration.") from e
