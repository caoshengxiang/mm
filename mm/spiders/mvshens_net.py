# -*- coding: utf-8 -*-
import requests
import scrapy
from pyquery import PyQuery as pq
import logging
from mm.items import MmItem
from scrapy import FormRequest, Request


class MvshensNetSpider(scrapy.Spider):
    name = 'mvshens_net'
    allowed_domains = ['https://www.nvshens.net']
    start_urls = ['https://www.nvshens.net/rank/sum/']

    def parse(self, response):
        doc = pq(response.text)
        logging.info('https://www.nvshens.net 开始解析列表')
        ranklis = doc('#post').find('.rankli')
        for li in ranklis.items():
            href = self.allowed_domains[0] + li.find('div.rankli_imgdiv > a').attr('href')
            logging.info('连接地址{}'.format(href))
            yield Request(url=href,
                          dont_filter=True,
                          method='GET',
                          meta={
                              # 'ROUTE_PARENT': ROUTE_PARENT
                          },
                          # headers=self.headers,
                          callback=self.list_detail)

    def list_detail(self, response):
        doc = pq(response.text)
        baseHtml = doc('#post > div:nth-child(2) > div')
        name = baseHtml.find('div.div_h1 > h1').text()
        poster = baseHtml.find('div.infoleft_imgdiv > a > img').attr('src')
        # logging.info('{}-{}'.format(name, poster))
        # mmItem = MmItem()
        # mmItem['name'] = name
        # mmItem['poster'] = poster
        # yield mmItem
        self.downImg(poster, name)

    def downImg(self, poster, name):
        dir_path = 'imgs'
        self.mkdir(dir_path)
        group = '{}/{}'.format(dir_path, name)
        self.mkdir(group)
        req = requests.get(poster)
        binFile = open('{}/{}.jpg'.format(group, name), 'wb')
        binFile.write(req.content)
        binFile.close()

    @staticmethod
    def mkdir(path):
        # 引入模块
        import os

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)

            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False
