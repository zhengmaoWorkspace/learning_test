#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging


def request_name(url, file_name_map):
    """
    解析url的标题
    :param url:
    :return:
    """
    name = file_name_map.get(url)
    if name is not None:
        return name
    else:
        behind_name = os.path.splitext(url)[-1]
        if behind_name == ".html":
            host = "http://200.200.1.35{}"
            content = requests.get(host.format(url)).content
            bs = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
            name = bs.find("head").find("title").string
            file_name_map[url] = unicode(name)
            return unicode(name)
        else:
            name = os.path.splitext(url)[0].split("/")[-1]
            file_name_map[url] = unicode(name)
            return unicode(name)


def load_data(path):
    """
    pandas读取日志文件
    :param path: 日志文件存放目录
    :return:
    """
    try:
        df = pd.read_table(path, sep=" ", header=None)
        df.columns = ["ip_addr", "del1", "del2", "time", "asser", "desc", "code", "count"]
        df = df.drop(["del1", "del2"], axis=1)
        return df
    except Exception as e:
        logging.warning("日志文件读取失败，程序退出！失败原因：{}".format(e))
        sys.exit(0)


def desc_processor(df):
    """
    处理desc字段，按照空格分割，分裂为多种列
    :param df: 原始dataFramde
    :return: split desc字段后的dataFram
    """
    try:
        names = df["desc"].str.split(" ", expand=True)
        names.columns = ["request_method", "source_page", "http"]
        df = df.join(names)
        df = df.drop(["desc"], axis=1)
        df["time"] = df["time"].str.replace("[", "")
        df["asser"] = df["asser"].str.replace("]", "")
        return df
    except IndexError as e:
        logging.warning(e.message)


def fileter_record(record):
    """
    过滤文件的后缀名，只取".html", ".htm", ".pdf", ".doc", ".docx", ".mpg"
    :param record: 原始文件记录
    :return: 布尔值，判断是否需要过滤
    """
    name = os.path.splitext(record)[-1]
    if name not in [".css", ".js"] and name in [".html", ".htm", ".pdf", ".doc", ".docx", ".mpg"]:
        return True
    else:
        return False


def pv_table(df, path, file_name_map):
    """
    文章报表
    :param df:
    :return:
    """
    path = path + u"\\文章报表.csv"
    # 计算pv值
    pv = df["source_page"].value_counts()
    # 计算访问IP数
    uv = df.groupby(["source_page"])[["ip_addr"]].nunique()
    uv["URL"] = uv.index
    # 计算文章标题
    result = pd.concat([pv, uv], axis=1, sort=False)
    result["file_name"] = uv["URL"].apply(lambda x: request_name(x, file_name_map))
    result.columns = ["访问人次", "访问IP数", "URL", "文章标题"]
    result = result[["URL", "文章标题", "访问人次", "访问IP数"]]
    save_csv(result, path)


def ip_table(df, path):
    """
    IP报表
    :param df:
    :return:
    """
    path = path + u"\\IP报表.csv"
    # 计算每种IP的访问次数
    # IP-访问次数
    uv = df["ip_addr"].value_counts()
    # 访问文章数
    files = df.groupby(["ip_addr"])[["source_page"]].nunique()
    result = pd.concat([files, uv], axis=1, sort=False)
    result["IP"] = result.index
    result.columns = ["访问文章数", "访问次数", "IP"]
    result = result[["IP", "访问次数", "访问文章数"]]
    save_csv(result, path)


def wide_table(df, path):
    """
    生成完整的宽表
    :param df:
    :return:
    """
    path = path + u"\\完整报表.csv"
    result = df.groupby(["ip_addr", "source_page"], as_index=False)["count"].count()
    result.columns = ["IP", "URL", "访问次数"]
    save_csv(result, path)


def data_frame_get(path):
    """
    处理日志文件，生成完整的宽表
    :return:
    """

    df = load_data(path)
    df = desc_processor(df)
    df = df[df["source_page"].apply(lambda x: fileter_record(x))]
    return df


def save_csv(df, path):
    """
    保存文件到path目录下
    :param df:
    :param path:
    :return:
    """
    df.to_csv(path, index=False, encoding="utf-8")


def get_file_name_map():
    """
    加载缓存数据
    :return:
    """
    config_path = "./config/map.json"
    try:
        with open(config_path, "r") as f:
            result = f.readlines()
        file_name_map = json.loads(result[0])
    except IOError as e:
        file_name_map = json.loads("{}")
        logging.warning("缓存文件读取失败，请检查！失败原因：{}".format(e))
    return file_name_map


def update_file_map(file_name_map):
    """
    保存当前解析的标题缓存的map到config/map.json
    :return:
    """
    result = json.dumps(file_name_map)
    with open("./config/map.json", "w") as f:
        f.writelines(result)


def processor():
    work_path = os.path.abspath('.')
    data_path = "{}\\data\\data.txt".format(work_path)
    save_path = "{}\\data".format(work_path)
    df = data_frame_get(data_path)
    file_name_map = get_file_name_map()
    pv_table(df, save_path, file_name_map)
    ip_table(df, save_path)
    wide_table(df, save_path)


if __name__ == "__main__":
    processor()
