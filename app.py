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
    r = requests.get(url)
    content = r.text
    #print(content)
    soup = bs4.BeautifulSoup(content, "html.parser")
    #titles = soup.find_all("a",target="_blank")
    #groups = enumerate(soup.find_all("div", class_="form-group row"))

    titles = soup.find_all("span", class_="name fn")
    images = soup.find_all("div", class_="vendor-picture b-lazy")
    infoUrl = soup.find_all("a", class_="hreview-aggregate url")


    titleName = ""
    for title in titles:
        if title.get_text() != None:
            titleName += title.get_text()+",,,"
    titleName = titleName[:len(titleName)-1]

    shopImage = ""
    for image in images:
        shopImage += image["data-src"].split("|")[1]+","
    shopImage = shopImage[:len(shopImage)-1]

    shopInfoUrl = ""
    for url in infoUrl:
        shopInfoUrl += url["href"] + ","
    shopInfoUrl = shopInfoUrl[:len(shopInfoUrl)-1]

    responseMsg = '{ "title": "' + titleName + '","image": "' + shopImage + '","infoUrl": "' + shopInfoUrl + '"}'
    return responseMsg

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
    r = requests.get(url)
    content = r.text
    soup = bs4.BeautifulSoup(content, "html.parser")

    infoUrl = soup.find_all("a", class_="hreview-aggregate url")

    title = ""
    for i,row in enumerate(soup.find_all("div", class_="nav-holder")):  #選擇主項目
        for j,datas in enumerate(row.find_all("a")):
            title += datas["title"] + ","
            #print(datas["title"])
    title = title[:len(title)-1]
    
    itemName = ""
    itemImage = ""
    titleNum = "0,"
    itemPrice = ""
    itemAddress = soup.find("p", class_="vendor-location").string
    itemDate = soup.find("span", class_="schedule-times").string
    itemComment = ""
    
    for i,row in enumerate(soup.find_all("div", class_="review-component hreview")):  #選擇主項目
        datas[0] = row.find("span", class_="fn").string
        datas[1] = row.find("abbr", class_="review-date dtreviewed").string
        datas[2] = row.find("div", class_="description").string

        if(datas[0]==None):
            datas[0] = "noperson"

        itemComment += datas[0] + ",,," + datas[1] + ",,," + datas[2] + ",,,"
    itemComment = itemComment[:len(itemComment)-3]
    #print(itemComment)
   
    num = 0
    for i,row in enumerate(soup.find_all("div", class_="dish-category-section")):  #主項目
        for j,datas in enumerate(row.find_all("li")):    #細項名稱
            data2 = json.loads(datas["data-object"])
            itemName += data2["name"] + ","
            #print(data2["name"])
            image = datas.find("div", class_="photo")
            if(image!=None):
                itemImage += image["data-src"] + ","
            else:
                itemImage += "notfind" + ","

            price = datas.find("span", class_="price p-price")
            clearPrice = price.get_text().replace(" ", "")
            itemPrice += clearPrice.replace("\n", "") + ","
            
            num+=1
        titleNum += str(num) + ","
    itemName = itemName[:len(itemName)-1]
    itemImage = itemImage[:len(itemImage)-1]
    titleNum = titleNum[:len(titleNum)-1]
    itemPrice = itemPrice[:len(itemPrice)-1]
    #print(itemPrice)

    #print(titleNum)
    #print(itemImage)

    responseMsg = '{ "title": "' + title + '","titleNum": "' + titleNum + '","itemName": "' + itemName + '","itemImage": "' + itemImage+ '","itemPrice": "' + itemPrice +'","itemAddress": "' + itemAddress+'","itemDate": "' + itemDate+'","itemComment": "' + itemComment +'"}'
    return responseMsg




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
    #url = "https://www.foodpanda.com.tw/restaurant/f7sc/k-d-bistro-taipei#"
    responseinfo = webCrawlerInfo(url)
    return responseinfo

if __name__=="__main__":
    app.run()