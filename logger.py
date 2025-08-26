from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

LEVEL_COLORS = {
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'DEBUG': Fore.CYAN,
}

def log(module: str, level: str, message: str) -> None:
    """打印带有颜色和统一格式的日志信息。"""
    level = level.upper()
    color = LEVEL_COLORS.get(level, Fore.WHITE)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{color}[{timestamp}] [{level}] [{module}] {message}{Style.RESET_ALL}")
