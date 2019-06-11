# coding=utf-8
import time

from conf import config
from processor import base_processor
from util.note_util import send_message


def host_processor():
    message = config.mess
    for host in config.minitor_map:
        # 获取指定主机列表及对应的监控列表
        info_map = config.minitor_map.get(host)
        term_list = info_map.get("items")
        # 对每个监控项进行触发条件判断
        for term in term_list:
            result = base_processor.processor(term, host)
            message = message + result
    return message


if __name__ == '__main__':
    while True:
        mess = host_processor()
        send_message(config.mail_addr, config.mail_theam, mess)
        time.sleep(config.batch_time)