from datasource.csvdata.ingestion.csv_source import CsvDataSource
from datasource.csvdata.ingestion.models import RejectedRecords
from datasource.csvdata.ingestion.validator import (
    BusinessValidationError,
    validate_sales_record,
)

#  temporary test on based on given csv
def main():

    source = CsvDataSource(
        r"datasource\csvdata\data\row\sales.csv"
    )

    results = source.fetch_data()

    accepted = 0
    rejected = 0

    for result in results:

        # -----------------------------------------
        # CSV / schema validation already failed
        # -----------------------------------------
        if isinstance(result, RejectedRecords):

            rejected += 1

            print("\n❌ REJECTED")
            print("Row:", result.number_row)
            print("Reason:", result.reason)
            print("Raw data:", result.raw_data)

            continue

        # -----------------------------------------
        # Business validation
        # -----------------------------------------
        try:

            validate_sales_record(result)

            accepted += 1

            print("\n✅ ACCEPTED")
            print("Order:", result.order_id)
            print("SKU:", result.sku)
            print("Quantity:", result.quantity)
            print("Date:", result.order_date)
            print("Unit_Price:", result.unit_price)
            print("Currency:",result.currency)
            print("Location_id:",result.location_id)

        except BusinessValidationError as exc:

            rejected += 1

            print("\n❌ BUSINESS VALIDATION FAILED")
            print("Order:", result.order_id)
            print("SKU:", result.sku)
            print("Reason:", exc)

    print("\n" + "=" * 50)

    print(f"Accepted records: {accepted}")
    print(f"Rejected records: {rejected}")


if __name__ == "__main__":
    main()