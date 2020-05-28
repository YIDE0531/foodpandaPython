import modules.file_funtion as fileFun
import base64

#responseMsg = fileFun.webCrawlerRead()

#print (base64.b64encode(responseMsg.encode('utf-8')).decode('utf-8'))
from flask import Flask
app=Flask(__name__)

@app.route("/")
def home():
    return "base64.b64encode(responseMsg.encode('utf-8')).decode('utf-8')"
    #return base64.b64encode(responseMsg.encode('utf-8')).decode('utf-8')

@app.route("/test")
def test():
    return "Hellow False8888888888"

if __name__=="__main__":
    app.run()