import argparse
import logging
import sys

import telebot
from telebot.custom_filters import ChatFilter

import handlers
import admin_handlers
from config_handler import get_token, get_admin_ids



def configure_logging():
    """
    Configure logging settings for the application.
    Logs will be appended to 'logs.txt' and set to INFO level.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="logs.txt",
        filemode="a"
    )
    # Set telebot logger level to INFO as well
    telebot.logger.setLevel(logging.WARN)


def parse_arguments():
    """
    Parse command-line arguments for the application.
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Telegram Bot Runner")
    parser.add_argument(
        "-m",
        "--mode",
        default="local",
        choices=["local", "dev"],
        help="Run mode (local or dev)"
    )
    return parser.parse_args()


def register_handlers(bot: telebot.TeleBot):
    """
    Register message and callback query handlers to the bot.
    
    Args:
        bot (telebot.TeleBot): The bot instance to register handlers for.
    """
    # Register admins handlers
    bot.register_message_handler(
        admin_handlers.admin_command,
        chat_id=get_admin_ids(),
        commands=["admin"],
        pass_bot=True
    )
    # Register welcome message handler for /start and /help commands
    bot.register_message_handler(
        handlers.send_welcome,
        commands=["start", "help"],
        pass_bot=True
    )
    # Register location handler
    bot.register_message_handler(
        handlers.finder,
        content_types=["location"],
        pass_bot=True
    )
    # Register echo handler for all messages
    bot.register_message_handler(
        handlers.echo_all,
        func=lambda message: True,
        pass_bot=True
    )
    # Register callback query handler for back navigation
    bot.register_callback_query_handler(
        handlers.back_callback,
        func=lambda c: c.data.startswith(handlers.location_factory.prefix),
        pass_bot=True
    )


def main():
    # Configure logging early in the execution
    configure_logging()

    # Parse command-line arguments
    args = parse_arguments()

    # Retrieve the bot token based on the mode
    TOKEN = get_token(args.mode)
    if not TOKEN:
        logging.error("No token provided. Exiting...")
        sys.exit(1)

    # Create a new TeleBot instance with HTML parsing enabled
    bot = telebot.TeleBot(TOKEN, parse_mode="html")
    bot.add_custom_filter(ChatFilter())
    register_handlers(bot)

    try:
        # Log bot information before starting polling
        me = bot.get_me()
        logging.info("_"*32)
        logging.info("Bot is starting...")
        logging.info(f"Mode: {args.mode}")
        logging.info(f"Token: {TOKEN[:16]}**************")
        logging.info(f"Bot username: {me.username}")

        # Start the bot in infinity polling mode
        bot.infinity_polling()
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)


if __name__ == '__main__':
    main()
