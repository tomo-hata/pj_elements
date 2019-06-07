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
import ConfigParser
from . import config

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
from .models import IssueAsset, SendAsset
from .forms import IssueAssetForm, SearchForm, SendAssetForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


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


# ********************************
# 新規アセット発行
@login_required
def issueasset(request):
    """表示・投稿を処理する"""
    # ModelFormもFormもインスタンスを作るタイミングでの使い方は同じ
    logging.debug("test_start")
    login_user_id = request.user.id
    login_user_name = request.user.username
    logging.debug(login_user_id)
    logging.debug(login_user_name)
    
    form = IssueAssetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            
            #Elements上でアセット発行関数呼び出し
            # assetid = elements_issueasset(request)
            
            try:
                # RPC接続設定呼び出し
                rpc_connection = rpcCon(login_user_name)
    
    
                req_assetamount = request.POST.get('assetamount')
                req_tokenamount = request.POST.get('tokenamount')
    
                logging.debug(req_assetamount)
                logging.debug(req_tokenamount)
                
                issueasset = rpc_connection.issueasset(req_assetamount,req_tokenamount)
                assetid = issueasset['asset']
                txid = issueasset['txid']
                logging.debug(assetid)
                #result = rpc_connection.listissuances(assetid)
                result = rpc_connection.getwalletinfo(assetid)
                logging.debug(result['balance'])
                
                logging.debug("tt20190121")
                
                balance = result['balance']
                
                logging.debug("tttt111")
    
            except JSONRPCException as json_exception:
                errJSONRPC = HttpResponse("A JSON RPC Exception occured: " + str(json_exception))
                messages.error(errJSONRPC)
            except Exception as general_exception:
                errHttp = HttpResponse("An Exception occured: " + str(general_exception))
                messages.error(errHttp)
            
            data = HttpResponse(result, content_type='application/json; charset=UTF-8')
            logging.debug(data)


            logging.debug("tttt2222")

            logging.debug("tttt")
            logging.debug(assetid)

            # moto
            # save()メソッドを呼ぶだけでModelを使ってDBに登録される。
            obj = form.save(commit=False)
            obj.assetid = assetid
            obj.txid = txid
            # 本当はbalanceの値で取得するのは正しいとは言えない。（listissuancesでassetamountを取得したいところ）
            obj.assetamount = balance
            obj.save()
            #created_at = ""
            #IssueAsset.objects.create(assetid)
            # メッセージフレームワークを使い、処理が成功したことをユーザーに通知
            messages.success(request, 'アセット発行を受付ました。')
            logging.debug('debug messages')
            logging.debug(request)
            return redirect('issueasset:issueasset')
        else:
            # メッセージフレームワークを使い、処理が失敗したことをユーザーに通知する
            messages.error(request, '入力内容に誤りがあります。')
    page = _get_page(
        IssueAsset.objects.order_by('-id'),  # 投稿を新しい順に並び替えて取得する
        request.GET.get('page')  # GETクエリからページ番号を取得する
    )
    contexts = {
        'form': form,
        'page': page,
        'user_name': login_user_name,
    }
    return render(request, 'issueasset/issueasset.html', contexts)


# ********************************
# 発行済みアセット情報取得
@login_required
def search_issuance(request):
    """表示・投稿を処理する"""
    # ModelFormもFormもインスタンスを作るタイミングでの使い方は同じ
    
    logging.debug("test_start")
    login_user_id = request.user.id
    login_user_name = request.user.username
    logging.debug(login_user_id)
    logging.debug(login_user_name)
    
    form = SearchForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            
            try:
                # RPC接続設定呼び出し
                logging.debug("test_connect_start")
                logging.debug(login_user_name)
                rpc_connection = rpcCon(login_user_name)
    
                req_assetid = request.POST.get('assetid')
                
                #result = rpc_connection.listissuances(req_assetid)
                result = rpc_connection.getwalletinfo(req_assetid)
                
                logging.debug(result['balance'])
                
                balance = result['balance']
                unconfirmed_balance = result['unconfirmed_balance']

                
            except JSONRPCException as json_exception:
                errJSONRPC = HttpResponse("A JSON RPC Exception occured: " + str(json_exception))
                messages.error(errJSONRPC)
            except Exception as general_exception:
                errHttp = HttpResponse("An Exception occured: " + str(general_exception))
                messages.error(errHttp)
            
            #data = HttpResponse(result, content_type='application/json; charset=UTF-8')
            data = result
            
            #data = result
            logging.debug("tt5555tt")
            logging.debug(data)
            #return data
            
            logging.debug("tttt2222")


            #created_at = ""
            #IssueAsset.objects.create(assetid)
            # メッセージフレームワークを使い、処理が成功したことをユーザーに通知
            messages.success(request, '検索結果を表示します。')
            logging.debug('debug messages')
            logging.debug(request)
            #return redirect('issueasset:search_issuance')
            
            page = _get_page(
                IssueAsset.objects.order_by('-id'),  # 投稿を新しい順に並び替えて取得する
                request.GET.get('page')  # GETクエリからページ番号を取得する
            )
            
            contexts = {
                'form': form,
                'page': page,
                'result': data,
                'assetid': req_assetid,
                'balance': balance,
                'unconfirmed_balance': unconfirmed_balance,
                'user_name': login_user_name,
            }
            return render(request, 'issueasset/search_issuance.html', contexts)

        else:
            # メッセージフレームワークを使い、処理が失敗したことをユーザーに通知する
            messages.error(request, '入力内容に誤りがあります。')
    page = _get_page(
        IssueAsset.objects.order_by('-id'),  # 投稿を新しい順に並び替えて取得する
        request.GET.get('page')  # GETクエリからページ番号を取得する
    )
    

    contexts = {
        'form': form,
        'page': page,
        #'result': data,
        'user_name': login_user_name,
    }
    
    logging.debug("t1t1t1")
    
    return render(request, 'issueasset/search_issuance.html', contexts )


# ********************************
# アセット送金
@login_required
def sendasset(request):
    """表示・投稿を処理する"""
    # ModelFormもFormもインスタンスを作るタイミングでの使い方は同じ
    
    logging.debug("test_start")
    login_user_id = request.user.id
    login_user_name = request.user.username
    logging.debug(login_user_id)
    logging.debug(login_user_name)
    
    form_SendAsset = SendAssetForm(request.POST or None)

    if request.method == 'POST':
        if form_SendAsset.is_valid():


            
            try:
                # RPC接続設定呼び出し
                logging.debug("test_connect_start")
                rpc_connection = rpcCon(login_user_name)
    
                req_assetid = request.POST.get('assetid')
                req_amounttosend = request.POST.get('amounttosend')
                req_addresstosend = request.POST.get('addresstosend')
                
                logging.debug(req_amounttosend)
                logging.debug(req_addresstosend)
                

                #walletinfo = rpc_connection.getwalletinfo(req_assetid)
                #assetbalance = walletinfo(['balance'])
                #logging.debug(assetbalance)

                logging.debug("20190121_3")
                
                txid = rpc_connection.sendtoaddress(req_addresstosend, req_amounttosend,"","",bool(0),req_assetid)
                logging.debug("20190121_4")
                
                result = rpc_connection.getwalletinfo(req_assetid)
                logging.debug(result['balance'])
                balance = result['balance']
                
                
                
            except JSONRPCException as json_exception:
                errJSONRPC = HttpResponse("A JSON RPC Exception occured: " + str(json_exception))
                messages.error(errJSONRPC)
            except Exception as general_exception:
                errHttp = HttpResponse("An Exception occured: " + str(general_exception))
                messages.error(errHttp)
            
            #data = HttpResponse(result, content_type='application/json; charset=UTF-8')
            data = HttpResponse(txid, content_type='application/json; charset=UTF-8')
            
            #data = result
            logging.debug("tt5555tt")
            logging.debug(data)
            #return data
            
            logging.debug("tttt2222")

            # save()メソッドを呼ぶだけでModelを使ってDBに登録される。
            obj = form_SendAsset.save(commit=False)
            obj.assetid = req_assetid
            obj.txid = txid
            obj.balance = balance
            obj.save()


            #created_at = ""
            # メッセージフレームワークを使い、処理が成功したことをユーザーに通知
            messages.success(request, '実行結果を表示します。')
            logging.debug('debug messages')
            logging.debug(request)
            #return redirect('issueasset:sendasset')
            
            page = _get_page(
                IssueAsset.objects.order_by('-id'),  # 投稿を新しい順に並び替えて取得する
                request.GET.get('page')  # GETクエリからページ番号を取得する
            )
            
            contexts = {
                'form': form_SendAsset,
                'page': page,
                'result': data,
                'txid': txid,
                'assetid': req_assetid,
                'addresstosend': req_addresstosend,
                'sent_at': obj.sent_at,
                'balance': obj.balance,
                'user_name': login_user_name,
            }
            return render(request, 'issueasset/sendasset.html', contexts)
            

        else:
            # メッセージフレームワークを使い、処理が失敗したことをユーザーに通知する
            messages.error(request, '入力内容に誤りがあります。')
    page = _get_page(
        IssueAsset.objects.order_by('-id'),  # 投稿を新しい順に並び替えて取得する
        request.GET.get('page')  # GETクエリからページ番号を取得する
    )
    

    contexts = {
        'form': form_SendAsset,
        'page': page,
        #'result': data,
        'user_name': login_user_name,
    }
    
    logging.debug("t1t1t1")
    
    return render(request, 'issueasset/sendasset.html', contexts )




# ********************************
# RPC接続設定
def rpcCon(login_user_name):
    
    logging.debug("test_connect")
    # elementsへの接続
    #inifile = ConfigParser.SafeConfigParser()
    #inifile.read('./config/config_1.ini')
    
    logging.debug("config読込")
    #logging.debug(inifile.get('elements_user', 'rpc_port'))
    
    #login_user_name = request.user.username
    logging.debug(login_user_name)
    user_no = login_user_name
    port = "rpc_port_" + str(user_no)
    
    logging.debug(port)
    
    logging.debug("config読込2")
    
    #elementsdir1のユーザ用
    #rpc_port = config.rpc_port_user1
    #rpc_user = config.rpc_user_user1
    #rpc_password = config.rpc_password_user1
    
    rpc_port = getattr(config,"rpc_port_" + str(user_no))
    rpc_user = getattr(config,"rpc_user_" + str(user_no))
    rpc_password = getattr(config,"rpc_password_" + str(user_no))
    
    logging.debug(rpc_port)
    logging.debug(rpc_user)
    logging.debug(rpc_password)
    
    #rpc_port = 18884
    #rpc_user = 'user1'
    #rpc_password = 'password1'


    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))

    return rpc_connection
        
        