
from __future__ import annotations
import csv
from pathlib import Path
from collections.abc import Iterator
from pydantic import ValidationError
from datasource.csvdata.ingestion.exceptions import FileIngestionError, SchemaError
from datasource.csvdata.ingestion.models import AcceptedRecord , RejectedRecords



class CsvDataSource:
    '''this is a class where the CSV data will fetch'''
    REQUIRED_COLUMNS = {"order_id","sku","quantity","order_date",}

    OPTIONAL_COLUMNS = {"unit_price","currency","location_id",}

    def __init__(self,f_path:str|Path)->None:
        self.f_path = Path(f_path)

    def fetch_data(self)->Iterator[AcceptedRecord| RejectedRecords]:
        self._validate_file()
        with self.f_path.open('r',encoding='utf-8-sig',newline="") as file:
            reader = csv.DictReader(file)
            headers = self._validate_headers(reader.fieldnames)

            for number_row ,row in enumerate(reader,start=2):
                __row__ = {
                    headers[key]:value 
                    for key , value in row.items()
                    if key is not  None
                }
                
                try:
                    yield self._parse_row(__row__)
                  
                except(ValidationError) as exc:
                    yield RejectedRecords(
                        number_row= number_row,
                        reason=f"{exc}",
                        raw_data=__row__
                    )
# validators
    def _validate_file(self)->None:
        if  not self.f_path.exists():
             raise FileIngestionError(
                 f'File do not exists',
                 f"{self.f_path}"
             )
        if not self.f_path.is_file():
            raise FileIngestionError(
                f" Given path not have any file"
                f"{self.f_path}"
            )
        if self.f_path.suffix.lower() != ".csv":
            raise FileIngestionError(
                f"File must have csv extension/format"
            )

        
    def _validate_headers(self,headers:list[str]|None)-> dict[str,str]:
        if not headers:
            raise SchemaError(f'CSV do not contain headers')

        normalized_headers :dict[str,str]= {}

        for header in headers:
            normalize = (header.strip().lower().replace(" ","_"))
            normalized_headers[header] = normalize
        normalized_names = set(normalized_headers.values())

        missing = (self.REQUIRED_COLUMNS - normalized_names)
        if missing:
            raise SchemaError(
                f'missing required columns : '+",".join(sorted(missing))
            )
        return normalized_headers
# a parser for csv
    @staticmethod
    def _parse_row(rows:dict[str,str|None])->AcceptedRecord:
        sanitized = {
            key.strip().lower():(value.strip()
            if isinstance(value,str) else value)
            for key , value in rows.items()
        }
        return AcceptedRecord(
            order_id=sanitized.get("order_id",""),
            sku=sanitized.get("sku"),
            quantity=sanitized.get("quantity",0),
            order_date=sanitized.get("order_date"),
            datetime = sanitized.get("datetime"),
            unit_price=sanitized.get("unit_price"),
            currency=sanitized.get("currency"),
            location_id=sanitized.get('location_id')
        )
    
        
             


