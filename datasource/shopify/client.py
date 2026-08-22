from __future__ import annotations
import requests
from datasource.shopify.token_access import AccessToken


class ShopifyClient:
    def __init__(self, shop_domain: str, access_token: str, api_version: str = '2026-07') -> None:
        '''Initilization'''
        self.domain = shop_domain
        self._token = access_token
        self.version = api_version
        self.url = f"https://{self.domain}.myshopify.com/admin/api/{self.version}/graphql.json"
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": self._token,
            }
        )

    def execute(self, query: str, variables: dict | None = None) -> dict:
        ''' executing the query to fetch data'''
        response = self._session.post(
            url=self.url,
            json={"query": query, "variables": variables or {}},
            timeout=30,
        )
        response.raise_for_status()

        payload = response.json()
        if payload.get("errors"):
            raise RuntimeError(f"Shopify GraphQL error: {payload['errors']}")

        return payload