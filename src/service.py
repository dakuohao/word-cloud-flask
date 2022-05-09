import base64
import os
import uuid
from collections import Counter
from os import path

import jieba
import numpy as np
import requests
from PIL import Image
from flask import Response, jsonify
from wordcloud import WordCloud

# 资源路径
dirPath = "res/"


def download(dir, url):
    fileName = path.basename(url)
    filePath = dirPath + dir + "/" + fileName
    if not path.exists(filePath):
        print("下载文件，路径：%s ，url：%s" % (filePath, url))
        r = requests.get(url)
        with open(filePath, "wb") as file:
            file.write(r.content)
    return filePath


def wordCloudImage(conf,id):
    ### 入参校验
    errMsg = []
    if "font" not in conf:
        errMsg.append("font 不能为空")
    if "mask" not in conf:
        errMsg.append("mask 不能为空")
    if "background_color" not in conf:
        errMsg.append("background_color 不能为空")
    if "prefer_horizontal" not in conf:
        errMsg.append("prefer_horizontal 不能为空")
    if "width" not in conf:
        errMsg.append("width 不能为空")
    if "height" not in conf:
        errMsg.append("height 不能为空")
    if "colormap" not in conf:
        errMsg.append("colormap 不能为空")
    if len(errMsg) > 0:
        return Response(errMsg)

    ### 常量定义
    font = download("font", conf["font"])
    background_color = conf["background_color"]
    mask = download("mask", conf["mask"])
    mask_image = np.array(Image.open(path.join(path.dirname(__file__), mask)))
    prefer_horizontal = conf["prefer_horizontal"]
    width = conf["width"]
    height = conf["height"]
    colormap = conf["colormap"]
    wordList = conf["wordList"]
    frequencies = dict()
    for w in wordList:
        frequencies[str(w['word'])] = w['count']
    else:
        print("转换后的frequencies： ", frequencies)

    wc = WordCloud(font_path=font,  # 字体
                   background_color=background_color,  # 背景色
                   mask=mask_image,  # 遮罩
                   prefer_horizontal=prefer_horizontal,  # 水平文字比例
                   width=width,  # 宽度
                   height=height,  # 高度
                   colormap=colormap  # 字体颜色 为空则随机生成
                   )

    wc.fit_words(frequencies)

    # 显示图片
    # plt.imshow(wc, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()

    outImgPath = dirPath + "tmp/" + id + ".png"
    wc.to_file(outImgPath)

    # 响应图片
    with open(outImgPath, 'rb') as f:
        image = f.read()
    # print("生成图片：{} ，base64编码：{}".format(id, base64.b64encode(image)))
    response = Response(image, mimetype='image/png')
    # 删除文件
    os.remove(outImgPath)
    return response


def wordSegmentation(conf):
    ### 入参校验
    errMsg = []
    if "text" not in conf:
        errMsg.append("text 不能为空")
    if len(errMsg) > 0:
        return Response(errMsg)

    text = conf["text"]
    content = jieba.cut(text, cut_all=False)

    """读取停用词"""
    if "stopwords" not in conf:
        stopwords = set()
    else:
        stopwords_path = download("stopwords", conf["stopwords"])
        with open(stopwords_path, "r", encoding="utf-8") as fp:
            stopwords = set([s.rstrip() for s in fp.readlines()])  # 数组转集合
        # 增加特色停用词
        stopwords.add(" ")
        stopwords.add("\n")
    print("停用词：", stopwords)

    """去除停用词"""
    words = []
    for word in content:
        if word not in stopwords:
            words.append(word)

    counter = Counter(words)

    """排序并返回前n个词语"""
    if "top" not in conf:
        most_common = counter.most_common()
    else:
        most_common = counter.most_common(conf["top"])
    print("按频次计数后数据：", most_common)

    # 转换格式
    list = []
    for k, v in most_common:
        word = {
            "word": k,
            "count": v
        }
        list.append(word)
    else:
        print(list)

    return jsonify(list)
