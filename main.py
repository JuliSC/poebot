import poebot

url = 'https://www.pathofexile.com/news/rss'

news = poebot.parseAndReturnNews(url)
formattedNews = poebot.createNotification(news)
poebot.writeNewsToFile(formattedNews)

poebot.notify('These PoE news are interesting', "Click to see what's up")
