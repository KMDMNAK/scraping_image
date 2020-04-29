import os
import re
import sys
import time
import requests
import threading
from functools import reduce
# https://www.bing.com/?scope=images&nr=1&FORM=NOFORM
SITE_OPERATOR = {
    "bing": {
        "pattern": r'<a [^>]*href[^=]*=[^"]*"([^"]*)"',
        "url": "https://www.bing.com/images/search?q={0}&page={1}&qs=n&form=QBIRMH&scope=images&sp=-1&pq={0}"
    },
    "excite": {
        "pattern": r'<a href[^=]*=[^"]*"([^"]*)"',
        "url": "https://imagesearch.excite.co.jp/?q={0}&page={1}"
    },
    "google": {
        "pattern": "",
        "url": ""
    }
}


def get_content(url, site_name):
    if site_name == 'bing':
        session = requests.Session()
        session.get('https://www.bing.com/')
        resp = session.get(url)
        content = str(resp.text)
    else:
        with requests.get(url) as resp:
            content = str(resp.text)
    return content


def extract_image_url(content, pattern):
    """
        extract each data from content from url
    """
    original_datas = re.findall(pattern, content, re.S)
    def each_loop(image_urls, each_data):
        splited = each_data.split(".")
        if(len(splited) == 1):
            return image_urls
        if(splited[-1] in ["jpeg", "jpg", "png"]):
            image_urls.append(each_data)
        return image_urls
    image_urls = reduce(each_loop, original_datas, [])
    return image_urls


def make_url(site_operator, query, page):
    executable_url = site_operator['url'].format(query, page)
    return executable_url


def create_query(parsed_query):
    query = parsed_query
    return query


def get_image_urls(site_name: str, image_num: int, query: str):
    page = 1
    image_urls = []
    site_operator = SITE_OPERATOR.get(site_name)
    if site_operator is None:
        raise BaseException(f'Site {site_name} does not exists.')
    while len(image_urls) < image_num:
        executable_url = make_url(site_operator, query, page)
        content = get_content(executable_url, site_name)
        newimage_urls = extract_image_url(
            content, site_operator.get('pattern'))
        image_urls.extend(newimage_urls)
        page += 1
    return image_urls


def save_images(image_urls, save_directory):
    if not os.path.isdir(save_directory):
        os.mkdir(save_directory)

    def get_and_save_image(image_url, save_path):
        with requests.get(image_url) as resp:
            with open(save_path, "wb") as f:
                f.write(resp.content)
    for i, url in enumerate(image_urls):
        file_path = os.path.join(save_directory, str(i) + '.jpg')
        threading.Thread(target=get_and_save_image,
                         args=(url, file_path)).start()


if __name__ == "__main__":
    _, site_name, image_num, parsed_query = sys.argv
    query = create_query(parsed_query)
    image_urls = get_image_urls(site_name, image_num, query)
