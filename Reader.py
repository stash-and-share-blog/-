from Setting import Setting
import os
import traceback
import re

class Reader:

    def __init__(self):
        pass

    def listAllDayDirNames(self):
        dayDirNameAry = []
        dirs = os.listdir(Setting.outputDirRoot)
        for tmpDirName in dirs:
            rx = re.compile(r"^(\d{4}-\d{1,2}-\d{1,2})$")
            if rx.match(tmpDirName):
                dayDirNameAry.append(tmpDirName)
        return dayDirNameAry

    def listHourDirPathsOfOneDay(self, dayDirStr):
        hrDirPathAry = []
        for i in range(0, 24): # 24 is for 1 day - 24 hr
            hrStr = "{:02d}".format(i + 1)
            hrDirPath = Setting.outputDirRoot + "/" + dayDirStr + "/" + dayDirStr + "_" + hrStr
            if os.path.exists(hrDirPath):
                hrDirPathAry.append(hrDirPath)
        return hrDirPathAry

    def listArticleDirPathsOfOneHour(self, hourDirPath):
        articleDirPathAry = []
        dirs = os.listdir(hourDirPath)
        for tmpDirName in dirs:
            rx = re.compile(r"^(\d{4}-\d{1,2}-\d{1,2}_\d{1,2}-\d{1,2}__\d{1,14}-\d{1,6})$")
            if rx.match(tmpDirName):
                articleDirPathAry.append(hourDirPath + "/" + tmpDirName)
        
        return articleDirPathAry

    def loadArticle_inArticleDir(self, articleDirPath):
        try:
            f = open(articleDirPath + "/text-content.txt", encoding="utf-8")
            content_with_title = f.read()  # output
            title = content_with_title.split("\n")[0]  # output
            content = content_with_title.split("\n")[2]  # output
            f.close()

            f = open(articleDirPath + "/url.url", encoding="utf-8")
            urlFileContent = f.read()
            url = urlFileContent.split("\n")[1].split("=")[1]  # output
            f.close()

            imgDict = {}
            fileList = os.listdir(articleDirPath)
            for fileName in fileList:
                # to get img url
                if fileName.startswith("img_") and not fileName.endswith("_desc.txt"):
                    f = open(articleDirPath + "/" + fileName, encoding="utf-8")
                    tmpImgUrlFileContent = f.read()
                    tmpImgUrl = tmpImgUrlFileContent.split(
                        "\n")[1].split("=")[1]  # output
                    f.close()
                    imgId = fileName[4:-4]  # for head "img_" and tail ".url"
                    imgDict[imgId] = {
                        "url": tmpImgUrl
                    }

            for fileName in fileList:
                # to get img desc
                if fileName.startswith("img_") and fileName.endswith("_desc.txt"):
                    f = open(articleDirPath + "/" + fileName, encoding="utf-8")
                    tmpImgDesc = f.read()  # output
                    f.close()
                    # for head "img_" and tail "_desc.txt"
                    imgId = fileName[4:-9]
                    imgDict[imgId]["desc"] = tmpImgDesc

            return {
                "url": url,
                "title": title,
                "content": content,
                "imgs": imgDict
            }

        except Exception:
            traceback.print_exc()
            return None


if __name__ == "__main__":
    r = Reader()

    # articleDirPathAry = r.listArticleDirPathsOfOneHour(r".\__output__\2019-07-13\2019-07-13_18")
    # print(articleDirPathAry)

    # dayDirNames = r.listAllDayDirNames()
    # print(dayDirNames)

    # hrDirPathAry = r.listHourDirPathOfOneDay("2019-07-13")
    # print(hrDirPathAry)
    
    # data = r.loadArticle_inArticleDir(r".\__output__\2019-07-13\2019-07-13_18\2019-07-13_18-24__20190713002360-260404")
    # print(data)
