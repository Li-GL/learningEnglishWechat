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


        # ------------------------------先用这两个词典，保证回复速度--------------------------------#
        # 柯林斯英汉词典
        with open('En-Ch CollinsCOBUILD.txt', 'r') as f:
            readdata = f.read()
        #剑桥高阶
        with open('En-Ch_Cambridge_Advanced_Learner_Dictionary.txt', 'r') as f1:
            readdata1 = f1.read()

        ##################正则判断，检索##################
        contentFinal = ' '.join(content.split())

        # 如果开头中文
        if content[0] >= u'\u4e00' and content[0] <= u'\u9fa5':
            contentUTF_8 = content.encode('utf-8')
            reExpre = "\n.{0,100}" + contentUTF_8 + ".{0,200}\n"
            allApes = re.findall(reExpre, readdata)+re.findall(reExpre, readdata1)

        # 如果有大写优先大写，包含小写
        elif content[0] >= 'A' and content[0] <= 'Z':

            # 如果结尾中文，用在  admit.*承认 这样的正则输入，注意正则表达式 ".{0,300}\n" 比英文少了一个空格
            if contentFinal[-1] >= u'\u4e00' and contentFinal[-1] <= u'\u9fa5':
                contentUTF_8 = contentFinal.encode('utf-8')
                reExpre = "\n.{0,200} " + contentUTF_8 + ".{0,300}\n"
                reExpre1 = "\n.{0,200} " + contentUTF_8.lower() + ".{0,300}\n"
            else:
                reExpre = "\n.{0,200} " + contentFinal + " .{0,300}\n"
                reExpre1 = "\n.{0,200} " + contentFinal.lower() + " .{0,300}\n"
            allApes = re.findall(reExpre, readdata) + re.findall(reExpre, readdata1) \
                      +re.findall(reExpre1, readdata) + re.findall(reExpre1, readdata1)
        # 如果只有小写
        else:
            # 如果结尾中文
            if contentFinal[-1] >= u'\u4e00' and contentFinal[-1] <= u'\u9fa5':
                contentUTF_8 = contentFinal.encode('utf-8')
                reExpre = "\n.{0,200} " + contentUTF_8 + ".{0,300}\n"
            else:
                reExpre = "\n.{0,200} " + contentFinal + " .{0,300}\n"

            #检索结果
            allApes = re.findall(reExpre, readdata)+re.findall(reExpre, readdata1)

        ##################回复查找的内容##################
        if len(allApes)>=6:
            random.shuffle(allApes)  # 随机化输出
            strip_str = '■'
            replies = [strip_str + "  " + re.sub('^■', '', i.strip('\n')) for i in allApes[:6]]
            reply_content = "\n\n".join(replies)


        #------------------------------如果上面字典搜的例句太少或没有，继续搜两个字典--------------------------------#
        else:
            # 牛津英汉词典
            with open('En-Ch_Oxford_Advanced_Leaner_Dictionary.txt', 'r') as f2:
                readdata2 = f2.read()
            # 朗曼
            with open('En-Ch_Longman_Dictionary_of_Contemporary_English.txt', 'r') as f3:
                readdata3 = f3.read()

            ##################正则判断，检索##################
            contentFinal = ' '.join(content.split())
            # 如果开头中文
            if content[0] >= u'\u4e00' and content[0] <= u'\u9fa5':
                contentUTF_8 = content.encode('utf-8')
                reExpre = "\n.{0,100}" + contentUTF_8 + ".{0,200}\n"
                allApes2 = re.findall(reExpre, readdata2) + re.findall(reExpre, readdata3)

            # 如果有大写优先大写，包含小写
            elif content[0] >= 'A' and content[0] <= 'Z':

                # 如果结尾中文，用在  admit.*承认 这样的正则输入，注意正则表达式 ".{0,300}\n" 比英文少了一个空格
                if contentFinal[-1] >= u'\u4e00' and contentFinal[-1] <= u'\u9fa5':
                    contentUTF_8 = contentFinal.encode('utf-8')
                    reExpre = "\n.{0,200} " + contentUTF_8 + ".{0,300}\n"
                    reExpre1 = "\n.{0,200} " + contentUTF_8.lower() + ".{0,300}\n"
                else:
                    reExpre = "\n.{0,200} " + contentFinal + " .{0,300}\n"
                    reExpre1 = "\n.{0,200} " + contentFinal.lower() + " .{0,300}\n"
                allApes2 = re.findall(reExpre, readdata2) + re.findall(reExpre, readdata3) \
                           + re.findall(reExpre1, readdata2) + re.findall(reExpre1, readdata3)
            #如果只有小写
            else:
                # 如果结尾中文
                if contentFinal[-1] >= u'\u4e00' and contentFinal[-1] <= u'\u9fa5':
                    contentUTF_8 = contentFinal.encode('utf-8')
                    reExpre = "\n.{0,200} " + contentUTF_8 + ".{0,300}\n"
                else:
                    reExpre = "\n.{0,200} " + contentFinal + " .{0,300}\n"
                # 检索结果
                allApes2 = re.findall(reExpre, readdata2) + re.findall(reExpre, readdata3)

            # 合并检索结果
            allApes = allApes+allApes2

            ##################回复查找的内容##################
            if allApes:

                random.shuffle(allApes)  # 随机化输出
                strip_str = '■'
                replies = [strip_str + "  " + re.sub('^■', '', i.strip('\n')) for i in allApes[:6]]
                reply_content = "\n\n".join(replies)

            else:
                reply_content = 'Sorry, your search didn\'t match any dictionaries'

        return self.render.reply_text(fromUser, toUser, int(time.time()), reply_content)
