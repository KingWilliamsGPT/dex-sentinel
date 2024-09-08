"""Contains classes for generating inline keyboards and handling their callback queries"""

from json import dumps, loads
from dexscreener import DexscreenerClient, TokenPair

from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import error, Update, InlineKeyboardMarkup, InlineKeyboardButton

from .utils import format_token
from storage import get_storage, get_logger, DatabaseTables

storage = get_storage()
logger = get_logger(__name__)



class KeyboardHandler:
    """Base class for handling keyboard callback queries
    All subclasses are expected to be used without instancing them."""
    pattern: str

    @classmethod
    async def generate_markup(cls, update: Update, context: CallbackContext) -> InlineKeyboardMarkup:
        """This function should generate the inline keyboard markup"""
        raise NotImplementedError    

    @classmethod
    def create_handler(cls) -> CallbackQueryHandler:
        """Creates a callback query handler"""
        handler = CallbackQueryHandler(cls.run, pattern = cls.pattern+':.+')
        return handler

    @classmethod
    def parse_data(cls, update: Update, context: CallbackContext) -> str:
        """This seperates the callback data (the page number) from the callback pattern"""
        # Returns None if no callback query is found, which means the keyboard markup doesn't exist
        if update.callback_query:
            data = update.callback_query.data.split(':')[-1]
        else:
            data = None
        return data
        

    @classmethod
    async def handle(cls, update: Update, context: CallbackContext):
        """This function handles the callback queries"""
        raise NotImplementedError


    @classmethod
    async def answer(cls, update: Update, context: CallbackContext) -> bool:
        """Returns boolean determining if handler answers a callback query"""
        if not update.effective_user:
            return False
        return True
    
    
    @classmethod
    async def run(cls, update: Update, context: CallbackContext):
        """This is the callback for the callback query handler"""
        if not await cls.answer(update, context):
            return
        try:
            await update.callback_query.answer()
        except error.BadRequest:
            # Callback query may be too old
            await update.effective_message.reply_text("Run the command again", reply_to_message_id = update.effective_message.id)
        else:
            await cls.handle(update, context)



class PaginationKeyboardHandler(KeyboardHandler):
    @classmethod
    async def generate_markup(cls, current: int, last: int,  update: Update, context: CallbackContext) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton("Previous", callback_data = f"{cls.pattern}:{current-1}"), ] if current!=1 else [],
            [InlineKeyboardButton("Next", callback_data = f"{cls.pattern}:{current+1}"), ] if current < last else [],
        ]

        markup = InlineKeyboardMarkup(keyboard)
        return markup
    
    @classmethod
    def parse_data(cls, update: Update, context: CallbackContext) -> str:
        data = KeyboardHandler.parse_data(update, context)
        try:
            data = int(data)
        except (ValueError, TypeError):
            data = None
        return data
    

    @classmethod
    async def get_data(cls, page: int, update: Update, context: CallbackContext):
        """Function which gets the data to be displayed by the keyboard"""
        raise NotImplementedError



class TokenPaginationKeyboard(PaginationKeyboardHandler):
    pattern = "token"
    client = DexscreenerClient()

    @classmethod
    async def get_data(cls, identifier: str, page: int, update: Update, context: CallbackContext) -> tuple[TokenPair, int]:
        tokens = await cls.client.search_pairs_async(identifier)
        if tokens:
            token = tokens[page-1]
        else:
            token = None
        return token, len(tokens)
                

    @classmethod
    async def handle(cls, update: Update, context: CallbackContext) -> None:
        page = cls.parse_data(update, context)
        new = not bool(page)
        page = page or 1
        user_data = storage.get_user_data(update.effective_user.id, DatabaseTables.USERS)
        
        # This happens if the server restarted and a user tries to interact with a previously generated keyboard
        if user_data["query_search"] is None:
            # Try to get the arguments from the replied to message
            message = update.effective_message.reply_to_message
            found = False
            if message:
                try:
                    query_search = " ".join(message.text.split(" ")[1:])
                    logger.info(f"{query_search}")
                    storage.set_user_data(update.effective_user.id, DatabaseTables.USERS, query_search = dumps(query_search))
                    user_data = storage.get_user_data(update.effective_user.id, DatabaseTables.USERS)
                    found = True
                except IndexError:
                    pass

            if not found:
                await update.effective_message.reply_text("Please search again")
                return

        # Load value in TEXT column from string
        identifier = loads(user_data["query_search"])
            
        token, last = await cls.get_data(identifier, page, update, context)
        if token:
            text = f"{page} of {last}\n\n" + format_token(token)
        
        else:
            text = f"Page {page} not found for {identifier}"
        
        markup = await cls.generate_markup(page, last, update, context)
        
        if new:
            await update.effective_message.reply_html(text, reply_to_message_id = update.effective_message.id, reply_markup = markup)
        else:
            await update.effective_message.edit_text(text, parse_mode = ParseMode.HTML, reply_markup = markup, disable_web_page_preview = False)



class TokenDetailsKeyboard(KeyboardHandler):
    pattern = "details"

    @classmethod
    async def generate_markup(cls, details: str, update: Update, context: CallbackContext) -> InlineKeyboardMarkup:
        details = "more" if details == "less" else "less"
        keyboard = [
            [InlineKeyboardButton(f"{details.title()} Details", callback_data = f"{cls.pattern}:{details}"), ],
        ]
        
        markup = InlineKeyboardMarkup(keyboard)
        return markup
        

    @classmethod
    async def handle(cls, update: Update, context: CallbackContext):
        details = cls.parse_data(update, context).lower()
        
        # TODO: Get the chain and address
        user_data = storage.get_user_data(update.effective_user.id, DatabaseTables.USERS)
        query_pair = user_data["query_pair"]
        
        # This happens if the server restarted and a user tries to interact with a previously generated keyboard
        if query_pair is None:
            # Try to get the arguments from the replied to message
            message = update.effective_message.reply_to_message
            found = False
            if message:
                try:
                    query_pair = " ".join(message.text.split(" ")[1:])
                    storage.set_user_data(update.effective_user.id, DatabaseTables.USERS, query_pair = dumps(query_pair))
                    user_data = storage.get_user_data(update.effective_user.id, DatabaseTables.USERS)
                    found = True
                except IndexError:
                    pass

            if not found:
                await update.effective_message.reply_text("Please search again")
                return
            
        chain, address = loads(query_pair).split(" ")
        token = await TokenPaginationKeyboard.client.get_token_pair_async(chain, address)
        text = format_token(token, details == "more")

        markup = await cls.generate_markup(details, update, context)
        await update.effective_message.edit_text(text, parse_mode = ParseMode.HTML, reply_markup = markup, disable_web_page_preview = False)

    
