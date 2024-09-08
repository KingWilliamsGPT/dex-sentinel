# Dex Sentinel TG Bot Project

This is a Python-based Telegram bot project for the **Dex Sentinel bot**.
The bot is set up using a virtual environment, and the main bot logic is contained in the `bot.py` file.

## How to use the bot

The main feature of the bot is to retrieve and display real-time blockchain token pair information from decentralized exchanges (DEX) based on user queries in Telegram.

### Bot commands

- `/start:` Welcomes the user and provides instructions to use the bot.

- `/help:` Explains how to use the `/pair` and `/search` commands to get token information.

- `/about:` Provides information about the bot and its purpose.

- `/pair:` Fetches and returns token pair information from DEX based on the provided blockchain ID and token address. If no token is found, it informs the user.

```
/pair ethereum 0xAbc123456789
```

if found the bot response the below or `Token not found on ethereum at 0xAbc123456789

```yaml
Token Name: Example Token (EXM)
Pair: EXM/ETH
Current Price: $123.45
Liquidity: $1,000,000
Volume (24h): $500,000
```

- `/search:`: Searches for token pairs by blockchain ID, token address, or token name.

`/search <blockchain id|token address|token name>`

```
/search WBTC/USDC
```

Reponse

```yaml
Chain ID: ethereum
Dex ID: uniswap
Pair Address: 0x1234567890ABCDEF...

Chain ID: polygon
Dex ID: sushiswap
Pair Address: 0x9876543210FEDCBA...

```

## Project Structure

```bash
$ tree -L 2     # list the project structure in 2 levels, might want to `sudo apt install tree` on linux
.
├── bot
│   ├── __init__.py
│   └── bot.py
│   └── keyboards.py
│   └── utils.py
├── scripts
│   └── setup.sh
│   └── start.sh
├── .env.example
├── LICENSE
├── main.py
├── routes.py
├── readme.md
└── requirements.txt
├── server.py
├── settings.py
├── storage.py
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

- **bot/bot.py:** The main script that contains the bot's logic and handlers.
- **bot/settings.py:** Configuration file for storing the bot's settings, like the API token.
- **main.py:** It sets up the bot and creates the api server.
- **routes.py:** Contains the routes for the api server.
- **requirements.txt:** Lists the Python packages required to run the bot.
- **server.py** Script for starting the api server.
- **util.py** Contains utility functions.

## Usage

Once the bot is running, it can be interacted with via Telegram. Make sure to configure the bot’s token and commands in settings.py.

## License

This project is licensed under the MIT License. See LICENSE for more details
