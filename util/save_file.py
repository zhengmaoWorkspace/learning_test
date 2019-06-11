# coding=utf-8
import logging

logger = logging.getLogger()


def save_local(result_map):
    """
    保存结果到本地文件，供zabbix发送
    :param result_map:
    :return:
    """
    try:
        with open("monitor.dat", "w") as f:
            for key in result_map.keys():
                line = "{}    {}\n".format(key, result_map.get(key))
                f.writelines(line)
    except IOError as e:
        logger.error(e.message)
