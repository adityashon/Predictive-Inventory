from __future__ import annotations
from typing import Any 
from collections.abc import Iterator
from decimal import Decimal
from datetime import datetime
from datasource.csvdata.ingestion.models import AcceptedRecord
from datasource.amazon.components.orders import AmazonOrderItemsAPI , AmazonOrdersAPI
from datasource.amazon.components.inventory import AmazonInventoryAPI
from datasource.amazon.components.reports import AmazonReportsAPI
'''
for understanding

    order_id : str  = Field(min_length=1)/
    sku : str  = Field(min_length=1)
    quantity : int = Field(gt=0)
    order_date : datetime /
    unit_price : int = Field(ge=0,default=float)
    currency : str = Field(min_length=1) /
    location_id : Optional[str] = None

'''

class AmazonDataSource:

    def __init__(self,orders:AmazonOrdersAPI,order_item:AmazonOrderItemsAPI):
        self.order_api = orders
        self.order_item_api = order_item

    def _fetch_sales(
        self,
        marketplace_ids:list[str],
        created_after: str | None = None,
        created_before: str | None = None,):
            '''we need to fetch `AmazonOrderId`,`PurchaseDate`,`OrderTotal[OrderTotal]`'''

            for order in self.order_api.get_all_orders(
                 marketplace_ids=marketplace_ids,
                 created_after=created_after,
                 created_before=created_before
            ):
                order_id = order.get('AmazonOrderId')
                if not order_id:
                     continue;
                order_date = order.get('PurchaseDate')
                if not order_date:
                     continue;
                currency = order.get('OrderTotal',{}).get('OrderTotal')

                yield from self._fetch_order_items(
                     order_id = order_id,
                     order_date=order_date,
                     currency = currency
                )
    def _fetch_order_items(
            self,
            order_id:str,
            order_date:str,
            currency:str
            ):

            for item in self.order_item_api.get_items(order_id=order_id):
                record = self._normalize_order_item(
                    order_id=order_id,
                    order_date=order_date,
                    currency = currency,
                    item=item
                    )
                if record is not None:
                     yield record
    def _normalize_order_item(
        self,
        order_id:str,
        order_date:str,
        currency:str,
        item:dict[str,Any])->Iterator[AcceptedRecord]:
            sku = item.get('SellerSKU')
            if  not sku:
                return None
            quntity =item.get('QuantityOrdered')
            if not quntity:
                return None
            price_data =  item.get('ItemPrice',{})
            unit_price =price_data.get('Amount')
            currency_code =price_data.get('CurrencyCode')
            if unit_price is None or currency_code:
                 return None

            return AcceptedRecord(
                order_id=order_id,
                sku=sku,
                order_date=datetime.isoformat(order_date.replace('Z',"+00:00")),
                quantity=quntity,
                unit_price=Decimal(str(unit_price)),
                currency=currency_code
            )


    def _fetch_inventory(self):pass
    def _fetch_reports(self):pass

         

         
         

                 

