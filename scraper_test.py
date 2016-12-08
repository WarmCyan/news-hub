import urllib.request

print("Querying top stories...")
response = urllib.request.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json")
content = response.read()
response.close()
print("Got list response")

articles = []

for i in range(0, 10):
    articleNumber = content[i]
    print("Retrieving story " + str(articleNumber) + "...")
    response = urllib.request.urlopen("https://hacker-news.firebaseio.com/v0/item/" + articleNumber + ".json")
    articles[i] = response.read()
    response.close()
    print("Got story response")

#print(content[0])

print(articles)
