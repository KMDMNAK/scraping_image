import sys
if __name__ == "__main__":
    if sys.argv[1]=="0":
        import getImages

        IG = getImages.ImageGetter("bing")
        """
        print(IG.TextPattern)

        executableURL = IG.makeURL("トランプ", 1)
        print(executableURL)

        content = IG.getContent(executableURL)
        #print(content)

        imageURLs = IG.extractImageURL(content)
        print(len(imageURLs))
        """

        print(len(IG.execute("トランプ")))
    elif sys.argv[1] == "1":
        import googleImageSearch
        results = googleImageSearch.main("https://www.asahi.com/articles/ASMBZ659HMBZUHBI02V.html", 1)
        print(results)