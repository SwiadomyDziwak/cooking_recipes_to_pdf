from enum import Enum

class Key(Enum):
    BACK         = "b"
    QUIT         = "q"
    RECIPES      = "r"
    GENERATE     = "g"
    NEW_RECIPE   = "n"
    ADD_SERVINGS = "s"
    TAG_OPTIONS  = "t"
    ADD_TAG      = "a"
    REMOVE_TAG   = "r"

INF = "\033[94mi\033[0m"
ERR = "\033[91m\u2718\033[0m"
OK  = "\033[92m\u2714\033[0m"
