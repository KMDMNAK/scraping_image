import sys
import time
import re
import requests

# https://www.bing.com/images/search?q=%E5%92%8C%E4%B9%85%E7%94%B0%E9%BA%BB%E7%94%B1%E5%AD%90&FORM=HDRSC2

SITE_OPERATOR = {
    "bing": {
        "pattern": r'<a [^>]*href[^=]*=[^"]*"([^"]*)"',
        "url": "https://www.bing.com/images/search?q={0}&page={1}"
    },
    "excite": {
        "pattern": r'<a href[^=]*=[^"]*"([^"]*)"',
        "url": "https://imagesearch.excite.co.jp/?q={0}&page={1}"
    },
    "google": {
        "pattern": "",
        "url":""
    }
}

class ImageGetter:
    def __init__(
            self,
            site):
        self.imageURLs = []
        self.TextPattern = SITE_OPERATOR[site].get("pattern")
        self.url = SITE_OPERATOR[site].get("url")

    def getContent(self, executableURL):
        get = requests.get(executableURL)
        content = str(get.text)
        get.close()
        return content

    def extractImageURL(self, content):
        """
            extract each data from content from url
        """
        imageURLs = []
        original_datas = re.findall(self.TextPattern, content, re.S)
        for each_data in original_datas:
            splited = each_data.split(".")
            if(len(splited) == 1):
                continue
            if(splited[-1] in ["jpeg", "jpg", "png"]):
                imageURLs.append(each_data)
        return imageURLs

    def makeURL(self, query, page):
        executableURL = self.url.format(query, page)
        return executableURL

    def execute(self, query, limit=100):
        """
            query(str) : what images you want to collect
        """
        page = 1
        while (len(self.imageURLs) < limit):
            executableURL = self.makeURL(query=query, page=page)
            content = self.getContent(executableURL)
            newImageURLs = self.extractImageURL(content)
            self.imageURLs.extend(newImageURLs)
            page += 1
        return self.imageURLs


"""
images = require_image_excite(
    "%E5%92%8C%E4%B9%85%E7%94%B0", 100, pattern=r'a href=\"(.*?)\"'
)
"""
