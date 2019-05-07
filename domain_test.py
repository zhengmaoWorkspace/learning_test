#!/usr/bin/env python
# coding=utf-8
from unittest import TestCase
import requests
from multiprocessing import Pool, freeze_support, Manager
from domain_analysis import before, start_process_pool, get_info_bak
from domain_analysis import get_info
class TestParseDomain(TestCase):

    def test_before(self):
        work_que = Manager().Queue()
        before(work_que)

    def test_get_info(self):
        url = "www.taobao.com"
        result = get_info(url)
        self.assertEquals(result, u"浙江淘宝网络有限公司")

    def test_get_bak(self):
        url = "www.taobao.com"
        result = get_info_bak(url)
        self.assertEquals(result, u"浙江淘宝网络有限公司")

    def test_pool(self):
        start_process_pool()


