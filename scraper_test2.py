from lxml import html
import requests
import json
import time

startTime = time.clock()

print("Querying top stories...")
page = requests.get('https://hacker-news.firebaseio.com/v0/newstories.json')
data = json.loads(page.text)
print("Got top story list")

articles = []

for i in range(0, 10):
    # timing
    runTime = time.clock() - startTime

    # get article by number
    articleNumber = data[i]
    print(str(i) + " - " + str(runTime) + ") Retrieving story " + str(articleNumber) + "...")
    articles.append(json.loads(requests.get("https://hacker-news.firebaseio.com/v0/item/" + str(articleNumber) + ".json").text))
    #articles.append(requests.get("https://hacker-news.firebaseio.com/v0/item/" + str(articleNumber) + ".json").json())
    print("Got story response")
    
#print(articles)
index = 0
for article in articles:
    print(str(index) + " - " + str(article))
    index += 1

#totalTime = time.clock() - startTime

#print("Total scrape time: " + str(totalTime))
