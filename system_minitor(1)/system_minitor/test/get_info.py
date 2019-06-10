# coding: utf-8
import psutil, time
from operator import itemgetter, attrgetter

def cpu():
    # cpu核数
    # 默认逻辑cpu核数，False查看真实cpu核数；
    cpu = psutil.cpu_count(False)
    cpu_per = int(psutil.cpu_percent(1))  # 每秒cpu使用率，（1，True） 每一核cpu的每秒使用率；
    print(cpu)
    print(cpu_per)
    print(psutil.cpu_percent(1, True))


if __name__ == '__main__':
    cpu()