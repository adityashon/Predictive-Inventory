
from __future__ import annotations
from typing import Any
from datasource.amazon.client import AmazonSPAPIClient
from collections.abc import Iterator

'''
createreport,
getreports,
getreport,
getdocuments/_id,

'''
class AmazonReportsAPI:

    def __init__(
            self,
            client:AmazonSPAPIClient
            ):
        self.client = client
        self.REPORT_PATH = '/reports/2021-06-30/reports'
        self.DOCUMENT_PATH  ="/reports/2021-06-30/documents" 

    def create_report(
        self,
        reportType:str,
        marketplaceIds:list[str],
        dataStartTime:str|None = None,
        dataEndTime:str|None = None,
        reportOptions:dict[str,Any] |None=None 
        ):      
            if not reportType :
                raise ValueError(
                    'Report type is required'
                )
            if not marketplaceIds:
                raise ValueError(
                    'at least one market id is required'
                )
            body = {
                'reportType':reportType,
                'marketplaceIds': ",".join(marketplaceIds)
            }
            if dataStartTime is not None:
                body['dataStartTime'] = dataStartTime
            if dataEndTime is not None:
                body['dataEndTime'] = dataEndTime
            if reportOptions is not None:
                body['reportOptions'] = reportOptions

            return self.client._post_(path=self.REPORT_PATH,body=body)

    def get_reports(
            self,
            *,
            reportTypes:list[str],
            marketplaceIds:list[str],
            processingStatuses:list[str]|None=None,
            pageSize :int|None = None,
            createdSince:str|None = None,
            createdUntil:str|None = None,
            nextToken:str|None=None
        )->dict[str,Any]:
                
                if not reportTypes:
                    raise ValueError(
                        'Report type is required'
                    )
                if not marketplaceIds:
                    raise ValueError(
                        'at least one market id is required'
                    )
                params :dict[str,Any] = {
                     'reportTypes':','.join(reportTypes),
                     'marketplaceIds':','.join(marketplaceIds)
                }
                if processingStatuses is not None:
                     params['processingStatuses'] = ",".join(processingStatuses)
                if createdSince is not None:
                     params['createdSince']=createdSince
                if createdUntil is not None:
                     params['createdUntil'] = createdUntil
                

                if pageSize is not None:
                    if  not 1<= pageSize <=100:
                          raise ValueError(
                               'page_size must be between 1 and 100.'
                          )
                    params['pageSize'] =pageSize

                if nextToken is not None:
                     params['nextToken'] = nextToken

# amazon will return a report_id
                return self.client._get_(path=self.REPORT_PATH,params=params)

    def iter_reports(
        self,
        reportTypes:list[str],
        marketplaceIds:list[str],
        processingStatuses:list[str]|None=None,
        pageSize :int|None = None,
        createdSince:str|None = None,
        createdUntil:str|None = None,
    )->Iterator[dict[str,Any]]:

        next_token:str|None = None
        while True:
            response = self.get_reports(
                reportTypes=reportTypes,
                marketplaceIds=marketplaceIds,
                processingStatuses=processingStatuses,
                pageSize=pageSize,
                createdSince=createdSince,
                createdUntil=createdUntil,
                nextToken=next_token
                )
            payload = response.get('payload',{})
            reports = payload.get('reports',[])
            for report in reports:
                 if report is not None:
                      yield report
            next_token = payload.get('nextToken')
            if not next_token:
                 break


    def get_report(self,report_id:str)->dict[str,Any]:

            if not report_id:
                raise ValueError(
                   'report id  is reuqired'
                )
            path = f'{self.REPORT_PATH}/{report_id}'
            params :dict[str,Any]={
                 'order_id':report_id
            }

            return self.client._get_(path=path,params=params)

    def get_report_document(self,document_id:str)->dict[str,Any]:

        if not document_id:
              raise ValueError(
                   'report_document_id is required.'
                   )
        path = f'{self.DOCUMENT_PATH}/{document_id}'
        params:dict[str,Any] = {
             'document_id':document_id
        }
        return self.client._get_(path=path,params=params)


         



    

