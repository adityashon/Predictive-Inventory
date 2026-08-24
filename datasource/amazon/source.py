from __future__ import annotations
from typing import Any 
from collections.abc import Iterator
from decimal import Decimal
from datetime import datetime
from datasource.model.models import AcceptedRecord ,InventoryRecord
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

    def __init__(self,orders:AmazonOrdersAPI,order_item:AmazonOrderItemsAPI,inventory:AmazonInventoryAPI):
        self.order_api = orders
        self.order_item_api = order_item
        # for inventory
        self.inventory_api = inventory

    def _fetch_sales(
        self,
        marketplace_ids:list[str],
        created_after: str | None = None,
        created_before: str | None = None,)->Iterator[AcceptedRecord]:
            '''we need to fetch `AmazonOrderId`,`PurchaseDate`,`OrderTotal[OrderTotal]`'''

            for order in self.order_api.get_all_orders(
                 marketplace_ids=marketplace_ids,
                 created_after=created_after,
                 created_before=created_before
            ):
                order_id = order.get('AmazonOrderId')
                if not order_id:
                     continue
                order_date = order.get('PurchaseDate')
                if not order_date:
                     continue
                currency_data = (order.get('OrderTotal') or {})
                currency=currency_data.get('CurrencyCode')

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
            )->Iterator[AcceptedRecord]:

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
        item:dict[str,Any])->AcceptedRecord|None:
            sku = item.get('SellerSKU')
            if  not sku:
                return None
            quantity =item.get('QuantityOrdered')
            if quantity is None:
                return None
            price_data =  item.get('ItemPrice',{})
            unit_price =price_data.get('Amount')
            currency_code =price_data.get('CurrencyCode')
            if unit_price is None or  not currency_code:
                 return None

            return AcceptedRecord(
                order_id=order_id,
                sku=sku,
                order_date=datetime.fromisoformat(order_date.replace('Z',"+00:00")),
                quantity=quantity,
                unit_price=Decimal(str(unit_price)),
                currency=currency_code
            )



    def _fetch_inventory(
        self,
        granularityType:str,
        granularityId:str,
        marketplaceIds:list[str]
        
            )->Iterator[InventoryRecord]:

         for summary in self.inventory_api.iter_inventory_summaries(
            granularityId=granularityId,
            granularityType=granularityType,
            marketplaceIds=marketplaceIds
            ):
                record = self._normalize_inventory(
                     granularityId=granularityId,
                     granularityType=granularityType,
                     summary = summary
                    )
                if record is not None:
                     yield record


    def _normalize_inventory(self,granularityId:str,granularityType:str,item:dict[str,Any])->InventoryRecord|None:
        sku = item.get('sellerSku')
        if not sku :return None
        quantity_data = item.get('inventoryDetails',) or {}
        quantity_on_hand = quantity_data.get('fulfillableQuantity')
        if quantity_on_hand is None:return None
        reserved_data = (quantity_data.get('reservedQuantity') or {})
        quantity_reserved = reserved_data.get('totalReservedQuantity',0)
        quantity_inbound  = quantity_data.get('inboundReceivingQuantity',0)
        if  quantity_inbound is None:return None
        last_updated = item.get('lastUpdatedTime')
        snapshot_datetime = datetime.fromisoformat(last_updated.replace('Z',"+00:00"))

        source = "amazon"

        return InventoryRecord(
             sku=sku,
             quantity_on_hand=quantity_on_hand,
            quantity_reserved=quantity_reserved,
            quantity_inbound=quantity_inbound,
            snapshot_datetime=snapshot_datetime,
            source= source
        )


              

         

    def _fetch_reports(self):pass

         

         
         

                 

