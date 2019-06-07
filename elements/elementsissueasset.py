#!/usr/bin/env python
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from django.conf import settings 
from django.http import HttpResponse
from django.core.management import execute_from_command_line
from django.conf.urls import url, include

import sys

#settings.configure(
    #DEBUG=True,
    #SECRET_KEY='asecretkey',
    #ROOT_URLCONF=sys.modules[__name__],
    #ALLOWED_HOSTS=["localhost", "*"],
#)
 
def index(assetamount):
    rpc_port = 18884
    rpc_user = 'user1'
    rpc_password = 'password1'

    try:
        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    
        args = sys.argv
        print(args)

        issueasset = rpc_connection.issueasset(assetamount,1)
        assetid = issueasset['asset']
        print(assetid) 
        result = rpc_connection.listissuances(assetid)

    except JSONRPCException as json_exception:
        return HttpResponse("A JSON RPC Exception occured: " + str(json_exception))
    except Exception as general_exception:
        return HttpResponse("An Exception occured: " + str(general_exception))

    
    return HttpResponse(result)    

urlpatterns = [
    url(r'^elementsissueasset/', index)
]
 
if __name__ == "__main__":
    execute_from_command_line(sys.argv) 
