import feedparser
import re
from bs4 import BeautifulSoup
from win10toast import ToastNotifier


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


def parse(url):
    freeBoxNews = []
    twitchDropsNews = []

    for item in rss_get_items(url):
        if 'free' in item.title or 'free' in item.summary:
            freeBoxNews.append(item)
        if 'livestream' in item.title or 'livestream' in item.summary:
            twitchDropsNews.append(item)

    print('These links might contain free boxes')
    for item in freeBoxNews:
        print('\t' + get_link_from_item(item))

    print()

    print('These links might contain twitch drops')
    for item in twitchDropsNews:
        print(f"\t {item.title}: {get_link_from_item(item)}")


def notify():
    toast = ToastNotifier()
    toast.show_toast(
        'These links might contain free boxes',
        'Notification body',
        duration=20,
        icon_path='poeicon.ico'
    )
