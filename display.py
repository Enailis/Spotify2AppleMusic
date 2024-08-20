RED = "\033[31m"
GREEN = "\033[32m"
WHITE = "\033[37m"
LRED = "\033[91m"
LGREEN = "\033[92m"
DGREY = "\033[38;2;87;87;87m"
PURPLE = "\033[38;2;135;105;172m"
LBLUE = "\033[38;2;29;161;242m"

def colored_text(text, color):
    return color + text + WHITE