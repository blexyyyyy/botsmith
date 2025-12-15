from functools import lru_cache
from botsmith.app import BotSmithApp

@lru_cache()
def get_botsmith_app() -> BotSmithApp:
    """
    Returns a singleton instance of BotSmithApp.
    """
    return BotSmithApp()
