class TiqetsProcessorError(Exception):
    """Base exception for Tiqets Processor."""
    pass


class DataValidationError(TiqetsProcessorError):
    """Raised when data validation fails."""
    pass


class DataProcessingError(TiqetsProcessorError):
    """Raised when data processing fails."""
    pass


class DatabaseError(TiqetsProcessorError):
    """Raised when database operations fail."""
    pass


class FileOperationError(TiqetsProcessorError):
    """Raised when file operations fail."""
    pass
