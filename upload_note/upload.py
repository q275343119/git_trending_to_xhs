import json
from datetime import datetime
from http import cookies

import requests
from xhs import XhsClient

from config import config_settings
from utils.logging_util import logger


def beauty_print(data: dict):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def sign(uri, data=None, a1="", web_session=""):
    """
    签名函数
    :param uri:
    :param data:
    :param a1:
    :param web_session:
    :return:
    """
    # 填写自己的 flask 签名服务端口地址
    res = requests.post(config_settings.url_sign_sign,
                        json={"uri": uri, "data": data, "a1": a1, "web_session": web_session})
    signs = res.json()
    return {
        "x-s": signs["x-s"],
        "x-t": signs["x-t"]
    }


def get_a1():
    """
    获取a1
    :return:
    """
    logger.info("获取a1")
    url_a1 = config_settings.url_sign_a1
    response = requests.get(url_a1)

    if response.status_code == 200:
        return response.json()["a1"]
    logger.error(response.text)
    raise ValueError("获取a1失败")


def get_cookies():
    """
    获取cookies
    :return:
    """
    logger.info("获取cookies")
    c = cookies.SimpleCookie()
    c.load(config_settings.cookies)

    c["a1"] = get_a1()
    str_cookies = ""
    for morsel in c.values():
        str_cookies += f"{str(morsel.key)}={str(morsel.value)};"
    return str_cookies


def upload_note():
    """
    上传笔记
    :return:
    """
    now = datetime.now()
    cookie = get_cookies()
    logger.info("实例化客户端")
    xhs_client = XhsClient(cookie, sign=sign)

    title = f"📅 {now.strftime('%Y-%m-%d')} | GitHub Python | 趋势✨"
    logger.info("准备上传笔记")

    with open(f"{config_settings.download_dir}/{now.strftime('%Y%m%d')}/xhs_note.txt", "r", encoding='utf-8') as f:
        desc = f.read()
    desc += f"\n#github宝藏项目[话题]# #Python[话题]# #github[话题]#"
    images = [
        f"{config_settings.download_dir}/{now.strftime('%Y%m%d')}/TrendingProjects.png",
    ]
    topics = [
        {
            "id": "63d293be00000000010012d0",
            "name": "github宝藏项目",
            "link": "",
            "type": "topic"
        },
        {
            "id": "5d35dd9b000000000e0088dc",
            "name": "Python",
            "link": "",
            "type": "topic"
        },
        {
            "id": "61be006c0000000001005c3f",
            "name": "github",
            "link": "",
            "type": "topic"
        }
    ]
    note = xhs_client.create_image_note(title, desc, images, topics=topics)
    beauty_print(note)
    logger.info("上传完毕")


if __name__ == '__main__':
    upload_note()
