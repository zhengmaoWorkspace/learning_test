# coding: utf-8
import json


class sample_json_util:
    def __init__(self, path):
        self.path = path
        self.dict = self.read_json_file()

    def read_json_file(self):
        """
        加载json配置文件，返回map
        :param path: json文件存放的路径
        :return:
        """
        load_dict = None
        with open(self.path, "r") as load_file:
            load_dict = json.load(load_file)
        return load_dict

    def get(self, key):
        return self.dict.get(key)
