
# coding: utf-8

# ##### 詳細ページ
# 画像ページですること

# In[ ]:

import numpy as np
import urllib.request
from bs4 import BeautifulSoup

# 一番詳細なページから画像urlのみ抽出
def exImageUrlFromDetailedPage(urlDetailedPage):

    url_each_image_on_it = urlDetailedPage

    isSucceeded = True
    img_url = ""
    #print(urlDetailedPage)

    try:
        html = urllib.request.urlopen(url_each_image_on_it)
        soup = BeautifulSoup(html, "html.parser")

        div_separator = soup.find("div", class_="separator")
        img_url = div_separator.a.get("href")

        isSucceeded = True
        #print(True)
    except:
        isSucceeded = False
        #print(False)
        pass

    # debug用
    #title_tag = soup.title
    #print(title_tag)

    return isSucceeded, img_url


# # クローリング関数

# In[ ]:

def crawlingYandM(yandm_url, urllist):
    #print(yandm_url)
    num = 0
    missed_count = 0

    imageList = []

    while(True):
        sub_url = "blog-post_" + str(num) + ".html"
        detailed_url = yandm_url + "/" + sub_url
        # print(detailed_url)

#        imageURL = exImageUrlFromDetailedPage(detailed_url)
        isSucceeded, url = exImageUrlFromDetailedPage(detailed_url)


        if isSucceeded == True:
            imageList.append(url)
            #print("success!")
            #print(url)
        else:
            missed_count += 1
            #print(url)


        # ページがなかった回数が上限値を超えたらループbreak
        if num > 20000 or missed_count > 2000:
            break

        if (num % 1000 == 0) or (missed_count % 200 == 0):
            print("num:" + str(num) + " , missed_count:" + str(missed_count))
        # 番号更新

        num += 1

    urllist.extend(imageList)

    return urllist


# # ダウンロード関数

# In[ ]:

def downloadImageFromList(urlList, path):
    print(path)
    print("downloading")
    index=0
    for url in urlList:
        try:
            index += 1
            i = urllib.request.urlopen(url)
            filename = str(index) + ".png"

            saveData = open(path +  filename, 'wb')

            saveData.write(i.read())
            saveData.close()

            i.close()
        except:
            pass
    a = index
    return index

#downloadImageFromList(list, "./imgs/")


# In[ ]:

def crawlingFromTop(top_url):
    print("crawling")

    year = np.array(["2012", "2013", "2014", "2015", "2016"])
    mon = np.array(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])

    URLList = []

    for y in year:
        #if y != "2012":
        #    continue

        for m in mon:
            yandm = y + "/" + m
            #print(yandm)
            yandmUrl = top_url + "/" + yandm
            URLList = crawlingYandM(yandmUrl, URLList)

            #downloadImageFromList(URLList, "./imgs/")
            #URLList = []
            print(yandm)
            print(URLList)
    a = 1
    return URLList

#%debug


# # main関数

# In[ ]:

import numpy as np

if __name__ == "__main__":

    top_url = "http://www.irasutoya.com"
    urllist = crawlingFromTop(top_url)
    downloadImageFromList(urllist, "./imgs/")
    print("main function")


# In[ ]:
