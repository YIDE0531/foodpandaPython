import modules.file_funtion as fileFun
import base64

responseMsg = fileFun.webCrawlerRead()

print (base64.b64encode(responseMsg.encode('utf-8')).decode('utf-8'))
