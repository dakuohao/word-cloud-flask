from os import path

import jieba as jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt

if __name__ == '__main__':
    """读取停用词"""
    with open("../res/stopwords/stopwords.txt", "r", encoding="utf-8") as fp:
        stopwords = set([s.rstrip() for s in fp.readlines()])  # 数组转集合

    """获取文本内容"""
    with open("../res/doc/input.txt", "r", encoding="utf-8") as fp:
        content = fp.read()

    """中文分词"""
    # content = jieba.lcut(content)
    content = jieba.cut(content,cut_all=False)

    """去除停用词"""
    text = []
    for word in content:
        if word not in stopwords:
            text.append(word)

    #计数器
    counter = Counter(text)
    # items = counter.items()

    # 排序
    # most_common = counter.most_common()
    most_common = counter.most_common(500)
    print(most_common)
    # with open('doc//词频统计.txt','w') as fw:
    #     for item in most_common:
    #         fw.write("%s\n" % item)

    frequency = dict(most_common)  # 去掉停用词后的词频统计

    # mask_image = plt.imread("images/bg.png")
    d = path.dirname(__file__)
    mask_image = np.array(Image.open(path.join(d, "../res/bg.png")))

    wc = WordCloud(font_path='../res/msyh.ttf',  # 字体
                   background_color="white",  # 背景色
                   mask=mask_image,  # 遮罩
                   prefer_horizontal=1.6,  # 水平文字比例
                   width=400,  # 宽度
                   height=200,  # 高度
                   colormap="tab10"
                   )

    wc.fit_words(frequency)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wc.to_file("out/out.png")
