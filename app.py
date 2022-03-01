# coding=UTF-8
import requests
import bs4
from flask import Flask, request
import json

#import base64

class Shop():
    def __init__(self, image, name):
        self.image = image
        self.name = name
        

def webCrawlerRead():
    url = "https://www.foodpanda.com.tw/city/taipei-city"  #測試網址 http://httpbin.org/post
    header = {   #FoodPanda有防爬蟲
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }
    session = requests.Session()
    r = session.get(url, headers = header)
    content = r.text
    #print(content)
    soup = bs4.BeautifulSoup(content, "html.parser")
    #titles = soup.find_all("a",target="_blank")
    #groups = enumerate(soup.find_all("div", class_="form-group row"))

    titles = soup.find_all("span", class_="name fn")
    images = soup.find_all("div", class_="vendor-picture b-lazy")
    infoUrl = soup.find_all("a", class_="hreview-aggregate url")

    result = []
    titleName = []
    shopImage = []
    shopInfoUrl = []

    for title in titles:
        if title.get_text() != None:
            titleName.append(title.get_text())

    for image in images:
        shopImage.append(image["data-src"].split("|")[1])

    for url in infoUrl:
        shopInfoUrl.append(url["href"])

    for i in range(0, len(titleName)):
        input_dict = {'title':titleName[i], 'image':shopImage[i], 'infoUrl':shopInfoUrl[i]}
        result.append(input_dict)

    return json.dumps(result, ensure_ascii=False)

    # for i,row in enumerate(soup.find_all("span", class_="name fn")):
    #     for j,datas in enumerate(row.find_all("a", title = "檢視本項產品細節資料")):
    #         title = row.find("div", class_="col-sm-2")
    #         print(title.a.string)
    #         ws.cell(row = num, column = 1).value = title.a.string
    #         ws.cell(row = num, column = 2).value = datas.get_text()
    #         datas = datas.get_text().split(' ')
    #         overflow = 0
    #         for ii in range(len(datas)):
    #             if datas[ii]=="C.C.":
    #                 ws.cell(row = num, column = ii +3 -1).value = datas[ii-1] + datas[ii].replace("C.C." ,"c.c.")
    #                 overflow += 1
    #             else:
    #                 ws.cell(row = num, column = ii + 3 - overflow).value = datas[ii]
    #         num+=1

def webCrawlerInfo(url):
    header = {   #FoodPanda有防爬蟲
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }
    session = requests.Session()
    r = session.get(url, headers = header)
    content = r.text
    soup = bs4.BeautifulSoup(content, "html.parser")

    infoUrl = soup.find_all("a", class_="hreview-aggregate url")

    title = []
    for i,row in enumerate(soup.find_all("div", class_="nav-holder")):  #選擇主項目
        for j,datas in enumerate(row.find_all("a")):
            # title += datas["title"]
            title.append(datas["title"])
            #print(datas["title"])
    
    responseMsg = []

    titleNum = [0]
    itemAddress = soup.find("p", class_="vendor-location").string
    itemDate = soup.find("span", class_="schedule-times").string

    #評論區 名稱，日期，評論內容
    itemComment = []

    #取得item名稱價錢與照片
    itemResult = []
    
    for i,row in enumerate(soup.find_all("div", class_="review-component hreview")):  #選擇主項目
        datas[0] = row.find("span", class_="fn").string
        datas[1] = row.find("abbr", class_="review-date dtreviewed").string
        datas[2] = row.find("div", class_="description").string

        if(datas[0]==None):
            datas[0] = "noperson"

        input_dict = {'itemCommentUserName':datas[0], 'itemCommentDate':datas[1], 'itemCommentText':datas[2]}
        itemComment.append(input_dict)
    #print(itemComment)
   
    num = 0
    for i,row in enumerate(soup.find_all("div", class_="dish-category-section")):  #主項目
        for j,datas in enumerate(row.find_all("li")):    #細項名稱
            data2 = json.loads(datas["data-object"])
            itemName = data2["name"]
            #print(data2["name"])
            image = datas.find("div", class_="photo")
            if(image!=None):
                itemImage = image["data-src"]
            else:
                itemImage = "notfind"

            price = datas.find("span", class_="price p-price")
            clearPrice = price.get_text().replace(" ", "")
            itemPrice = clearPrice.replace("\n", "")

            input_dict = {'itemName':itemName, 'itemImage':itemImage, 'itemPrice':itemPrice}
            itemResult.append(input_dict)
            num+=1
        titleNum.append(num)

    resultDic = {'title':title}
    resultDic['titleNum'] = titleNum
    resultDic['itemResult'] = itemResult
    resultDic['itemAddress'] = itemAddress
    resultDic['itemDate'] = itemDate
    resultDic['itemComment'] = itemComment
    # responseMsg = '{ "title": "' + title + '","titleNum": "' + titleNum + '","itemResult": "' + aaa + '","itemAddress": "' + itemAddress+'","itemDate": "' + itemDate+'","itemComment": "' + bbb +'"}'
    return json.dumps(resultDic, ensure_ascii=False)




#print (base64.b64encode(responseMsg.encode('utf-8')).decode('utf-8'))
from flask import Flask
app=Flask(__name__)

@app.route("/getData")
def home():
    #return "base64.b64encode(responseMsg.encode('utf-8')).decode('utf-8')"
    responseMsg = webCrawlerRead()
    return responseMsg
@app.route("/getInfo", methods=['POST'])
def test():
    url = request.form.get("infoUrl")
    # url = "https://www.foodpanda.com.tw/restaurant/f7sc/k-d-bistro-taipei#"
    responseinfo = webCrawlerInfo(url)
    return responseinfo

if __name__=="__main__":
    app.run()