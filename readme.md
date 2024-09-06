# Dex Sentinel TG Bot Project

This is a Python-based Telegram bot project for the **Dex Sentinel bot**.
The bot is set up using a virtual environment, and the main bot logic is contained in the `bot.py` file.

## Project Structure
```bash
$ tree -L 2     # list the project structure in 2 levels, might want to `sudo apt install tree` on linux
.
├── bot
│   ├── bot.py
│   ├── __init__.py
│   ├── __pycache__
│   └── settings.py
├── env
│   ├── bin
│   ├── include
│   ├── lib
│   ├── lib64 -> lib
│   ├── pyvenv.cfg
│   └── share
├── LICENSE
├── main.py
├── readme.md
└── requirements.txt
```


## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Telegram Bot API token](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <bot-url>
   cd telegram-bot
   ```

2. **Setup Virtual environment**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```


3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the bot**
    ```bash
    python3 main.py
    ```

## Files Overview

- **bot/bot.py:** The main script that contains the bot's logic and handlers.
- **settings.py:** Configuration file for storing your bot's settings, like the API token.
- **requirements.txt:** Lists the Python packages required to run the bot.
- **env/:** The virtual environment directory (generated after setup).


## Usage

Once the bot is running, it can be interacted with via Telegram. Make sure to configure the bot’s token and commands in settings.py.

## License

This project is licensed under the MIT License. See LICENSE for more details.