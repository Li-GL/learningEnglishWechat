# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import requests
import os
import urllib
import urllib2
import json
from lxml import etree
import cookielib
import re
import random


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "lglfa888"  #
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # sha1加密算法

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        data = web.data()  # 获得post来的数据
        xml = etree.fromstring(data)  # 进行XML解析

        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text

        if msgType =="event":

            msg = xml.find('Event').text
            if msg =="subscribe":
                return self.render.reply_text(fromUser,toUser,int(time.time()), u"■ 发送中英文词组或单词即可获得相应的权威例句\n■ 随机返回6句，如果没有想要的，再发送一遍\n\
■ 支持正则输入，譬如：\n    1)  admit.*   匹配admit, admitted等。“.”匹配任意字符，“*”重复前面\n\
    2)  admit.*承认   匹配admit与承认有关的例句\n    3)  get \w*ed   匹配get married, get killed等; “\w”表任意英文字符")

        if msgType=="text":

            content = xml.find("Content").text  # 获得用户所输入的内容

            with open('Dictionaries.txt', 'r') as f:
                dic = f.readlines()

            readData = []
            for i in dic:
                with open(i.strip('\n'),'r') as d:
                    readData = readData + d.read()

                # 如果开头中文
                contentFinal = ' '.join(content.split()).encode('utf-8')
                if content[0] >= u'\u4e00' and content[0] <= u'\u9fa5':
                    
                    reExpre = "\n.{0,200}" + contentFinal + ".{0,300}\n"
                    self.replyData = re.findall(reExpre, readData)

            # 如果有大写优先大写，包含小写
                elif content[0] >= 'A' and content[0] <= 'Z':

                # 如果结尾中文，用在  admit.*承认 这样的正则输入，注意正则表达式 ".{0,300}\n" 比英文少了一个空格
                    if content[-1] >= u'\u4e00' and content[-1] <= u'\u9fa5':
                        reExpre = "\n.{0,200} " + contentFinal + ".{0,300}\n"
                        reExpre1 = "\n.{0,200} " + contentFinal.lower() + ".{0,300}\n"
                    else:
                        reExpre = "\n.{0,200} " + contentFinal + " .{0,300}\n"
                        reExpre1 = "\n.{0,200} " + contentFinal.lower() + " .{0,300}\n"
                    self.replyData = re.findall(reExpre, readData) + re.findall(reExpre1, readData)
                # 如果只有小写
                else:
                    # 如果结尾中文
                    if content[-1] >= u'\u4e00' and content[-1] <= u'\u9fa5':
                        reExpre = "\n.{0,200} " + contentFinal + ".{0,300}\n"
                    else:
                        reExpre = "\n.{0,200} " + contentFinal + " .{0,300}\n"
                    self.replyData = re.findall(reExpre, readData)

            ##################回复查找的内容##################
                if len(self.replyData)>=6:
                    break
                
            if self.replyData:
                random.shuffle(self.replyData)  # 随机化输出
                strip_str = '■'
                replies = [strip_str + "  " + re.sub('^■', '', i.strip('\n')) for i in self.replyData[:6]]
                reply_content = "\n\n".join(replies)
            else:
                reply_content = 'Sorry, your search didn\'t match any dictionaries'

            return self.render.reply_text(fromUser, toUser, int(time.time()), reply_content)
