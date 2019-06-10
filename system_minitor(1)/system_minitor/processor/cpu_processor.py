# coding: utf-8
import psutil

from conf import config
from util.logger_util import logger

warning_message = "[warning]-[cpu]-[{}]-[{}]"


def get_info(host):
    """
    返回当前主机的cpu信息，对cpu的每个核心计算使用率
    :return: map
    """
    result = {}
    batch = config.minitor_map.get(host).get("batch")
    # cpu核数
    # 默认逻辑cpu核数，False查看真实cpu核数；
    cpu_list = psutil.cpu_percent(batch, True)
    index = 1
    for core in cpu_list:
        core_name = "core-{}".format(index)
        result[core_name] = core
        index = index + 1
    return result


def processor(host):
    """
    处理cpu的触发条件，生成告警信息
    :param host:
    :return:
    """
    result_info = get_info(host)
    trigger_threshold = config.minitor_map.get(host).get("trigger").get("cpu")
    for core in result_info:
        if result_info.get(core) > trigger_threshold:
            mess = warning_message.format(core, result_info.get(core))
            logger.warn(mess)
