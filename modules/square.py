#!/usr/bin/env python3
from square.client import Client


class Square:
    """CLASS SQUARE"""

    def __init__(self, user_token, env='sandbox'):
        """
        ----------------
        METHOD: __init__
        ----------------
        Initializer that sets the available endpoints
        associated with a user.

        @user_token: must provide a user_auth_token
        @env: Optional, however env only supports 'production' or 'sandbox'
              If env hasn't been offered, env defaults to sandbox
        """
        try:
            self._api_endpoints = Client(access_token=user_token,
                                         environment=env)
        except:
            raise NameError('The User Auth Token or environment option is not valid')

    @property
    def api_endpoints(self):
        """Returns the available API endpoints associated with the user"""
        return self._api_endpoints
    
    @api_endpoints.setter
    def api_endpoints(self, sq_client):
        """Sets the instance attribute called api_endpoints"""
        if isinstance(sq_client, Client):
            self._api_endpoints = sq_client
        else:
            raise NameError('Can\'t set the client to a non-Square client')
