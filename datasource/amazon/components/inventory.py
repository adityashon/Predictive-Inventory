from __future__ import annotations
from typing import Any 
from datasource.amazon.client import AmazonSPAPIClient

'''
getInventorySummaries
'''

class AmazonInventoryAPI:

    def __init__(self,client:AmazonSPAPIClient):
        self.client = client
        self.IN_SUM_PATH = '/fba/inventory/v1/summaries'

    def get_inventory_summaries(
        self,
        *,
        granularityType:str,
        granularityId:str,
        details:bool = True,
        sellerSkus:list[str]|None=None,
        startDateTime:str|None=None,
        marketplaceIds:list[str]|None=None,
        nextToken:str|None=None
        ):

            if not granularityType:
                raise ValueError(
                    'granularityType is required'
                )
            if not granularityId:
                raise ValueError(
                     'granularityId is required'
                )
            params :dict[str,Any]={
                'granularityId':granularityId,
                'granularityType':granularityType,
                'details':details

            }
            if sellerSkus is not None:
                 params['sellerSkus'] =",".join(sellerSkus)
            if startDateTime is not None:
                 params['startDateTime'] =startDateTime
            if marketplaceIds is not None:
                 params['marketplaceIds'] = ','.join(marketplaceIds)

            if nextToken is not None:
                 params['nextToken'] = nextToken
            return self.client._get_(path=self.IN_SUM_PATH,params=params)
    

        

