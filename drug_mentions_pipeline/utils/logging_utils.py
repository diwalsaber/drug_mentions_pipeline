"""
Utility functions for logging setup.
"""
import logging
from drug_mentions_pipeline.config import LOG_LEVEL, LOG_FORMAT


def setup_logging():
    """Configure the root logger for the application."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler()  # Ceci envoie les logs vers stdout
        ]
    )
    return logging.getLogger("drug_mentions_pipeline")
