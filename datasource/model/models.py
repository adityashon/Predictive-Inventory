

from __future__ import annotations
from pydantic import BaseModel , Field , field_validator
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass
from typing import Optional


class AcceptedRecord(BaseModel):
    ''' a structure to verify the data that will ingest  '''

    order_id : str  = Field(min_length=1)
    sku : str  = Field(min_length=1)
    quantity : int = Field(gt=0)
    order_date : datetime 
    unit_price : int = Field(ge=0,default=float)
    currency : str = Field(min_length=1)
    location_id : Optional[str] = None

    @field_validator('currency')
    @classmethod
    def currency(cls, value :str | None)-> str|None:
        None if value is None else value.strip().upper()
        if len(value)!=3:
            raise ValueError(
                'Currency must be in 3 letter Code !'

            )
        return value
    

    @property
    def revenue(self)->Decimal | None:
        if self.unit_price is None:
            return None
        return self.unit_price * self.quantity





@dataclass
class RejectedRecords:
 number_row:int 
 reason:str
 raw_data:dict[str,str|None]

class InventoryRecord(BaseModel):
    sku: str
    location_id: str | None = None

    quantity_on_hand: int
    quantity_reserved: int = 0
    quantity_inbound: int = 0

    snapshot_datetime: datetime

    source: Optional[str]




class ReportJob(BaseModel):
    report_id: str = Field(min_length=1)
    report_type: str = Field(min_length=1)
    processing_status: str = Field(min_length=1)
    report_document_id: Optional[str] = None
    created_time: datetime
    data_start_time: Optional[datetime] = None
    data_end_time: Optional[datetime] = None
    
    
        