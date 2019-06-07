# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import logging
import json
import simplejson
from django.core import serializers
from decimal import Decimal
from rpcconnect import RPCConnect

import sys

# ページネーター
from django.core.paginator import (
    Paginator,  # ページネーター本体のクラス
    EmptyPage,  # ページ番号が範囲外だった場合に発生する例外クラス
    PageNotAnInteger  # ページ番号が数字でなかった場合に発生する例外クラス
)
from django.shortcuts import (
    render,
    redirect,
)
from .models import Posting
from .forms import PostingForm
from django.contrib import messages

# elementsissue.pyから移植
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core.management import execute_from_command_line

def _get_page(list_, page_no, count=5):
    """ページネーターを使い、表示するページ情報を取得する"""
    paginator = Paginator(list_, count)
    try:
        page = paginator.page(page_no)
    except (EmptyPage, PageNotAnInteger):
        # page_noが指定されていない場合、数値で無い場合、範囲外の場合は
        # 先頭のページを表示する
        page = paginator.page(1)
    return page


def index(request):
    """表示・投稿を処理する"""
    # ModelFormもFormもインスタンスを作るタイミングでの使い方は同じ
    form = PostingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            
            #Elements上でアセット発行関数呼び出し
            #succResult = elements_issueasset(request)
            assetid = elements_issueasset(request)
            
            logging.debug("tttt2222")
            #obj = json.load(succResult)
            
            
            #data = succResult.json

            logging.debug("tttt")
            #logging.debug(succResult.keys())
            #logging.debug(data)
            #logging.debug(succResult)
            #logging.debug(assetamount)
            #logging.debug(tokenamount)
            logging.debug(assetid)

            
            # moto
            # save()メソッドを呼ぶだけでModelを使ってDBに登録される。
            obj = form.save(commit=False)
            obj.assetid = assetid
            obj.save()
            #created_at = ""
            #Posting.objects.create(assetid)
            # メッセージフレームワークを使い、処理が成功したことをユーザーに通知
            messages.success(request, 'アセット発行を受付ました。')
            logging.debug('debug messages')
            logging.debug(request)
            return redirect('issueasset:index')
        else:
            # メッセージフレームワークを使い、処理が失敗したことをユーザーに通知する
            messages.error(request, '入力内容に誤りがあります。')
    page = _get_page(
        Posting.objects.order_by('-id'),  # 投稿を新しい順に並び替えて取得する
        request.GET.get('page')  # GETクエリからページ番号を取得する
    )
    contexts = {
        'form': form,
        'page': page,
    }
    return render(request, 'issueasset/index.html', contexts)


    
# ********************************
# 新規アセット発行
def elements_issueasset(request):

        try:
            # RPC接続設定呼び出し
            rpc_connection = rpcCon()


            req_assetamount = request.POST.get('assetamount')
            req_tokenamount = request.POST.get('tokenamount')

            logging.debug(req_assetamount)
            logging.debug(req_tokenamount)
            
            issueasset = rpc_connection.issueasset(req_assetamount,req_tokenamount)
            assetid = issueasset['asset']
            logging.debug(assetid)
            result = rpc_connection.listissuances(assetid)
            
            logging.debug("tttt111")

        except JSONRPCException as json_exception:
            errJSONRPC = HttpResponse("A JSON RPC Exception occured: " + str(json_exception))
            messages.error(errJSONRPC)
        except Exception as general_exception:
            errHttp = HttpResponse("An Exception occured: " + str(general_exception))
            messages.error(errHttp)
        
        #return  HttpResponse(simplejson.dumps(result))
        #return  HttpResponse(result, content_type='application/json; charset=UTF-8')
        data = HttpResponse(result, content_type='application/json; charset=UTF-8')
        #data = serializers.serialize("json", data, stream=sys.stdout, indent=2)
        logging.debug(data)
        return assetid


# ********************************
# RPC接続設定
def rpcCon():
    # elementsへの接続
        rpc_port = 18884
        rpc_user = 'user1'
        rpc_password = 'password1'


        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))

        return rpc_connection