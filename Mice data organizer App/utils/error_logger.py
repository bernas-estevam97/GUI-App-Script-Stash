# utils/error_logger.py
import traceback

def format_exception(error):
    return f"Error: {str(error)}\n{traceback.format_exc()}"