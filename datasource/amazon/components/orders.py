from __future__ import annotations 
from typing import Any
from datasource.amazon.client import AmazonSPAPIClient
from datasource.amazon.exceptions import AmazonAPIError ,AmazonOrderErrorf
from collections.abc import Iterator


class AmazonOrdersAPI:

    def __init__(
        self,
        client:AmazonSPAPIClient
        ):
        self.client = client
        self.ORDERS_PATH = '/orders/v0/orders'
        

    def get_orders(
        self,
        *,
        marketplace_ids: list[str],
        created_after: str | None = None,
        created_before: str | None = None,
        order_statuses: list[str] | None = None,
        fulfillment_channels: list[str] | None = None,
        max_results_per_page: int = 100,
        next_token :str|None = None
    ):
        if not marketplace_ids:
            raise ValueError(
                'At least one marketplace ID is required.'
            )
        if 1<= max_results_per_page <=100:
            raise ValueError(
                'max_results_per_page must be between 1 and 100.'
            )
        if created_after is None and not order_statuses:
            raise ValueError(
                'created_after is required unless order_statuses is provided.'
            )
        params :dict[str,Any] = {
            'MarketplaceIds': ','.join(marketplace_ids),
            'MaxResultsPerPage':max_results_per_page
        }
        if created_after is not None:
            params['CreatedAfter']=created_after
        if created_before is not None:
            params['CreatedBefore']=created_before
        if order_statuses:
            params['OrderStatuses']=order_statuses
        if fulfillment_channels:
            params['FulfillmentChannels']=fulfillment_channels
        if next_token is not None:
            params['NextToken'] = next_token

        return self.client._get_('GET',path=self.ORDERS_PATH,params=params)
# iter_orders
    def get_all_orders(
        self,
        marketplace_ids: list[str],
        created_after: str | None = None,
        created_before: str | None = None,
        order_statuses: list[str] | None = None,
        fulfillment_channels: list[str] | None = None,
        max_results_per_page: int = 100,
        )->Iterator[dict[str,Any]]:

        next_token:str|None = None

        while True:
            response = self.get_orders(
                marketplace_ids=marketplace_ids,
                created_after=created_after,
                created_before=created_before,
                order_statuses=order_statuses,
                fulfillment_channels=fulfillment_channels,
                max_results_per_page=max_results_per_page,
                next_token=next_token
            )
            payload = response.get('payload',{})
            orders = payload.get('Orders',[])

            for order in  orders:
                yield order
            next_token = payload.get('NextToken')
            if not next_token:
                 break;

class AmazonOrderItemsAPI:

    def __init__(
            self,
            client:AmazonSPAPIClient):
        self.client = client
        self.ORDERS_PATH_ITEM = '/orders/v0/orders/{order_id}/orderItems'
        


    def get_order_items(
            self,
            order_id:str,
            next_token:str|None = None
    ):
        path = self.ORDERS_PATH_ITEM.format(order_id)
        if not order_id:
            raise ValueError(
                '"order_id is required.'
            )
        params:dict[str,Any] = {}
        if not next_token:
            params['NextToken'] = next_token

        return self.client._get_('GET',path=path,params=params)
# iter_items
    def get_items(
            self,
            order_id:str
            )->Iterator[dict[str,Any]]:
        
        next_token:str|None = None

        while True:
            response = self.get_order_item(
                order_id=order_id,
                next_token=next_token
            )
            payload = response.get('payload',{})
            items = payload.get('Items',[])
            for item in items:
                yield item

            next_token = payload.get('NextToken')
            if not next_token:
                break;
    







