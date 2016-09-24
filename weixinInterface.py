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
        str_xml = web.data()  # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        content = xml.find("Content").text  # 获得用户所输入的内容
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text

        content1 = content.split()
        content2 = ''
        for m in content1:
            content2 = content2 + m + ' '
        # 柯林斯英汉词典
        f = open('En-Ch CollinsCOBUILD.txt', 'r')
        readdata = f.read()

        # 微信发来的content为unicode
        content_u = content
        # 判断中英文
        if content_u[0] >= u'\u4e00' and content_u[0] <= u'\u9fa5':
            content_8 = content_u.encode('utf-8')
            reExpre = "\n.{2,100}" + content_8 + ".{0,200}\n"
            allApes = re.findall(reExpre, readdata)
        # 有大写优先大写，包含小写
        elif content_u[0] >= 'A' and content_u[0] <= 'Z':
            reExpre = "\n.{0,100} " + content2 + ".{0,200}\n"
            reExpre1 = "\n.{0,100} " + content2.lower() + ".{0,200}\n"
            allApes = re.findall(reExpre, readdata) + re.findall(reExpre1, readdata)
        else:
            reExpre = "\n.{0,100} " + content2 + ".{0,200}\n"
            allApes = re.findall(reExpre, readdata)

        # 回复查找的内容
        strip_str = u'■'.encode('utf-8')
        if len(allApes) > 0:
            j = 1
            reply_content = ""
            for i in allApes:
                if i[1:4] == strip_str:
                    reply_content = reply_content + strip_str + "  " + i.strip('\n').strip(strip_str) + '\n\n'
                    j += 1
                else:
                    reply_content = reply_content + strip_str + "  " + i.strip('\n') + '\n\n'
                    j += 1
                if j > 6:
                    break
        else:
            reply_content = 'Sorry, your search didn\'t match any dictionaries'

        return self.render.reply_text(fromUser, toUser, int(time.time()), reply_content)

