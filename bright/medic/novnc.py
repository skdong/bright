import requests


def get_vnc():
    params = {'instance_name': 'test-win',
              'instance_id': '5e6925b1-2144-4614-8f13-752a257305c9',
              'token': 'add23c3d-7296-45d6-9a1a-f0fa031c5c35',
              'image': 'windows',
              'path': 'RegionOne/websockify'}
    cookie = {' django_language': 'zh',
              ' region_id': 'RegionOne',
              ' user_id': 'a5020eebb22247289d0c4e41fbcb2f8e',
              ' JSESSIONID': 'dummy',
              ' token': 'add23c3d-7296-45d6-9a1a-f0fa031c5c35',
              'csrftoken': 'My6Eo8oVkIKAzrEKjbm9zk12MGFNoqZr',
              ' scope': 'project',
              ' project_id': '5d92506dfc0a4289aef1b375480020c4'}

    rq = requests.get('http://console.ghyun.com.cn/vnc/RegionOne/vnc_auto.html',
                      params=params)

    print rq.content


def get_websocket():
    url = 'http://console.ghyun.com.cn/RegionOne/websockify'
    headers = {'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Cache-Control': 'no-cache',
               'Connection': 'Upgrade',
               'Cookie': 'csrftoken=oAm0PCp8QeYNpbmyRYAShqe46TzFD9ij; user_id=a5020eebb22247289d0c4e41fbcb2f8e; region_id=RegionOne; sessionid=hlk0smnvnganb9w7xesqawzr1a0xkl5w; scope=project; project_id=5d92506dfc0a4289aef1b375480020c4; django_language=zh; ',
               'Host': 'console.ghyun.com.cn',
               'Origin': 'http://console.ghyun.com.cn',
               'Pragma': 'no-cache',
               'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
               'Sec-WebSocket-Key': 'f0Wp5PHgDluoQLVbGti6CQ==',
               'Sec-WebSocket-Version': '13',
               'Upgrade': 'websocket',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    rq = requests.get(url, headers=headers, )
    print rq.status_code


def get_novnc():
    url = 'http://console.ghyun.com.cn/RegionOne/websockify'
    headers = {'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Cache-Control': 'no-cache',
               'Connection': 'Upgrade',
               'Cookie': 'token=93f85634-7cd8-4ed1-a207-832dd1d3c351',
               'Host': 'console.ghyun.com.cn',
               'Origin': 'http://console.ghyun.com.cn',
               'Pragma': 'no-cache',
               'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
               'Sec-WebSocket-Key': 'Oi5CLf9yAt6q5ftlc/+ahA==',
               'Sec-WebSocket-Protocol': 'base64',
               'Sec-WebSocket-Version': '13',
               'Upgrade': 'websocket',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    print requests.get(url, headers=headers).content

def main():
    get_novnc()


if __name__ == "__main__":
    main()
