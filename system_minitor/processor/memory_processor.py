# coding: utf-8

import psutil
from conf import config
from util.logger_util import logger


def get_info():
    result = {}
    # 查看内存信息；
    try:
        mem = psutil.virtual_memory()
        result["mem_total"] = "{} GB".format(int(mem.total / 1024 / 1024))
        result["mem_available"] = "{} GB".format(int(mem.available / 1024 / 1024))
        result["mem_per"] = mem.percent
    except Exception as e:
        logger.warn(e.message)
    return result


def processor(host):
    """
    处理内存信息的触发条件，满足条件即增加告警信息
    :param host:
    :return:
    """
    result = "[warning]-[memory]-[mem_per]-[{}%]\n"
    result_info = get_info()
    try:
        trigger_threshold = config.minitor_map.get(host).get("trigger").get("memory")
        term_info = result_info.get("mem_per")
        if term_info > trigger_threshold:
            result = result.format(term_info)
    except Exception as e:
        logger.warn("无法加载触发器条件，失败原因：{}".format(e))
    return result
