from Reader import Reader

class Analyzer:

    def __init__(self):
        pass

    def analyze(self):
        pass

if __name__ == "__main__":
    
    dayArticleNumDict = {}
    hrArticleNumDict = {}
    articlePicNumDict = {}
    articleNum = 0
    articleWithPicNum = 0
    
    r = Reader()
    dayDirNames = r.listAllDayDirNames()
    for dayDirName in dayDirNames:
        hrDirPathAry = r.listHourDirPathsOfOneDay(dayDirName)
        for hrDirPath in hrDirPathAry:
            hrDirName = hrDirPath.split("/")[-1]
            articleDirPathAry = r.listArticleDirPathsOfOneHour(hrDirPath)
            hrArticleNumDict[hrDirName] = len(articleDirPathAry)
            if dayDirName in dayArticleNumDict:
                dayArticleNumDict[dayDirName] += len(articleDirPathAry)
            else:
                dayArticleNumDict[dayDirName] = len(articleDirPathAry)

            for articleDirPath in articleDirPathAry:
                articleData = r.loadArticle_inArticleDir(articleDirPath)
                articleId = articleDirPath.split("/")[-1]
                if not articleData == None:
                    articleNum += 1

                    imgsDict = articleData["imgs"]
                    if not len(imgsDict) == 0:
                        articleWithPicNum += 1
                        articlePicNumDict[articleId] = len(imgsDict)

    print("articleNum", articleNum)
    print("articleWithPicNum", articleWithPicNum)
    print("hrArticleNumDict", hrArticleNumDict)
    print("dayArticleNumDict", dayArticleNumDict)
    print("articlePicNumDict", articlePicNumDict)

        