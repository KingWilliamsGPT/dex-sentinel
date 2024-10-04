"""Main code entry point"""

from telegram import Update
from contextlib import asynccontextmanager
from fastapi import Depends, Header, HTTPException, FastAPI, Request


from bot import Bot
from routes import router
from settings import get_settings, get_logger


settings = get_settings()
logger = get_logger(__name__)


# Checks if the secret token included in the headers is matched the one specified
def auth_bot_token(x_telegram_bot_api_secret_token: str = Header(None)) -> str:
    if x_telegram_bot_api_secret_token != settings.SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return x_telegram_bot_api_secret_token


# The liespan of the fastapi app
@asynccontextmanager
async def lifespan(app: FastAPI):
    bot = Bot(settings.BOT_TOKEN)
    await bot.setup(settings.SECRET_TOKEN, settings.BOT_WEB_URL+settings.WEBHOOK_URL )


    # The webhook path handler
    @router.post(settings.WEBHOOK_URL, status_code=204)
    async def webhook(request: Request, token: str = Depends(auth_bot_token)) -> None:
        """Handle incoming updates by putting them into the `update_queue`"""
        update_json = await request.json()
        update = Update.de_json( update_json, bot.application.bot )
        await bot.application.update_queue.put(update)


    app.include_router(router)
    async with bot.application:
        # Runs when app starts
        logger.info(f"\n🚀 Bot starting up ...\nDebugging is {'enabled' if settings.DEBUG else 'disabled'}")
        await bot.application.start()

        yield

        # Runs after app shuts down
        logger.info("\n⛔ Bot shutting down ...\n")
        await bot.application.stop()



app = FastAPI( title = "BotFastAPI", description = "A webhook api for a telegram DexScreener bot", lifespan = lifespan )
