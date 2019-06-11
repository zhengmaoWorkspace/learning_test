# coding: utf-8
from util.logger_util import logger


def processor(term, host):
    """
    通用处理器
    :param term: 监控项
    :param host: 监控主机
    :return:
    """
    result = None
    model_name = "processor.{}_processor".format(term)
    try:
        model = __import__(model_name, fromlist=True)
        func = getattr(model, "processor", None)
        result = func(host)
    except Exception as e:
        logger.warning(e)
    return result
