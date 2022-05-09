# encoding:utf8
import base64
import uuid

import time
from flask import Flask, request, jsonify

from service import wordCloudImage, wordSegmentation

app = Flask(__name__)


# 首页测试
@app.route('/')
def index():
    return 'Hello Flask!'


# json测试
@app.route('/json')
def json():
    r = {
        "code": 1,
        "msg": "成功"
    }
    return jsonify(r)


@app.route('/api/v1/wordCloud/image', methods=["POST"])
def image():
    """
    生成词云图片接口
    """

    start_time = time.time()
    id = str(uuid.uuid1())
    conf = request.json
    r = wordCloudImage(conf, id)
    end_time = time.time()
    print("调用生成图片\nuuid：{}\n耗时：{}\n入参：{}\n返回：{}".format(id, end_time - start_time, conf, base64.b64encode(r.data)))

    return r


@app.route('/api/v1/wordCloud/wordSegmentation', methods=["POST"])
def fenci():
    """
    分词接口
    """

    start_time = time.time()
    conf = request.json
    end_time = time.time()
    r = wordSegmentation(conf)
    print("调用分词接口\nuuid：{}\n耗时：{}\n入参：{}\n返回：{}".format(id, end_time - start_time, conf, r.json))

    return r


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    # app.run(host='0.0.0.0')
