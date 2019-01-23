
# -*- coding: UTF-8 -*-

import requests
import json
import datetime
import random
import asyncio;

from tools.jsonTools import JSONObject;
from tools.shellTools import execCmd;

#参与用户组
gamePlayer=[]
# 撸羊毛账户组
haoUsers = ['rbvfagli1qco']
# api节点
apiNode = "https://bos.api.blockgo.vip";
# 系统资产符号
symbol = "BOS";
# 休眠时间
sleepCount = 5;
# 是否可以第一个投注，默认不投
isFirst = False
# 投注随机范围
max = 1




def getTable():
    params = '{"json":true,"code":"bitthirtymax","table":"player","scope":"bitthirtymax","lower_bound":null,"upper_bound":null,"limit":100}'
    uri = "{apiNode}/v1/chain/get_table_rows".format(apiNode=apiNode)
    try:
        contents = requests.get(uri, data=params, timeout=10)
        if (contents.status_code == 200):
            if 'rows' in str(contents.content):
                palyerJson = json.loads(contents.text, object_hook=JSONObject)
                all_player = palyerJson.rows.__len__()
                print(palyerJson.rows.__len__())
                if palyerJson.rows.__len__() > 0:
                    for i in range(0, palyerJson.rows.__len__()):
                        gamePlayer.append(palyerJson.rows[i].owner)

    except Exception as e:
        print(e)


def checkStatus():
    params = '{"json":true,"code":"bitthirtymax","table":"globalstate","scope":"bitthirtymax","lower_bound":null,"upper_bound":null,"limit":2}'
    uri = "{apiNode}/v1/chain/get_table_rows".format(apiNode=apiNode)
    try:
        contents = requests.get(uri, data=params, timeout=5)
        if (contents.status_code == 200):
            if 'rows' in str(contents.content):
                palyerJson = json.loads(contents.text, object_hook=JSONObject)
                if palyerJson.rows.__len__() > 0:
                    print(contents.content)
                    if (palyerJson.rows[0].status == 1 or palyerJson.rows[0].status == 4):
                        return True;
                    else:
                        if palyerJson.rows[0].status == 3:
                            print("系统正在开奖中，不能投注！")
                            return False;
                        else:
                            betTime = palyerJson.rows[0].wait_time;
                            print("开奖等待时间{betTime}".format(betTime=betTime))
                            nowTime = (datetime.datetime.now() + datetime.timedelta(hours=-8)).strftime(
                                "%Y-%m-%dT%H:%M:%S")
                            if (betTime < nowTime):
                                print("当前时间大于系统开奖时间，不投注！")
                                return False;
                            else:
                                return True;
        else:
            print("暂时未取到链上数据，不投注！")
            return False

    except Exception as e:
        print(e)
        print("发生未知错误，不投注！")
        return False


def doMiniGame_30max():
    try:
        if (haoUsers.__len__() > 0):
            idx = random.randrange(0, haoUsers.__len__());
            betAccount = haoUsers[idx]
            t = '36743e2f322fcebe16876d5bddb37e61bc8f14772c715fa429a0f569cb2f779c36743e2f322fcebe16876d5bddb37e61bc8f14772c715fa429a0f569cb2f779c36743e2f322fcebe16876d5bddb37e61bc8f14772c715fa429a';
            memo = random.sample(t, 64)
            memoValue = ""
            for i in memo:
                memoValue += i
            token = round(random.uniform(1, int(max)), 1);
            commandTrans = 'cleos -u {apiNode} transfer {user} bitthirtymax "{token} {symbol}" "mg:{memo}"'.format(
                apiNode=apiNode, user=betAccount, token=str(token), symbol=symbol, memo=memoValue);
            commandReturn = execCmd(commandTrans)
            print(commandReturn)
        else:
            print("不添加账户怎么薅羊毛呢")
    except  Exception as e:
        print(e)
        pass


def run():
    gamePlayer=[]
    getTable();
    if haoUsers.__len__()>1:
        for i in haoUsers:
            if i not in gamePlayer:
                if checkStatus():
                    doMiniGame_30max()
            else:
                print("已经投注，不再投注")
    else:
        if haoUsers[0]  not in gamePlayer:
            if checkStatus():
                doMiniGame_30max()
        else:
            print("已经投注，不再投注")

