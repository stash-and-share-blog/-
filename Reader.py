from Setting import Setting
import os


class Reader:

    def __init__(self):
        pass

    # def loadArticleOfOneDay(self, dateStr):
    #     for i in range(0, 24): # 24 is for 1 day - 24 hr
    #         hrStr = "{:02d}".format(i + 1)
    #         hrDirName = Setting.outputDirRoot + "/" + dateStr + "/" + dateStr + "_" + hrStr, "r"
    #         if os.path.exists(hrDirName):

    def loadArticle_inArticleDir(self, articleDirPath):
        f = open(articleDirPath + "/text-content.txt", encoding="utf-8")
        content_with_title = f.read()  # output
        title = content_with_title.split("\n")[0]  # output
        content = content_with_title.split("\n")[2]  # output
        f.close()
        # TODO to get other data
        return {
            "title": title,
            "content": content
        }


if __name__ == "__main__":
    r = Reader()
    # r.loadArticleOfOneDay("2019-07-10")
    r.loadArticle_inArticleDir(
        r".\__output__\2019-07-12\2019-07-12_16\2019-07-12_16-32__20190712003070-260405")
