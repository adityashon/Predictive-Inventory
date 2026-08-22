# custon
class AmazonError(Exception):
    ''' Amazon general error'''

class AmazonAuthError(AmazonError):
    ''' Amazon authentication error '''


class AmazonAPIError(AmazonError):
    """Raised when Amazon SP-API returns an error or the request fails."""

class AmazonOrderError(AmazonAPIError):
    '''Raised when Amazon SP-API returns an error  or the request fails of Orders. '''


class AmazonSalesError(AmazonError):
    ''' Amazon sales error '''
class AmazonInventoryError(AmazonError):
    ''' amazon inventory errror '''