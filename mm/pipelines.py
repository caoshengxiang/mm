# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import requests


class MmPipeline(object):
    # def __init__(self, IMAGES_STORE):
    #     self.IMAGES_STORE = IMAGES_STORE

    def process_item(self, item, spider):
        fold_name = item['name']
        url = item['poster']
        req = requests.get(url)
        logging.debug(req.content)

        binfile = open(url, 'wb')
        binfile.write(req.content)
        binfile.close()

        return item
