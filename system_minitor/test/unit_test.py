from unittest import TestCase
from conf import config
from processor import base_processor
from run.main import host_processor


class test(TestCase):
    def test_config(self):
        mail_theam = config.mail_theam
        self.assertEquals(mail_theam, "Monitor Notes")

    def test_base_processor(self):
        term = "cpu"
        host = "Local"
        result = base_processor.processor(term, host)
        self.assertIsInstance(result, basestring)
        term = "memory"
        host = "Local"
        result = base_processor.processor(term, host)
        self.assertIsInstance(result, basestring)

    def test_host_processor(self):
        mess = host_processor()
