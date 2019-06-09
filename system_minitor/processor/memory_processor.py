# coding: utf-8

import psutil


def processor():
    result = {}
    # 查看内存信息；
    mem = psutil.virtual_memory()
    result["mem_total"] = "{} GB".format(int(mem.total / 1024 / 1024))
    result["mem_available"] = "{} GB".format(int(mem.available / 1024 / 1024))
    result["mem_per"] = mem.percent
    return result
