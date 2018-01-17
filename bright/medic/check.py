import requests
from timeit import Timer

url = 'http://console.oceanstack.slancer.com/os/compute/v2/9e923bf059524d97babb4d1446871c2f/os-keypairs'

url = 'http://console.oceanstack.slancer.com/us/manage/v1/config/global/DEFAULT/ENV_NAME'
# url = 'http://op.ghyun.com.cn/us/manage/v1/config/global/DEFAULT/ENV_NAME'
headers = {
    "Accept": "application/json",
    "User-Agent": "python-openstackclient keystoneauth1/2.3.0 python-requests/2.14.1 CPython/2.7.6",
    "X-Auth-Token": "42b3cb21502644e1a9f684f3b49dc8e0",
    # 'Cookie':'_ga=GA1.3.396182815.1512966034; csrftoken=6zDWgapr7dRUkHn8VqA5r0GXQr89LynI; user_id=7159ac5bd07a42b69e8660afcbe474a2; django_language=zh; sessionid=sdt5i55trhje5vpss8jylyl918vi1slf; scope=project; project_id=7a253c0075f147dca127669e0a19ea0d'
}


def check_url():
    print url
    print requests.get(url=url, headers=headers)


t1 = Timer("check_url()", "from __main__ import check_url")
print t1.repeat(10, 1)
