from urllib.parse import urlencode

from lxml import etree
from requests.exceptions import ConnectionError
import requests

base_url = 'https://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'CXID=A64D2BD94A2D3C579BDD04D023174065; SUID=BEF00CB73965860A5BAB42B3000A2D1A; ad=w4lxvkllll2b$138lllllVmHkzDlllllHZ8Zskllll9lllll4joll5@@@@@@@@@@; sw_uuid=6930958092; ssuid=3030699075; dt_ssuid=7818600662; start_time=1538794445706; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; SUV=009A01EDB70CF1A85BBC5FC7C3F6D070; ABTEST=0|1539242883|v1; IPLOC=CN4403; weixinIndexVisited=1; SNUID=13D3AE84F6F3821B19C9F002F60A4CD4; JSESSIONID=aaaF12sJKyzTd4zBu7Hzw; ppinf=5|1539245221|1540454821|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTglQkYlOTklRTYlQTAlQjclRTUlQTUlQkQlRTQlQkElODZ8Y3J0OjEwOjE1MzkyNDUyMjF8cmVmbmljazozNjolRTglQkYlOTklRTYlQTAlQjclRTUlQTUlQkQlRTQlQkElODZ8dXNlcmlkOjQ0Om85dDJsdUVmUEJnbl9RVlNHVlF1T2RrNmFtZlFAd2VpeGluLnNvaHUuY29tfA; pprdig=GupJP6bZIw94PY64FSNP0HeA_S1h5LwOeLjOgNNci8MgzMxsiq2dJLDBrCwCjfyKAmYOouIoVbTa3mRaRYRswnqAxSuDooHngs9BoNIF9xWLlpMgmdEgxdxj8OiAskfITUtz73pqChkv-8Rhl40xShXxRFQnJplDzJEF7t3SCk0; sgid=20-37459125-AVuicBKWpMTBM34DicfZdagPg; ppmdig=15392452210000000b4a966a1c684a96f7959ad2b85361a7; sct=4',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://weixin.sogou.com/weixin?query=%E8%99%8E%E7%89%99%E8%8E%89%E5%93%A5%E8%B4%A6%E5%8F%B7%E8%A2%AB%E5%B0%81&s_from=hotnews&type=2&page=11&ie=utf8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
proxy_pool_url = 'http://127.0.0.1:5000/get'
proxy = None
max_count = 5


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError as e:
        return None


def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    global proxy
    global max_count
    if count >= max_count:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            print(proxies)
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            print('200')
            return response.text
        if response.status_code == 302:
            #Next Proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return get_html(url)
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)

def get_index(keyword, page):
    data = {
        'query': keyword,
        'page': page,
        'type': 2
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_html_index(html):
    if html:
        selector = etree.HTML(html)
        src = selector.xpath('//h3/a[@id="sogou_vr_11002601_title_0"]/@href')
        print(src)


def main():
    for page in range(1, 101):
        html = get_index('风景', page)
        parse_html_index(html)


if __name__ == '__main__':
    main()