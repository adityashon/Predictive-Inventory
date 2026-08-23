

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
    
    
        