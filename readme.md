# Dex Sentinel TG Bot Project

This is a Python-based Telegram bot project for the **Dex Sentinel bot**.
The bot is set up using a virtual environment, and the main bot logic is contained in the `bot.py` file.

## Project Structure

```bash
$ tree -L 2     # list the project structure in 2 levels, might want to `sudo apt install tree` on linux
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── routes.py
├── bot
│   ├── __init__.py
│   ├── bot.py
│   └── settings.py
├── .env.example
├── LICENSE
├── readme.md
└── requirements.txt
├── server.py
├── utils.py
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Telegram Bot API token](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone <bot-url>
   cd dex-sentinel
   ```

2. **Setup environment**

    ```bash
    ./scripts/setup.sh
    ```

3. **Run the server**

    ```bash
    ./scripts/start.sh
    ```

## Files Overview

- **app/main.py:** It sets up the bot and creates the api server.
- **app/routes.py:** Contains the routes for the api server.
- **bot/bot.py:** The main script that contains the bot's logic and handlers.
- **bot/settings.py:** Configuration file for storing the bot's settings, like the API token.
- **requirements.txt:** Lists the Python packages required to run the bot.
- **server.py** Script for starting the api server.
- **util.py** Contains utility functions.

## Usage

Once the bot is running, it can be interacted with via Telegram. Make sure to configure the bot’s token and commands in settings.py.

## License

This project is licensed under the MIT License. See LICENSE for more details
