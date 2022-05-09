import json

if __name__ == '__main__':
    list = []
    for a in range(200,0,-1):
        # list.append({"word": str(a), "count": a})
        list.append({"word": a, "count": a})
    else:
        print(json.dumps(list))
