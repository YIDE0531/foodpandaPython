# coding=UTF-8
import sys
import modules.file_funtion as fileFun
import base64

url = sys.argv[1]  #測試網址 http://httpbin.org/post
# url = "https://www.foodpanda.com.tw/restaurant/a1ce/hala-chicken#restaurant-info"
responseMsg = fileFun.webCrawlerInfo(url)
print (base64.b64encode(responseMsg.encode('utf-8')).decode('utf-8'))