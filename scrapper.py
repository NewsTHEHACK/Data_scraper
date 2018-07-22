import requests, json
from bs4 import BeautifulSoup
from pprint import pprint
import re

result = []

def get_news_tags(web_page):
    tags = []
    web_data = requests.get(web_page)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    for i in soup.select("#keywords"):
        for j in i:
            if j.string != '' and j.string != " " and j.string != '\n':
                tags.append(j.string)
    if len(tags[1:]) == 0:
        for i in soup.select(".article-keywords"):
            for j in i:
                if j.string != '' and j.string != " " and j.string != '\n':
                    tags.append(j.string)
    return tags[1:]


def get_body(url):
    web_data = requests.get(url)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    try:
        title = soup.select('#article')[0].text
        return title
    except:
        try:
            title = soup.select('#artibody')[0].text
        except:
            return ''
        return title

def get_title(url):
    web_data = requests.get(url)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    try:
        title = soup.select('.main-title')[0].text
        return title
    except:
        try:
            title = soup.select('#artibodyTitle')[0].text
        except:
            return ''
        return title


def get_api_data(city):
    res = requests.get("http://api.map.baidu.com/geocoder/v2/?address=" + city + "&output=json&ak=hoDiRIzg2SRe96gQnSZH50yoNTj0cTgS&callback=showLocation")
    resp = json.loads(res.text.strip("showLocation&&showLocation()").rstrip(")"))
    if "result" in resp:
        return resp['result']['location']['lng'], resp['result']['location']['lat']
    return '', ''


def get_all():
    urls = ["http://news.sina.com.cn/world/", 'http://news.sina.com.cn/china/', "https://news.sina.com.cn/society/"]
    file = open('city.txt', 'r', encoding='UTF8').read()
    cities = re.split(r' |\n|★|▲|\t', file)
    for url in urls:
        web_data = requests.get(url)
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text,'lxml')

        for news in soup.select('.news-item'):
            web = {}
            if(len(news.select('h2')) > 0):
                h2 = news.select('h2')[0].text
                time = news.select('.time')[0].text
                a = news.select('a')[0]['href']
                tags = get_news_tags(a)
                title = get_title(str(a))
                body = get_body(str(a))
                print(h2,time,a, tags)
                web['url'] = str(a)
                web['title'] = title
                web['content'] = body
                web['tags'] = tags
                for city in cities:
                    if len(city) > 0:
                        if city in body:
                            web['city'] = city
                            x, y = get_api_data(city)
                            web['x'] = x
                            web['y'] = y
                            print(city)
                            break
                if len(title) == 0 and len(body) == 0 and len(tags) == 0:
                    pass
                else:
                    result.append(web)

get_all()

# pprint(result)
with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False)

