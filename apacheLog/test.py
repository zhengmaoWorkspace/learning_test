#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from unittest import TestCase
from apache_log_analysis import request_name
from apache_log_analysis import load_data
from apache_log_analysis import desc_processor
from apache_log_analysis import fileter_record
from apache_log_analysis import processor
import pandas as pd
class TestAnalyse(TestCase):
    def test_request_name(self):
        file_name_map = json.loads("{}")
        title = request_name("/coding/miniproject/material.html", file_name_map)
        self.assertEquals(title, u"培训素材 · 编码上手包")

    def test_load_data(self):
        path = "E:\Work\Python\\20190211\\test\data\data.txt"
        df1 = load_data(path)
        self.assertIsInstance(df1, pd.DataFrame)

    def test_desc_processor(self):
        path = "E:\Work\Python\\20190211\\test\data\data.txt"
        df1 = load_data(path)
        df2 = desc_processor(df1)
        self.assertIsInstance(df2, pd.DataFrame)

    def test_fileter_record(self):
        a = "/root/sd/fg/demo.txt"
        b = "/root/sd/fg/demo.html"
        test1 = fileter_record(a)
        test2 = fileter_record(b)
        self.assertEquals(test1, False)
        self.assertEquals(test2, True)

    def test_processor(self):
        processor()


