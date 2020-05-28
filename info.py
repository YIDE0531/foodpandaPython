import modules.file_funtion as fileFun
import base64
import sys

url = sys.argv[1]  #測試網址 http://httpbin.org/post
#url = "https://www.foodpanda.com.tw/restaurant/f7sc/k-d-bistro-taipei#"
responseMsg = fileFun.webCrawlerInfo(url)
print (base64.b64encode(responseMsg.encode('utf-8')).decode('utf-8'))
