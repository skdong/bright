import requests


def get_datas():
    url = 'http://hq.sinajs.cn/list=sh601006'
    rep = requests.get(url)
    item = rep.text.split('"')[1].split(',')
    for value in item:
        print value,
    return 'test'


def main():
    datas = get_datas()
    print datas


if __name__ == '__main__':
    main()
