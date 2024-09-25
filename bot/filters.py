import re
from datetime import datetime
from dexscreener import TokenPair

from settings import get_logger, get_settings

settings = get_settings()
logger = get_logger(__name__)



class TokenFilter:
    @classmethod
    def filter(cls, text: str, tokens: list[TokenPair]) -> list[TokenPair]:
        filters = cls.parse_filters(text)
        if filters:
            filtered = filter(lambda token: cls.filter_token(token, filters), tokens)
        else:
            filtered = tokens

        return filtered

    @classmethod
    def filter_token(cls, token: TokenPair, filters: list[dict]) -> True:
        passed = True
        for i in filters:
            if not passed:
                break

            name = i["name"]
            match name:
                case "chain":
                    passed = cls.filter_by_chain(token, i)
                case "dex":
                    passed = cls.filter_by_dex(token, i)
        return passed

    @classmethod
    def parse_filters(cls, text: str) -> list[dict]:
        pattern = "(?P<name>(\w)+)(\s)*(?P<op>(=|<|>|<=|>=))(\s)*(?P<value>[^,]+)"
        last = 0
        filters = []

        while True:
            chunk = text[last:]
            matched = re.search(pattern, chunk)
            if not matched:
                break

            last = matched.span()[1] + 1
            parsed = {key.lower(): value for key, value in matched.groupdict().items()}
            filters.append(parsed)

        return filters


    # Place filter methods here

    @classmethod
    def filter_by_chain(cls, token: TokenPair, args: dict) -> bool:
        return token.chain_id == args["value"]

    @classmethod
    def filter_by_dex(cls, token: TokenPair, args: dict) -> bool:
        return token.dex_id == args["value"]

    @classmethod
    def filter_by_mcap(cls, token: TokenPair, args: dict) -> bool:
        return token.dex_id == args["value"]

    @classmethod
    def filter_by_time(cls, token: TokenPair, args: dict) -> bool:
        try:
            value = datetime(args["value"])
        except Exception as exception:
            return False

        # TODO: Finish the timestamp filter, add a reliable way to convert user input to datetime
        return False
