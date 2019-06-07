# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import logging
from rpcconnect import RPCConnect

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
            
            # elementsへの接続
            rpc_port = 18884
            rpc_user = 'user1'
            rpc_password = 'password1'

            try:
                rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))

                assetamount = request.POST.get('assetamount')
                tokenamount = request.POST.get('tokenamount')

                logging.debug(assetamount)
                logging.debug(tokenamount)
                
                issueasset = rpc_connection.issueasset(assetamount,tokenamount)
                assetid = issueasset['asset']
                logging.debug(assetid)
                result = rpc_connection.listissuances(assetid)

            except JSONRPCException as json_exception:
                errJSONRPC = HttpResponse("A JSON RPC Exception occured: " + str(json_exception))
                messages.error(errJSONRPC)
            except Exception as general_exception:
                errHttp = HttpResponse("An Exception occured: " + str(general_exception))
                messages.error(errHttp)
            
            succResult =  HttpResponse(result)
            logging.debug(succResult)

            # elements ここまで

            # moto
            # save()メソッドを呼ぶだけでModelを使ってDBに登録される。
            form.save()
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
