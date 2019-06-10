# coding=utf-8
from conf import config
from util.logger_util import logger


if __name__ == '__main__':

    for host in config.minitor_map:
        info_map = config.minitor_map.get(host)
        term_list = info_map.get("items")
        for term in term_list:
            model_name = "processor.{}_processor".format(term)
            model = __import__(model_name, fromlist=True)
            func = getattr(model, "processor", None)
            result = func(host)
            logger.info(result)