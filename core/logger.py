# core/logger.py
import logging

logger = logging.getLogger("DataTransformer")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # Console Handler for clean terminal output
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    
    # File Handler for deep debugging
    f_handler = logging.FileHandler("app.log", encoding="utf-8")
    f_handler.setLevel(logging.DEBUG)

    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)