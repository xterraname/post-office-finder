# Telegram Post Office Bot

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytelegrambotapi)


## Overview

This project is a Telegram bot that helps users find the nearest post office based on their location (The service is available only for the territory of Uzbekistan!). The bot uses the following technologies and libraries:

- **TeleBot (pyTelegramBotAPI):** For handling Telegram API interactions.
- **Peewee ORM:** For managing an SQLite database to store user data.
- **NumPy:** For efficient numerical computations (calculating the nearest post office).
- **CSV & JSON:** For configuration and data storage.


## Requirements

- Python 3.6 or higher
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- [Peewee](http://docs.peewee-orm.com/)
- [NumPy](https://numpy.org/)

### Installing Dependencies

You can install the required packages using pip:

```bash
pip install -r pof-bot/requirements.txt
```

## Configuration

The project relies on a JSON configuration file (`config.json`) that holds your bot tokens for different run modes. An example configuration:

```json
{
  "bot": {
    "local": {
      "username": "YOUR_BOT_USERNAME",
      "token": "YOUR_LOCAL_BOT_TOKEN"
    },
    "dev": {
      "username": "YOUR_BOT_USERNAME",
      "token": "YOUR_DEV_BOT_TOKEN"
    }
  }
}
```

Make sure to replace `YOUR_LOCAL_BOT_TOKEN` and `YOUR_DEV_BOT_TOKEN` with your actual Telegram bot tokens.

## Database Initialization

The bot uses an SQLite database (`bot.db`) to store user information. The database and tables are automatically created if they do not exist.

- **Automatic Database Creation:**  
  SQLite creates the database file when connecting to it if it is missing.
  
- **Table Creation:**  
  The tables are created using Peewee’s `create_tables` method. You can also explicitly create or drop tables using:

  ```bash
  python -c "from models import create_tables; create_tables()"
  ```

## Usage

1. **Start the Bot:**

   Run the bot with the desired mode (local or dev):

   ```bash
   python bot.py --mode local
   ```

   or

   ```bash
   python bot.py --mode dev
   ```

2. **Interacting with the Bot:**

   - **Commands:**  
     Send `/start` or `/help` to receive a welcome message.
   
   - **Location Sharing:**  
     Share your location to get details of the nearest post office.
   
   - **Inline Buttons:**  
     Use the inline buttons provided to interact further, such as viewing the exact location on the map.

## Logging

- **Logs:**  
  All runtime logs are written to `logs.txt` with the log level set to `INFO` by default. This helps in monitoring the bot's activity and debugging issues.

## Error Handling

The project includes error handling mechanisms:
- **User Data Handling:**  
  The `send_welcome` function captures errors during user creation/retrieval.
- **Data Processing:**  
  The CSV data parsing in `nearest.py` handles potential conversion errors.
- **General Exceptions:**  
  Try-except blocks are used throughout the code to catch unexpected errors and log them accordingly.

## Contributing

Contributions are welcome! If you find a bug or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [TeleBot Documentation](https://pypi.org/project/pyTelegramBotAPI/)
- [Peewee ORM Documentation](http://docs.peewee-orm.com/)
- [NumPy Documentation](https://numpy.org/doc/)

---