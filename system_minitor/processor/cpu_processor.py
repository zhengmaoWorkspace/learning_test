# coding: utf-8
import psutil
from util.sample_json_util import sample_json_util


def processor():
    """
    返回当前主机的cpu信息，对cpu的每个核心计算使用率
    :return: map
    """
    result = {}
    conf_path = "/Users/yexin/Desktop/MyGit/learning_test/system_minitor/conf/conf.json"
    json_util = sample_json_util(conf_path)
    batch = json_util.get("Local").get("batch")
    # cpu核数
    # 默认逻辑cpu核数，False查看真实cpu核数；
    cpu_list = psutil.cpu_percent(batch, True)
    index = 1
    for core in cpu_list:
        core_name = "core-{}".format(index)
        result[core_name] = core
        index = index + 1
    return result
