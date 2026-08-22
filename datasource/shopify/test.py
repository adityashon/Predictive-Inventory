import os
from dotenv import load_dotenv
from datasource.shopify.token_access import AccessToken
from datasource.shopify.client import ShopifyClient
from typing import Any
from dataclasses import dataclass
from datasource.shopify.source import ShopifyDataSource
from datasource.shopify.client import ShopifyClient
import datetime
load_dotenv()
shop_domain = os.getenv('SHOPIFY_SHOP')
client_id = os.getenv('SHOPIFY_CLIENT_ID')
client_serect = os.getenv('SHOPIFY_CLIENT_SECRET')
access_token = os.getenv('ACCESS_TOKEN')

@dataclass
class TokenOutput:
    token:str
    access_token:str
    status:str


class ShopifyTest:


    def access_token_test(self,num:int = 20)->dict[str,Any]:
        ''' test perform to get access token '''
        if AccessToken:
            get_token = AccessToken(shop_domain,client_id,client_serect).get_access_token()
            length = len(get_token)
            remain_length= length- num
            return TokenOutput (
                token=get_token,
                access_token=get_token.replace(get_token[num:],"*"*remain_length),
                status='token received!'
            )
        else:
            return("no token")

    def data_source_test(self):
        '''test perform to test shopify data fetching'''
        token = self.access_token_test()
        client = ShopifyClient(shop_domain,access_token=token.token)
        instance = ShopifyDataSource(client)
        return instance.fetch_data()



# --- perform test ---

test = ShopifyTest()
print(test.access_token_test())
for r in test.data_source_test():
    print(r)
        