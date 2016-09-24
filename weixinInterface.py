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

        # 柯林斯英汉词典
        with open('En-Ch CollinsCOBUILD.txt', 'r') as f:
            readdata = f.read()
        #牛津英汉词典
        # with open('En-Ch_Oxford_Advanced_Leaner_Dictionary.txt', 'r') as f1:
        #     readdata1 = f1.read()
        #朗曼
        # with open('En-Ch_Longman_Dictionary_of_Contemporary_English.txt', 'r') as f2:
        #     readdata2 = f2.read()
        #剑桥
        with open('En-Ch_Cambridge_Advanced_Learner_Dictionary.txt', 'r') as f3:
            readdata3 = f3.read()

        # 微信发来的content为unicode
        content2 = ' '.join(content.split())
        # 判断中英文
        if content[0] >= u'\u4e00' and content[0] <= u'\u9fa5':
            content_8 = content.encode('utf-8')
            reExpre = "\n.{0,100}" + content_8 + ".{0,200}\n"
            allApes = re.findall(reExpre, readdata)+re.findall(reExpre, readdata3)

        # 有大写优先大写，包含小写
        elif content[0] >= 'A' and content[0] <= 'Z':
            reExpre = "\n.{0,200} " + content2 + " .{0,300}\n"
            reExpre1 = "\n.{0,200} " + content2.lower() + ".{0,300}\n"
            allApes = re.findall(reExpre, readdata) + re.findall(reExpre, readdata3) \
                      +re.findall(reExpre1, readdata) + re.findall(reExpre1, readdata3)
        else:
            reExpre = "\n.{0,200} " + content2 + " .{0,300}\n"
            allApes = re.findall(reExpre, readdata)+re.findall(reExpre, readdata3)

        # 回复查找的内容
        if len(allApes)>=6:
            strip_str = u'■'.encode('utf-8')
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
        ##############################加上另外两个字典
        else:
            # 牛津英汉词典
            with open('En-Ch_Oxford_Advanced_Leaner_Dictionary.txt', 'r') as f1:
                readdata1 = f1.read()
            # 朗曼
            with open('En-Ch_Longman_Dictionary_of_Contemporary_English.txt', 'r') as f2:
                readdata2 = f2.read()

             ###############################跟上面一样的处理
            content2 = ' '.join(content.split())
            # 判断中英文
            if content[0] >= u'\u4e00' and content[0] <= u'\u9fa5':
                content_8 = content.encode('utf-8')
                reExpre = "\n.{0,100}" + content_8 + ".{0,200}\n"
                allApes2 = re.findall(reExpre, readdata1) + re.findall(reExpre, readdata2)

            # 有大写优先大写，包含小写
            elif content[0] >= 'A' and content[0] <= 'Z':
                reExpre = "\n.{0,200} " + content2 + " .{0,300}\n"
                reExpre1 = "\n.{0,200} " + content2.lower() + " .{0,300}\n"
                allApes2 = re.findall(reExpre, readdata1) + re.findall(reExpre, readdata2) \
                           + re.findall(reExpre1, readdata1) + re.findall(reExpre1, readdata2)
            else:
                reExpre = "\n.{0,200} " + content2 + " .{0,300}\n"
                allApes2 = re.findall(reExpre, readdata1) + re.findall(reExpre, readdata2)
            allApes = allApes+allApes2
            if allApes:
                strip_str = u'■'.encode('utf-8')
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
