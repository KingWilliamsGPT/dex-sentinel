from dexscreener import TokenPair

from settings import get_settings, get_logger


settings = get_settings()
logger = get_logger(__name__)



def format_token(token: TokenPair) -> str:
    text_format = (
        "Chain ID: {token.chain_id}\n"
        "Dex ID: {token.dex_id}\n"
        "Pair Address: {token.pair_address}\n"
        "FDV: {token.fdv}\n\n"
        
        "USD Price: {token.price_usd}\n"
        "Native Price: {token.price_native}\n"
        f"Created: {token.pair_created_at.isoformat()}\n"
        
        "<b>Base Token</b>\n"
        "Symbol: {token.base_token.symbol}\n"
        "Name: {token.base_token.name}\n"
        "Address: {token.base_token.address}\n\n"
        
        "<b>Quote Token</b>\n"
        "Symbol: {token.quote_token.symbol}\n"
        "Name: {token.quote_token.name}\n"
        "Address: {token.quote_token.address}\n\n"
        
        "<b>Liquidity</b>\n"
        "Base: {token.liquidity.base}\n"
        "USD: {token.liquidity.usd}\n"
        "Quote: {token.liquidity.quote}\n\n"

        "<b>Transactions</b>\n"
        "5m: {token.transactions.m5.buys} bought, {token.transactions.m5.sells} sold\n"
        "1h: {token.transactions.h1.buys} bought, {token.transactions.h1.sells} sold\n"
        "6h: {token.transactions.h6.buys} bought, {token.transactions.h6.sells} sold\n"
        "24h: {token.transactions.h24.buys} bought, {token.transactions.h24.sells} sold\n\n"
        
        "<b>Volume</b>\n"
        "5m: {token.volume.m5}\n"
        "1h: {token.volume.h1}\n"
        "6h: {token.volume.h6}\n"
        "24h: {token.volume.h24}\n\n"

        "<b>Price Change</b>\n"
        "5m: {token.price_change.m5}\n"
        "1h: {token.price_change.h1}\n"
        "6h: {token.price_change.h6}\n"
        "24h: {token.price_change.h24}n\n"

        "URL: {token.url}"
    )

    text = text_format.format(token = token)
    return text