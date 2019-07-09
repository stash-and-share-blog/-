# https://www.chinatimes.com/realtimenews
# --------------------------------------------------

import requests
import time
from bs4 import BeautifulSoup
import os


class Xiaolongbao:

    def __init__(self):
        self.baseUrl = "https://www.chinatimes.com"

    def getArticleMetaList(self):
        res = requests.get(self.baseUrl + "/realtimenews")
        soup = BeautifulSoup(res.text, "lxml")

        articleList = []
        for elem in soup.select(".articlebox-compact"):
            urlElem = elem.select(".title a")[0]
            title = urlElem.get_text()  # output
            href = urlElem.attrs["href"]
            url = self.baseUrl + str(href)  # output
            urlId = url.split("/")[-1]  # output

            timeElem = elem.select("time")[0]
            datetime = timeElem.attrs["datetime"]  # output

            datetimeForFileName = datetime.replace(":", "-").replace(" ", "_")
            dirName = datetimeForFileName + "__" + urlId

            articleList.append({
                "title": title,
                "url": url,
                "urlId": urlId,
                "datetime": datetime,
                "dirName": dirName
            })
            

        return articleList

    def getArticleContent(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")

        title = soup.select(".article-title")[0].get_text()  # output

        # to get text content
        pAry = soup.select(".article-body p")
        textContent = ""  # output
        for pElem in pAry:
            textContent += pElem.get_text()

        # to get hash tags
        hashTags = []
        hashTagLinkElems = soup.select(".hash-tag a")
        for hashTagLinkElem in hashTagLinkElems:
            hashTags.append(hashTagLinkElem.get_text())

        # to get photo url
        imgAry = []
        imgElems = soup.select(".photo-container img.photo")
        for imgElem in imgElems:
            imgUrl = imgElem.attrs["src"]
            imgDesc = imgElem.attrs["alt"]

            imgDict = {}
            imgDict["url"] = imgUrl
            imgDict["desc"] = imgDesc
            imgAry.append(imgDict)

        return {
            "url": url,
            "textContent": textContent,
            "hashTags": hashTags,
            "imgAry": imgAry
        }

    def saveArticleAsFile(self, articleMeta, articleDict):
        dirName = articleMeta["dirName"]
        os.makedirs(dirName)
        # TODO now-here


if __name__ == "__main__":
    bao = Xiaolongbao()
    articleMetaList = bao.getArticleMetaList()

    for articleMeta in articleMetaList:
        url = articleMeta["url"]
        articleDict = bao.getArticleContent(url)

        bao.saveArticleAsFile(articleMeta, articleDict)

