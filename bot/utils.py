from dexscreener import TokenPair

from settings import get_settings, get_logger


settings = get_settings()
logger = get_logger(__name__)



def format_token(token: TokenPair, detailed = False) -> str:
    """Returns information about a token pair as a string"""
    try:
        created = token.pair_created_at.strftime("%A, %B %d %Y %h:%M:%S %p")
    except:
        created = "Unknown"
    finally:
        chain = token.chain_id.title()
        dex = token.dex_id.title()

    text_format = (
        f"⛓ Chain ID:  {chain}\n"
        f"💱 DEX ID:  {dex}\n"
        + ("🔗 Token Pair:  {token.base_token.symbol}/{token.quote_token.symbol}\n\n" if not detailed else "") +
        "📍 Address:  {token.pair_address}\n\n"
        f"🗓️ Created:  {created}\n\n"

        "<b>Prices</b>\n"
        "FDV:  {token.fdv:,} USD\n"
        "USD Price:    {token.price_usd:.16f} USD\n"
        "Native Price: {token.price_native:.16f} {token.quote_token.symbol}\n\n"

    )

    if detailed:
        text_format += (
            "<b>Base Token</b>\n"
            "Name:    {token.base_token.name}\n"
            "Symbol:  {token.base_token.symbol}\n"
            "📍 Address: {token.base_token.address}\n\n"

            "<b>Quote Token</b>\n"
            "Name:    {token.quote_token.name}\n"
            "Symbol:  {token.quote_token.symbol}\n"
            "📍 Address: {token.quote_token.address}\n\n"

            "<b>Liquidity</b>\n"
            "USD:   {token.liquidity.usd:,}\n"
            "Base:  {token.liquidity.base:,}\n"
            "Quote: {token.liquidity.quote:,}\n\n"

            "<b>Transactions</b>\n"
            "5m:  {token.transactions.m5.buys:>8,} bought  {token.transactions.m5.sells:>8,} sold\n"
            "1h:  {token.transactions.h1.buys:>8,} bought  {token.transactions.h1.sells:>8,} sold\n"
            "6h:  {token.transactions.h6.buys:>8,} bought  {token.transactions.h6.sells:>8,} sold\n"
            "24h: {token.transactions.h24.buys:>8,} bought  {token.transactions.h24.sells:>8,} sold\n\n"

            "<b>Volume</b>\n"
            "5m:   {token.volume.m5}\n"
            "1h:   {token.volume.h1}\n"
            "6h:   {token.volume.h6}\n"
            "24h:  {token.volume.h24}\n\n"

            "<b>Price Change</b>\n"
            "5m:   {token.price_change.m5}\n"
             "1h:   {token.price_change.h1}\n"
            "6h:   {token.price_change.h6}\n"
            "24h:  {token.price_change.h24}\n\n"

        )

    text_format += "URL: {token.url}"
    text = text_format.format(token = token)
    return text
