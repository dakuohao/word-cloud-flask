from src.service import wordCloudImage


def testImag():
    list = [{"word": "20", "count": 20}, {"word": "19", "count": 19}, {"word": "18", "count": 18},
            {"word": "17", "count": 17}, {"word": "16", "count": 16}, {"word": "15", "count": 15},
            {"word": "14", "count": 14}, {"word": "13", "count": 13}, {"word": "12", "count": 12},
            {"word": "11", "count": 11}, {"word": "10", "count": 10}, {"word": "9", "count": 9},
            {"word": "8", "count": 8}, {"word": "7", "count": 7}, {"word": "6", "count": 6}, {"word": "5", "count": 5},
            {"word": "4", "count": 4}, {"word": "3", "count": 3}, {"word": "2", "count": 2}, {"word": "1", "count": 1}]

    wordCloudImage(list)
    print("完成")


if __name__ == '__main__':
    testImag()
