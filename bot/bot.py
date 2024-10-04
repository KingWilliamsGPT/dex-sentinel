from json import dumps
from traceback import format_exception
from html import escape as html_escape

from telegram.constants import ParseMode
from telegram import BotCommand, Update
from telegram.ext import filters, Application, CommandHandler, MessageHandler, ContextTypes, CallbackContext

from .utils import format_token
from settings import get_settings, get_logger
from storage import get_storage, DatabaseTables
from .keyboards import TokenPaginationKeyboard, TokenDetailsKeyboard


storage = get_storage()
settings = get_settings()
logger = get_logger(__name__)




class BotContext(CallbackContext):
    @classmethod
    def from_update(cls, update: object, application: "Application") -> "BotContext":
        if isinstance(update, Update):
            return cls(application = application)
        return super().from_update(update, application)



async def log_in_channels(text: str, context: BotContext):
    for chat_id in settings.LOG_CHAT_IDS:
        await context.bot.send_message(chat_id = chat_id, text = text, parse_mode = ParseMode.HTML)


async def send_to_developers(text: str, context: BotContext):
    for chat_id in settings.DEVELOPER_CHAT_IDS:
        await context.bot.send_message(chat_id = chat_id, text = text, parse_mode = ParseMode.HTML)


class Bot:
    def __init__(self, bot_token: str) -> None:
        """Set up bot application and a web application for handling the incoming requests."""

        # Set updater to None so updates are handled by webhook
        context_types = ContextTypes(context = BotContext)
        self.application = Application.builder().token(bot_token).updater(None).context_types(context_types).build()


    async def setup(self, secret_token: str, bot_web_url: str) -> None:
        # Set webhook url and secret_key
        await self.application.bot.set_webhook(url = bot_web_url, secret_token = secret_token)
        await self.set_bot_commands_menu()

        # Add handlers here
        self.application.add_error_handler(self.handle_error)

        self.application.add_handler( CommandHandler("start", self.cmd_start) )
        self.application.add_handler( CommandHandler("help", self.cmd_help) )
        self.application.add_handler( CommandHandler("about", self.cmd_about) )
        self.application.add_handler( CommandHandler("pair", self.cmd_pair) )
        self.application.add_handler( CommandHandler("search", self.cmd_search) )

        self.application.add_handler(TokenDetailsKeyboard.create_handler())
        self.application.add_handler(TokenPaginationKeyboard.create_handler())
        self.application.add_handler( MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message) )


    # Bot methods

    async def set_bot_commands_menu(self) -> None:
        # Register commands for bot menu
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Get help about this bot"),
            BotCommand("about", "Get information about the bot"),

            BotCommand("pair", "Get token pair matching the specified blockchain and address"),
            BotCommand("search", "Get token pairs matching the specified address or name"),
        ]
        await self.application.bot.set_my_commands(commands)


    # Bot handlers

    async def handle_error(self, update: Update, context: BotContext) -> None:
        """Log the error and send a message to notify the developer."""
        # Log the error first so it can be seen even if something breaks.
        logger.error("Exception while handling an update:", exc_info = context.error)

        # traceback.format_exception returns the usual python message about an exception, but as a
        # list of strings rather than a single string, so we have to join them together.
        tb_list = format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)

        # Build the message with some markup and additional information about what happened.

        update_str = dumps(update.to_dict() if isinstance(update, Update) else str(update), indent = 2, ensure_ascii = False)
        for text in (
            f"An exception was raised while handling an update\n"
            f"<pre>update = {html_escape(update_str)}</pre>\n",

            "<b>Context</b>\n"
            f"<pre><u>context.bot_data</u> = {html_escape(dumps(context.bot_data, indent = 2, ensure_ascii = False))}</pre>\n\n"
            f"<pre><u>context.chat_data</u> = {html_escape(dumps(context.chat_data, indent = 2, ensure_ascii = False))}</pre>\n\n"
            f"<pre><u>context.user_data</u> = {html_escape(dumps(context.user_data, indent = 2, ensure_ascii = False))}</pre>\n\n",

            "<b>Traceback</b>\n"
            f"<pre>{html_escape(tb_string)}</pre>\n",
        ):
            await log_in_channels(text, context)


    async def handle_message(self, update: Update, context: BotContext) -> None:
        """Handles messages"""
        if not update.effective_message:
            return
        text = "Use /help to get a list of commands"
        await update.effective_message.reply_text(text, reply_to_message_id = update.effective_message.message_id)


    # Bot commands
    async def cmd_start(self, update: Update, context: BotContext):
        text = (
            f"Welcome, {update.effective_user.first_name} !\n"
            "I am a bot designed to help you easily access and analyze blockchain token data\n\n"
            "With me, you can:\n"
            "- Retrieve token pair details using the /pair command\n"
            "- Search for token pairs by blockchain, address, or name with the /search command\n"
            "- Apply filters to refine your results by specific chains or DEXs using the /filter option\n\n"
            "To begin, simply enter /pair or /search followed by the relevant details, I will provide the information you need\n"
            "For further guidance, type /help. I'm here to assist you in navigating the world of cryptocurrency tokens with ease."
            )
        await update.effective_message.reply_text(text)


    async def cmd_help(self, update: Update, context: BotContext):
        text = (
            "Commands\n\n"

            "1. /pair\nGet token pair info for a specific blockchain\n\n"
            "Usage: /pair <blockchain id> <token address>\n\n"
            "Example: /pair ethereum 0xAbc123456789\n\n\n"

            "2. /search\nFind token pairs by address or name\n\n"
            "Usage: /search <blockchain id|token address|token name>\n\n"
            "Examples:\n\n"
            "/search 0xAbc123456789\n"
            "/search WBTC/USDC\n"
            "/search WBTC\n\n\n"

            "3. Filters\nApply filters to refine search results\n\n"
            "Usage: /search <blockchain id|token address|token name> /filters [chain=chain id,] [dex=dex id,]\n\n"
            "Examples:\n"
            "/search 0xAbc123456789 /filter chain=ton\n"
            "/search WBTC/USDC /filter dex=stonfi\n"
            "/search WBTC /filter chain=ton,dex=stonf\n\n\n"
        )
        await update.effective_message.reply_text(text, reply_to_message_id = update.effective_message.id)


    async def cmd_about(self, update: Update, context: BotContext):
        """Handles """
        text = (
            f"Hi, I'm {context.bot.first_name}\n"

            "Copyright 2024 Samurai Coder\n"
            "This bot is licensed under the <a href='https://opensource.org/license/mit' title='MIT License'>MIT</a>\n"
            "Source code: <a href='https://github.com/KingWilliamsGPT/dex-sentinel/' title='Github repository'>https://github.com/KingWilliamsGPT/dex-sentinel</a>"
        )
        await update.effective_message.reply_html(text, reply_to_message_id = update.effective_message.id)


    async def cmd_pair(self, update: Update, context: BotContext):
        """Handles the pair command"""
        if len(context.args) != 2: return
        chain, address = context.args

        token = await TokenPaginationKeyboard.client.get_token_pair_async(chain, address)

        if token:
            text = format_token(token)
            keyboard = await TokenDetailsKeyboard.generate_markup("less", update, context)
            await update.effective_message.reply_html(text, reply_to_message_id = update.effective_message.id, reply_markup = keyboard)
            # Have to enclose values in quotes for TEXT column in sqlite3
            storage.set_user_data(update.effective_user.id, DatabaseTables.USERS, query_pair = dumps(f"{chain} {address}"))

        else:
            text = f"Token not found on {chain} at {address}"
            await update.effective_message.reply_text(text, reply_to_message_id = update.effective_message.id)


    async def cmd_search(self, update: Update, context: BotContext):
        """Handles the search command"""
        # Returns if argument length is not 1 and `/filter` was not found in text
        if len(context.args) != 1 and context.args.count('/filter') != 1: return
        identifier = " ".join(context.args)

        # Have to enclose values in quotes for TEXT column in sqlite3
        storage.set_user_data(update.effective_user.id, DatabaseTables.USERS, query_search = dumps(identifier))
        await TokenPaginationKeyboard.handle(update, context)

