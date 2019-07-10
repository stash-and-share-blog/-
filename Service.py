from Crawler import Crawler
from threading import Timer
import traceback
import time


class Service:

    howOftenShouldServeiceCrawl_inSec = 5 * 60  # for every 5 minutes

    def __init__(self):
        self.crawler = Crawler()

    def batchSaveArticleAsFile(self):
        articleMetaList = self.crawler.getArticleMetaList()
        for articleMeta in articleMetaList:
            url = articleMeta["url"]
            articleDict = self.crawler.getArticleContent(url)
            self.crawler.saveArticleAsFile(articleMeta, articleDict)

    def start(self):
        currentTimeStr = time.strftime("%Y-%m-%d, %H:%M:%S")
        print("------ START TO CRAWL ------ @ " + currentTimeStr)
        try:
            self.batchSaveArticleAsFile()
        except Exception:
            traceback.print_exc()
        print("------ END OF THIS ROUND ------")

        # --------------------------------------------------
        t = Timer(Service.howOftenShouldServeiceCrawl_inSec, self.start)
        t.start()


if __name__ == "__main__":
    s = Service()
    s.start()
