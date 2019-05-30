# coding=utf-8

import time
import logging
from multiprocessing import Pool
from multiprocessing import Manager
from config import URL_1
from config import URL_2
import os
from bs4 import BeautifulSoup
import requests
import config


def request(url):
    """
    爬取指定url内容
    :param url:
    :return: bs4对象
    """
    try:
        re = requests.get(url)
        result = re.content
        bf_soup = BeautifulSoup(result, 'html.parser', from_encoding='utf-8')
        return bf_soup
    except Exception as e:
        logging.warning(e)
        return None


def get_info(url):
    """
    定制beianbeian网址查询到的内容
    :param url:
    :return:
    """
    url_pro = URL_1.format(url)
    bf_soup = request(url_pro)
    result = None
    if bf_soup is not None:
        try:
            tbody = bf_soup.find_all("tbody")[1]
            result = tbody.text.split("\n")[3]
            return result.strip()
        except IndexError as e:
            logging.warn("bs4解析时越界！{}".format(e.message))
        except Exception as e:
            logging.warn("bs4解析异常！异常原因:{}".format(e.message))
    else:
        return result


def get_info_bak(url):
    """
    定制化解析，解析chinaz网站的查询内容
    :param url:
    :return:
    """
    url_pro = URL_2.format(url)
    bf_soup = request(url_pro)
    div = bf_soup.find("div", class_="Tool-MainWrap wrapper pr").find_all("p")
    if len(div) > 5:
        s = div[5].next.string
    else:
        s = "未查询到相关数据"
        logging.warn(s)
    return s.strip()


def before(worker_data):
    """
    从文件中加载需要查询的网址,并放入每个worker对应的队列里。
    :return:
    """
    in_path = config.INPATH
    try:
        with open(in_path) as r:
            line = r.readlines()
        for i in range(0, len(line)):
            work_num = config.MAX_WORKER_NUM
            current_queue = worker_data[i % work_num]
            current_queue.put(line[i].strip('\n'))

        for current_queue in worker_data.values():
            current_queue.put(None)

    except Exception as e:
        logging.warning("读取输入文件失败，失败原因{}".format(e))


def hander(worker_id, worker_data):
    """
    处理队列里的数据，将结果录入结果队列里
    :return:
    """
    print('正在运行的任务PID：%s' % os.getpid())
    start = time.time()

    while True:
        current_queue = worker_data[worker_id]
        data = current_queue.get()
        if data is None:
            logging.info("finished")
            break
        result = get_info(data)
        if len(result) == 0:
            result = get_info_bak(data)
        print('%s gets data: %s, result: %s' % (worker_id, data, result))

    end = time.time()
    print('任务PID：%s，用时：%0.2f 秒' % (os.getpid(), (end - start)))


def _init_worker_data():
    # 为每一个worker进程分配自己的队列
    worker_data = {}
    work_num = config.MAX_WORKER_NUM
    try:
        for i in range(0, work_num):
            worker_data[i] = Manager().Queue()
    except Exception as e:
        logging.warn("Manager().Queue()初始化失败！")
        raise RuntimeError("Manager().Queue()初始化失败！")
    return worker_data


def start_process_pool():
    """
    开始执行处理进程
    :return:
    """

    worker_data = _init_worker_data()
    before(worker_data)

    work_num = config.MAX_WORKER_NUM
    pool = Pool(work_num + 2)
    for i in range(0, work_num):
        pool.apply_async(func=hander, args=(i, worker_data,))
    pool.close()
    pool.join()


if __name__ == "__main__":
    start_process_pool()
