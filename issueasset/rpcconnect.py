# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your views here.
import logging

# elementsissue.pyから移植
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from django.http import HttpResponse
from django.core.management import execute_from_command_line

class RPCConnect:

    # 初期処理
    def __init__(self) :
        print("start")

    def sayStr():
        print ("t12")
        logging.debug("t12")


    def rpcCon():

        logging.debug("test")
        # elementsへの接続
        rpc_port = 18884
        rpc_user = 'user1'
        rpc_password = 'password1'

        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
       
