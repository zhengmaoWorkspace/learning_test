# coding=utf-8

import time
from logging import Logger
from multiprocessing import Pool
from multiprocessing import Manager

import os
from bs4 import BeautifulSoup

import requests

logger = Logger("this")
MAX_WORKER_NUM = 3
WORKER_DATA = {}
RESULT_DATA = Manager().Queue()

URL_1 = "http://www.beianbeian.com/s-0/{}.html"
URL_2 = "http://icp.chinaz.com/{}"


def request(url):
    try:
        re = requests.get(url)
        result = re.content
        bf_soup = BeautifulSoup(result, 'html.parser', from_encoding='utf-8')
        return bf_soup
    except Exception as e:
        logger.warning(e)
        return None


def get_info(url):
    url_pro = URL_1.format(url)
    bf_soup = request(url_pro)
    if bf_soup is not None:
        t = bf_soup.find_all("tbody")[1]
        s = t.text.split("\n")[3]
        return s.strip()
    else:
        s = None
        return s


def get_info_bak(url):
    url_pro = URL_2.format(url)
    bf_soup = request(url_pro)
    t = bf_soup.find("div", class_="Tool-MainWrap wrapper pr").find_all("p")
    if len(t) > 5:
        s = t[5].next.string
    else:
        s = "未查询到相关数据"
        logger.warn(s)
    return s.strip()


def before():
    """
    从文件中加载需要查询的网址,并放入每个worker对应的队列里。
    :return:
    """
    index = 0
    inpath = "/Users/yexin/Desktop/untitled/domain.dat"
    try:
        with open(inpath) as r:
            line = r.readlines()
        for i in range(0, len(line)):
            current_queue = WORKER_DATA[i % MAX_WORKER_NUM]
            current_queue.put(line[i].strip('\n'))

        for current_queue in WORKER_DATA.values():
            current_queue.put(None)

    except Exception as e:
        logger.warning("读取输入文件失败，失败原因{}".format(e))


def hander(worker_id):
    """
    处理队列里的数据，将结果录入结果队列里
    :return:
    """
    print('正在运行的任务PID：%s' % os.getpid())
    start = time.time()

    while True:
        current_queue = WORKER_DATA[worker_id]
        data = current_queue.get()
        if data is None:
            print("finished")
            break
        result = get_info(data)
        if len(result) == 0:
            result = get_info_bak(data)
        print('%s gets data: %s, result: %s' % (worker_id, data, result))

    end = time.time()
    print('任务PID：%s，用时：%0.2f 秒' % (os.getpid(), (end - start)))


def _init_worker_data():
    # 为每一个worker进程分配自己的队列
    for i in range(0, MAX_WORKER_NUM):
        WORKER_DATA[i] = Manager().Queue()


def start_process_pool():
    _init_worker_data()
    pool = Pool(MAX_WORKER_NUM + 2)
    before()
    for i in range(0, MAX_WORKER_NUM):
        pool.apply_async(func=hander, args=(i,))

    pool.close()
    pool.join()


if __name__ == "__main__":
    start_process_pool()
