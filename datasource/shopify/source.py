
from __future__ import annotations
from datetime import datetime
from typing  import Optional,Any,Literal
from model.models import AcceptedRecord
from datasource.shopify.client import ShopifyClient
from datasource.shopify.exceptions import ShopifyAuthenticateError,ShopifyApiError,ShopifyError
from datasource.shopify.Query.query import ORDERS_QUERY
from collections.abc import Iterator
from decimal import Decimal

PAGE_SIZE = 100
class ShopifyDataSource:

    def __init__(self,client:ShopifyClient,page_size:int=PAGE_SIZE)->None:
        '''Initialization'''
        self.client = client
        self.page_size = page_size

    def fetch_data(self)->Iterator[AcceptedRecord]:
        ''' reading all the shopify data '''
        cursor:Optional[str] = None
        while True:
            self.page_size+=1
            payload  = self.client.execute(query=ORDERS_QUERY,variables={'first':1,'after':cursor})

            order_page = payload['data']['orders']

            for order in order_page['nodes']:
                yield self._records_for_orders(order)
            page_info = order_page["pageInfo"]
            if not page_info['hasNextPage']:
                break;
            cursor = page_info['endCursor']


    def _records_for_orders(self,order:dict[str,Any])->Iterator[AcceptedRecord]:
        ''' recording for orders'''
        date_of_order = datetime.fromisoformat(order['createdAt'].replace('Z',"+00:00"))
        for item in order['lineItems']['nodes']:
            variant = order.get('variant')
            sku = variant.get('sku') if variant else None
            if not sku:
                continue

            money = order['originalUnitPriceSet']['shopMoney']
            yield AcceptedRecord(
                order_id= order["name"],
                sku= sku,
                quantity=order['quantity'],
                datetime=date_of_order,
                unit_price=Decimal(money['amount']),
                currency=order(money['currencyCode']),
            )