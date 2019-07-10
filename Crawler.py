# https://www.chinatimes.com/realtimenews
# --------------------------------------------------

import requests
import time
from bs4 import BeautifulSoup
import os


class Crawler:

    outputDirRoot = "./__output__"

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

            hourParentDir = datetimeForFileName[:13]  # output
            dayParentDir = datetimeForFileName[:10]  # output

            articleList.append({
                "title": title,
                "url": url,
                "urlId": urlId,
                "datetime": datetime,
                "dirName": dirName,
                "hourParentDir": hourParentDir,
                "dayParentDir": dayParentDir
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

            imgDict = {
                "url": imgUrl,
                "desc": imgDesc
            }
            imgAry.append(imgDict)

        return {
            "url": url,
            "textContent": textContent,
            "hashTags": hashTags,
            "imgAry": imgAry
        }

    def __createDataAbsPath__(self, articleMeta):
        dirName = articleMeta["dirName"]
        hourParentDir = articleMeta["hourParentDir"]
        dayParentDir = articleMeta["dayParentDir"]
        return Crawler.outputDirRoot + "/" + \
            dayParentDir + "/" + hourParentDir + "/" + dirName

    def saveArticleAsFile(self, articleMeta, articleDict):
        dirAbsPath = self.__createDataAbsPath__(articleMeta)
        url = articleMeta["url"]
        textContent = articleDict["textContent"]

        dirName = articleMeta["dirName"]
        if not os.path.exists(dirAbsPath):
            os.makedirs(dirAbsPath)
        else:
            print("article exist, skip: " + dirName)
            return

        # --- write URL file
        f = open(dirAbsPath + "/url.url", "w", encoding="utf-8")
        f.write("[InternetShortcut]\n")
        f.write("URL=" + url)
        f.close()

        # --- write text-content
        f = open(dirAbsPath + "/text-content.txt", "w", encoding="utf-8")
        f.write(textContent)
        f.close()

        imgAry = articleDict["imgAry"]
        for imgDict in imgAry:
            imgUrl = imgDict["url"]
            imgFileName = imgUrl.split("/")[-1]
            imgId = imgFileName.split(".")[0]

            # --- write photo url
            f = open(dirAbsPath + "/img_" + imgId +
                     ".url", "w", encoding="utf-8")
            f.write("[InternetShortcut]\n")
            f.write("URL=" + imgUrl)
            f.close()

            # --- write photo desc
            f = open(dirAbsPath + "/img_" + imgId + "_desc.txt",
                     "w", encoding="utf-8")
            f.write(imgUrl)
            f.write("\n\n")
            f.write(imgDict["desc"])
            f.close()

            # # --- download photo
            # with open(dirAbsPath + "/img_" + imgFileName, 'wb') as handle:
            #     res = requests.get(imgUrl, stream=True)

            #     # TODO to handle err
            #     # if not res.ok:
            #     #     print(res)

            #     for buff in res.iter_content(2048):
            #         if not buff:
            #             break
            #         handle.write(buff)

        print("article saved: " + dirName)


if __name__ == "__main__":
    crawler = Crawler()
    articleMetaList = crawler.getArticleMetaList()

    for articleMeta in articleMetaList:
        url = articleMeta["url"]
        articleDict = crawler.getArticleContent(url)

        crawler.saveArticleAsFile(articleMeta, articleDict)
