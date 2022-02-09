import feedparser
import re
from bs4 import BeautifulSoup
from win10toast_click import ToastNotifier
import subprocess as sp


def rss_get_items_feedparser(webData):
    feed = feedparser.parse(webData)
    items = feed["items"]
    return items


def rss_get_items_beautifulSoup(webData):
    soup = BeautifulSoup(webData)
    for item_node in soup.find_all('item'):
        item = {}
        for subitem_node in item_node.findChildren():
            if subitem_node.name is not None:
                item[str(subitem_node.name)] = str(subitem_node.contents[0])
        yield item


def rss_get_items(webData):
    items = rss_get_items_feedparser(webData)
    if (len(items) > 0):
        return items
    return rss_get_items_beautifulSoup(webData)


def get_link_from_item(item):
    p = re.compile(
        'https://www.pathofexile.com/forum/view-thread/[0-9]+">Read More'
    )

    return p.search(item.summary).group()[:-11]


def parseAndReturnNews(url):
    freeBoxNews = []
    twitchDropsNews = []

    for item in rss_get_items(url):
        if 'free' in item.title.lower() or 'free' in item.summary.lower():
            freeBoxNews.append(item)
        if 'drops' in item.title.lower() or 'drops' in item.summary.lower():
            twitchDropsNews.append(item)

    return [freeBoxNews, twitchDropsNews]


def createNotification(news):
    old_news = readFileToString()
    formattedNews = ''

    formattedNews += 'These links might contain free boxes\n'
    for item in news[0]:
        link = get_link_from_item(item)
        if link not in old_news:
            formattedNews += (f'NEW\t {item.title}:'
                              f'{get_link_from_item(item)}\n')
        else:
            formattedNews += f'\t {item.title}: {get_link_from_item(item)}\n'

    formattedNews += '\n'

    formattedNews += 'These links might contain twitch drops\n'
    for item in news[1]:
        link = get_link_from_item(item)
        if link not in old_news:
            formattedNews += (f'NEW\t {item.title}:'
                              f'{get_link_from_item(item)}\n')
        else:
            formattedNews += f'\t {item.title}: {get_link_from_item(item)}\n'

    return formattedNews


def readFileToString():
    with open('poenews.txt', 'r') as file:
        data = file.read()
        return data


def writeNewsToFile(news):
    f = open('poenews.txt', 'w')
    f.write(news)
    f.close()


def openNewsFile():
    programName = "C:/Program Files (x86)/Notepad++/notepad++.exe"
    fileName = "poenews.txt"
    sp.Popen([programName, fileName])


def notify(title, body):
    toast = ToastNotifier()
    toast.show_toast(
        title,
        body,
        duration=20,
        icon_path='./poeicon.ico',
        threaded=True,
        callback_on_click=openNewsFile
    )


def main():
    url = 'https://www.pathofexile.com/news/rss'

    news = parseAndReturnNews(url)
    formattedNews = createNotification(news)
    writeNewsToFile(formattedNews)

    notify('These PoE news are interesting', "Click to see what's up")


main()
