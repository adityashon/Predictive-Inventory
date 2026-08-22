
class ShopifyError(Exception):
    '''Base Shopify Ingestion Errror'''


class ShopifyApiError(ShopifyError):
    '''Shopify admin API error'''

class ShopifyAuthenticateError(ShopifyError):
    '''Shopify authorisation failed'''
class ShopifyAccessTokenError(ShopifyError):
    '''Shopify token access faied'''