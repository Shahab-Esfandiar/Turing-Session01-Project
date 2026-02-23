# core/exceptions.py

class DataTransformerError(Exception):
    """Base exception for the application."""
    pass

class LLMServiceError(DataTransformerError):
    """Raised when AI model prediction fails."""
    pass

class TableStructureError(DataTransformerError):
    """Raised when the table format is unreadable."""
    pass