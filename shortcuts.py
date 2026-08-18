from enum import Enum, IntFlag

class Key(Enum):
    BACK         = "b"
    QUIT         = "q"
    RECIPES      = "r"
    GENERATE     = "g"
    NEW          = "n"
    ADD_SERVINGS = "s"
    TAG_OPTIONS  = "t"
    ADD          = "a"
    REMOVE       = "x"
    INGREDIENTS  = "i"

INF = "\033[94mi\033[0m"
ERR = "\033[91m\u2718\033[0m"
OK  = "\033[92m\u2714\033[0m"

class ShowInfo(IntFlag):
    DISH_NAME   = (1 << 0)
    TAGS        = (1 << 1)
    SERVINGS    = (1 << 2)
    INGREDIENTS = (1 << 3)
    STEPS       = (1 << 4)
    FULL_INFO   = DISH_NAME | TAGS | SERVINGS | INGREDIENTS | STEPS
