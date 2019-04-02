import urllib
url = 'https://console.sinnetcloud.com.cn/account/alipay/notify_url'
url_data = 'seller_email=ghxw686868%40163.com&sign=df159217db654b770630006acc424ca9&subject=%E8%B4%A6%E6%88%B7%E5%85%85%E5%80%BC&is_total_fee_adjust=N&gmt_create=2018-03-20+16%3A39%3A08&out_trade_no=8c434887937fdf09e00bd27b3e0bfdd3&sign_type=MD5&price=10.00&buyer_email=myl%2A%2A%2A%40gmail.com&discount=0.00&trade_status=TRADE_SUCCESS&gmt_payment=2018-03-20+16%3A39%3A12&trade_no=2018032021001004050545212075&seller_id=2088311276421285&use_coupon=N&payment_type=1&total_fee=10.00&notify_time=2018-03-20+16%3A43%3A13&buyer_id=2088002058709056&notify_id=dfe30ad4e54497a9af5052f50f72165ge1&notify_type=trade_status_sync&quantity=1'

print urllib.open(url, url_data).read()


