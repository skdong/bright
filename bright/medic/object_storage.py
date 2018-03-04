import requests

# headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
#           'Accept-Encoding': 'gzip, deflate',
#           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#           'Cache-Control': 'no-cache',
#           'Connection': 'keep-alive',
#           'Cookie': '_ga=GA1.2.963664809.1514345711; csrftoken=VnJLFw4SK9olX3C3VBnKBmqnIBEtPiMT; region_id=RegionOne; django_language=zh; sessionid=5cydeqrtb136z6n46s6ias6fglvrl4oy; user_id=f059a19a56c348eebf51b64ba542d719; scope=project; project_id=9e923bf059524d97babb4d1446871c2f',
#           'Host': 'console.oceanstack.slancer.com',
#           'Pragma': 'no-cache',
#           'Referer': 'http://console.oceanstack.slancer.com/apps/storage',
#           'REGION': 'RegionOne',
#           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
#           'X-Requested-With': 'XMLHttpRequest',
#           }

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Cookie": "Hm_lvt_314a8b89f08af7522545eae893ab2179=1499221310; _ga=GA1.1.415801105.1490755877; csrftoken=N4fznXtVVZnYavQVUQjocEuFWmagD1at; user_id=e18d7d57bff94e2784dc45f84481db02; region_id=RegionOne; sessionid=hzkpf951lhu3mampwmj98exjuc8bj9gg; scope=project; project_id=b5112f82a3e44f908937fc1c2bd1e191; django_language=zh; JSESSIONID=dummy",
    "Host": "10.0.30.10:5555",
    "Origin": "http://10.0.30.10:5555",
    "Referer": "http://10.0.30.10:5555/apps/storage",
    "REGION": "RegionOne",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
    # "X-Container-Read": ".r:*,.rlistings",
    "x-container-read": ".r:*,.rlistings",
    "X-Requested-With": "XMLHttpRequest",
}
# url = 'http://console.oceanstack.slancer.com/os/object-store/swift/v1'
# url = 'http://console.oceanstack.slancer.com/us/bill/v2/products'
# url = 'http://10.0.30.10:5555/os/object-store/swift/v1/b5112f82a3e44f908937fc1c2bd1e191test-2'
url = 'http://console.test.oceanstack.slancer.com/os/object-store/swift/v1/b5112f82a3e44f908937fc1c2bd1e191test-3'

print requests.post(url, headers=headers)
import pprint

pprint.pprint(requests.get(url, headers=headers).headers)
