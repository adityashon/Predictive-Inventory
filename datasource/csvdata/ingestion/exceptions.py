# custom error handlings


class IngestionError(Exception):
    """Base exception for ingestion errors."""


class FileIngestionError(IngestionError):
    """Raised when the input file cannot be processed."""


class SchemaError(IngestionError):
    """Raised when the input schema is invalid."""


class RecordValidationError(IngestionError):
    """Raised when an individual record is invalid."""