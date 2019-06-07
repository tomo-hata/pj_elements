# -*- coding: utf-8 -*1
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.http.response import HttpResponse
from datetime import datetime
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from django.shortcuts import redirect
from . import forms
from django.core.management import execute_from_command_line
from . import elementsissueasset


class Hello(models.Model):
    your_name = models.CharField(max_length=10)

    def __str__(self):
        return "<{0}>".format(self.your_name)

class IssueAsset(models.Model):
    assetamount = models.CharField(max_length=30)
    #tokenamount = models.CharField(max_length=1)
    tokenamount = 1

    def __str__(self):

        print(self)        

        return "<{0}>".format(self.assetamount)

    def issueasset(assetamount):

        rpc_port = 18884
        rpc_user = 'user1'
        rpc_password = 'password1'

        try:
            rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))

            issueasset = rpc_connection.issueasset(assetamount,tokenamount)
            assetid = issueasset['asset']
            print(assetid)
            result = rpc_connection.listissuances(assetid)

        except JSONRPCException as json_exception:

            return HttpResponse("A JSON RPC Exception occured: " + str(json_exception))
        except Exception as general_exception:
            return HttpResponse("An Exception occured: " + str(general_exception))

        return HttpResponse(result)

        #return "<{0}>".format(self.assetamount)

    if __name__ == "__main__":
        execute_from_command_line(sys.argv)

