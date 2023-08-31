import re

import requests


def get_url(url, UA=None):
    if UA is None:
        UA = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        }
    data = requests.get(url='https://www.zkk78.com/dongmanplay/{}'.format(url), headers=UA).text
    url = re.findall('"url":"(.*?)"', data)[1]
    return "https://danmu.yhdmjx.com/m3u8.php?url={}".format(url)


if __name__ == "__main__":
    get_url()
