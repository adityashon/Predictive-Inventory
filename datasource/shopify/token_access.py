import requests
from datasource.shopify.exceptions import ShopifyAccessTokenError , ShopifyError



class AccessToken:

    def __init__(
            self,
            shop_name:str,client_id:str,client_secret:str)->None:
            '''Initialization'''
            self.shop_name = shop_name
            self.client_id = client_id
            self.client_secret = client_secret
            self.request = requests
            self.timeout = 30
            self.url = (f'https://{self.shop_name}.myshopify.com'
                        f"/admin/oauth/access_token")
            self.data = {
                  'grant_type':'client_credentials',
                  'client_id': self.client_id,
                  'client_secret':self.client_secret
                  
            }

    def get_access_token(self)->str:
        '''attempting to get access token to fetch data'''
        try:
            response = self.request.post(
            url=self.url,
            data=self.data,
            timeout=self.timeout
            ) 
            response.raise_for_status()
            payload = response.json()
            token = payload.get('access_token')
            if not token:
                 raise ShopifyAccessTokenError("No access_token in response")
            return token


        except self.request.exceptions.HTTPError as exc:
            raise ShopifyAccessTokenError(
                  f'Failed to receive access_token'
                  f'\n{exc}'
                  ) from exc
        except self.request.exceptions.RequestException as exc:
             raise ShopifyError(
                  f'An error occured'
                  f'\n{exc}'
             ) from exc
               
        
                



    
