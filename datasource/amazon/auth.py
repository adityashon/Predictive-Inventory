
from __future__ import annotations
from dataclasses import dataclass
from datasource.amazon.exceptions import AmazonAuthError
import requests

@dataclass(frozen=True)
class LWAAccessToken:
    access_token:str
    expires_in:int
    token_type:str

class AmazonAuth:
      def __init__(
               self,
               client_id:str,
               client_secret:str,
               refresh_token:str,
               timeout:int=30,
               exp_in:int = 3600):
                    self.client_id = client_id
                    self.client_secret = client_secret
                    self.ref_token = refresh_token
                    self.timeout = timeout
                    self.exp_in = exp_in
                    self.LWAurl = 'https://api.amazon.com/auth/o2/token'
                    self.request = requests
                    self.maindata = {
                            'grant_type':'refresh_token',
                            'client_id':self.client_id,
                            'client_secret':self.client_secret,
                            'refresh_token':self.ref_token
                            }

      def get_token_access(self)->LWAAccessToken:
        try:
            response = self.request.post(
            url=self.LWAurl,
            headers={'Content-type':'application/x-www-form-urlencoded'},
            data=self.maindata,
            timeout=self.timeout
            )
            response.raise_for_status()
        except self.request.exceptions.RequestException as exc:
              raise AmazonAuthError(f' Amazon authentication failed :\n  {exc}') from exc
        payload = response.json()
        access_token = payload.get('access_token')
        if not access_token:
              raise AmazonAuthError(
                    'Amazon did not return an access token'
              )

        return LWAAccessToken(
              access_token=access_token,
              expires_in=payload.get('expires_in',self.exp_in),
              token_type=payload.get('token_type','bearer')
            )


         