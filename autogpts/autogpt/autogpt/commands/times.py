from datetime import datetime

def get_current_datetime() -> str:
    """Return the current date and time as a formatted string.

    Returns:
        str: The current date and time in the format "YYYY-MM-DD HH:MM:SS".
    """
    return f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
