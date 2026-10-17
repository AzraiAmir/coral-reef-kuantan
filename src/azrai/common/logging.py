"""
Common logging helper for Azr.AI phase scripts.
"""
import logging
import sys


def phase_logger(phase_name: str) -> logging.Logger:
    logger = logging.getLogger(phase_name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_logger(name: str) -> logging.Logger:
    return phase_logger(name)