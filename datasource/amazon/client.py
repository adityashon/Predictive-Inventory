from __future__ import annotations
import requests
from dataclasses import dataclass
from datasource.amazon.exceptions import AmazonAPIError
from datasource.amazon.auth import AmazonAuth ,LWAAccessToken
from typing import Any
import time

TOKEN_REFRESH_BUFFER_SECONDS = 60
MAX_RETRIES = 5
INITIAL_BACKOFF_SECONDS = 1.0

@dataclass(frozen=True)
class AmazonClientConfig:
    endpoint:str
    region:str
    user_agent:str

class AmazonSPAPIClient:
    ''' Amazon client  '''
    def __init__(
            self,
            auth:AmazonAuth,
            config:AmazonClientConfig,
            timeout:int=30
            )->None:
        self.auth = auth
        self.config = config
        self.timeout = timeout
        self.session = requests.Session()
        self._token = LWAAccessToken | None = None
        self._token_expires_at :float = 0.0

    def get_valid_token(self)->str:
        ''' to verify the token thay we accessed, with expiration time '''
        __time__ = time.monotonic()
        if self._token is None and  __time__ >= self._token_expires_at:
            self._token = self.auth.get_token_access()
            self._token_expires_at = (
                __time__ + self._token_expires_at - TOKEN_REFRESH_BUFFER_SECONDS
            )
        return self._token.access_token

    def _get_(self,method:str,path:str,params:dict[str,Any]|None=None)->dict[str,Any]:
            ''' a method to get data '''
            return self.__request__('GET',path,params)
    def _post_(self,method:str,path:str,body:dict[str,Any]|None=None)->dict[str,Any]:
            ''' a method to post data '''
            return self.__request__('POST',path,body)
    

    def __request__(
              self,
              method:str,
              path:str,
              params:dict[str,Any]|None=None,
              body:dict[str,Any]|None=None,
    )->dict[str,Any]:
        ''' a method to run get and post methods'''

        url = self.config.endpoint.rstrip("/") +"/"+path.lstrip("/")
        backoff = INITIAL_BACKOFF_SECONDS

        for attempts in range(1,MAX_RETRIES+1):
            headers = {
                  'x-amz-access-token': self.get_valid_token(),
                  'user_agent':self.config.user_agent,
                  'Content-type':'application/json'
            }
            try:
                response = self.session(
                    url=url,
                    headers=headers,
                    params=params,
                    body=body,
                    timeout=self.timeout
                    )

            except requests.exceptions.HTTPError as exc:
                raise AmazonAPIError(
                      'Amazon SP-API request failed for {path}: {exc}'
                 ) from exc
            if response.status_code == 429: # too many requests in single point of time

                if attempts == MAX_RETRIES:
                    raise AmazonAPIError(
                           'Amazon SP-API throttled after {MAX_RETRIES} retries: {path}'
                        )
                retry_after = float(response.headers.get('retry-After'),backoff)
                time.sleep(retry_after)
                backoff*=2
                continue;
            return self._response_handler(response,path)
        
    @staticmethod
    def _response_handler(self,response:requests.Response,path:str):
        ''' to handle responses '''
        try:
             if response.ok:
                  return response.json()
        except requests.exceptions.HTTPError as exc:
             raise AmazonAPIError(
                  'f"Amazon SP-API error {response.status_code} for {path}: {response.text}'
             ) from exc
            

         
         

