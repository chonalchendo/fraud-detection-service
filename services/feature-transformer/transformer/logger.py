import logging
import logging.handlers
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Custom theme for Rich
custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "critical": "bold white on red",
        "debug": "dim blue",  # Added debug level
        "success": "bold green",  # Added success level
    }
)

console = Console(
    color_system="256",
    width=150,
    theme=custom_theme,
    record=True,  # Enable logging history
)


@lru_cache
def get_logger(
    module_name: str,
    level: Union[int, str] = logging.INFO,
    log_file: Optional[str] = "logs/app.log",
    format_string: Optional[str] = None,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console_width: Optional[int] = None,
) -> logging.Logger:
    """Get a customized logger for the module.

    Args:
        module_name (str): Name of the module.
        level (Union[int, str]): Logging level. Can be string ('INFO') or int (logging.INFO).
        log_file (Optional[str]): If provided, also log to this file.
        format_string (Optional[str]): Custom format string for log messages.
        max_file_size (int): Maximum size in bytes before rotating log file.
        backup_count (int): Number of backup files to keep.
        console_width (Optional[int]): Override console width if needed.

    Returns:
        logging.Logger: Customized logger for the module.
    """
    # Convert string level to int if necessary
    if isinstance(level, str):
        level = getattr(logging, level.upper())

    logger = logging.getLogger(module_name)
    logger.setLevel(level)

    # Remove any existing handlers to avoid duplication
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Rich console handler with optional width override
    if console_width:
        console.width = console_width

    rich_handler = RichHandler(
        rich_tracebacks=True,
        console=console,
        tracebacks_show_locals=True,
        tracebacks_extra_lines=2,
        tracebacks_theme="monokai",
        show_time=True,
        show_path=True,
        enable_link_path=True,  # Enable clickable file paths
    )

    # Use custom format string if provided, else use default
    if not format_string:
        format_string = "%(asctime)s - %(name)s - [%(threadName)s:%(funcName)s:%(lineno)d] - %(levelname)s - %(message)s"

    rich_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(rich_handler)

    # Add rotating file handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        if not log_path.parent.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)

        # Use RotatingFileHandler instead of FileHandler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_file_size, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(format_string))
        logger.addHandler(file_handler)

    # Add custom success level
    logging.SUCCESS = 25  # Between INFO and WARNING
    logging.addLevelName(logging.SUCCESS, "SUCCESS")

    def success(self, message, *args, **kwargs):
        """Log 'msg % args' with severity 'SUCCESS'."""
        if self.isEnabledFor(logging.SUCCESS):
            self._log(logging.SUCCESS, message, args, **kwargs)

    logging.Logger.success = success

    return logger
