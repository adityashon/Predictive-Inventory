from datasource.csvdata.ingestion.csv_source import AcceptedRecord


'''
SKU doesn't exist
future order date
duplicate order
negative revenue
currency missing
impossible quantity
'''


class BusinessValidationError(Exception):
    """Raised when a business rule is violated."""


def validate_sales_record(
    record: AcceptedRecord,
) -> None:

    if record.quantity <= 0:
        raise BusinessValidationError(
            "Quantity must be greater than zero."
        )

    if (
        record.unit_price is not None
        and record.unit_price < 0
    ):
        raise BusinessValidationError(
            "Unit price cannot be negative."
        )