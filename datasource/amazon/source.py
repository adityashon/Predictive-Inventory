from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from decimal import Decimal
from typing import Any

from datasource.amazon.components.orders import AmazonOrdersAPI, AmazonOrderItemsAPI
from datasource.csvdata.ingestion.models import AcceptedRecord


class AmazonSource:


    def __init__(
        self,
        orders_api: AmazonOrdersAPI,
        order_items_api: AmazonOrderItemsAPI,
    ) -> None:
        self.orders_api = orders_api
        self.order_items_api = order_items_api


# sales
    def fetch_sales(
        self,
        *,
        marketplace_ids: list[str],
        created_after: str | None = None,
        created_before: str | None = None,
    ) -> Iterator[AcceptedRecord]:
        """
        Fetch Amazon orders and convert their order items into
        canonical AcceptedRecord objects.
        """
        orders = self.orders_api.iter_orders(
            marketplace_ids=marketplace_ids,
            created_after=created_after,
            created_before=created_before,
        )

        for order in orders:
            order_id = order.get("AmazonOrderId")
            if not order_id:
                continue

            purchase_date = order.get("PurchaseDate")
            if not purchase_date:
                continue

            currency = order.get("OrderTotal", {}).get("CurrencyCode")

            yield from self._fetch_order_items(
                order_id=order_id,
                order_date=purchase_date,
                currency=currency,
            )


# order items


    def _fetch_order_items(
        self,
        *,
        order_id: str,
        order_date: str,
        currency: str | None,
    ) -> Iterator[AcceptedRecord]:
        for item in self.order_items_api.iter_order_items(order_id=order_id):
            record = self._normalize_order_item(
                order_id=order_id,
                order_date=order_date,
                currency=currency,
                item=item,
            )
            if record is not None:
                yield record

# normalisation
    

    @staticmethod
    def _normalize_order_item(
        *,
        order_id: str,
        order_date: str,
        currency: str | None,
        item: dict[str, Any],
    ) -> AcceptedRecord | None:
        """
        Convert one Amazon order item into an AcceptedRecord.
        Returns None for items that can't be turned into a valid
        record (no SKU, no price, no quantity, no currency).
        """
        sku = item.get("SellerSKU")
        if not sku:
            return None

        quantity = item.get("QuantityOrdered")
        if quantity is None:
            return None

        price_data = item.get("ItemPrice")
        if not price_data:
            # Items without ItemPrice (e.g. gifts, promotions) are
            # skipped rather than recorded with a fabricated price.
            return None

        unit_price_value = price_data.get("Amount")
        item_currency = price_data.get("CurrencyCode") or currency
        if unit_price_value is None or not item_currency:
            return None

        return AcceptedRecord(
            order_id=order_id,
            sku=sku,
            quantity=int(quantity),
            order_date=datetime.fromisoformat(order_date.replace("Z", "+00:00")),
            unit_price=Decimal(str(unit_price_value)),
            currency=item_currency,
        )