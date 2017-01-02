import requests
import json
import time
import sys

startTime = time.clock()

articleIDList = None # list of id numbers returned from firebase query
articleData = [] # actual list of article data from each individual article id query
saved = [] # list of id numbers that have been retrieved successfully

# stats
numArticles = 0

# take care of initial log file (erase any current contents)
logFile = open("logs/hnscrape.log", 'w')
logFile.close()

dataFileName = sys.argv[1]

def log(msg):
    safeMsg = safe(msg)
    logFile = open("logs/hnscrape.log", 'a')
    logFile.write(safeMsg + "\n")
    logFile.close()
    print(safeMsg)

# make sure encoding isn't monkey business
def safe(obj):
    try: obj = str(obj) # convert to string first if necessary
    except: pass
    obj = obj.encode(sys.stdout.encoding, errors="replace").decode("utf-8")
    return obj

def loadSaved():
    global dataFileName
    global saved
    global articleData
    
    try:
        saveFile = open("data/" + dataFileName + "_saved.json", 'r')
        saved = json.loads(saveFile.read())
        
        dataFile = open("data/" + dataFileName + "_temp.json", 'r')
        articleData = json.loads(dataFile.read())

        log("\nFound previous temp/save files!\n")
    except:
        log("\nNo temp or save files found for this data set, creating new...\n")
        pass

def saveDataset(temp=False, point=0):
    global articleData
    global dataFileName
    global saved
    
    # write the article data
    dataFile = None
    if temp: dataFile = open("data/" + dataFileName + "_temp.json", 'w')
    else: dataFile = open("data/" + dataFileName + ".json", 'w')
    dataFile.write(json.dumps(articleData))
    dataFile.close()

    # write the saved list
    saveFile = open("data/" + dataFileName + "_saved.json", 'w')
    saveFile.write(json.dumps(saved))
    saveFile.close()

def getCurrentRunTime():
    global startTime
    runTime = time.clock() - startTime
    return "(" + str(int(runTime)) + " sec)"

def obtainTopArticles():
    global articleIDList
    global articleData
    global numArticles
    
    log(getCurrentRunTime() + " Querying top stories...")
    page = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    articleIDList = json.loads(page.text)
    numArticles = len(articleIDList)
    log(getCurrentRunTime() + " Queried top story list!")
    
def obtainNewArticles():
    global articleIDList
    global articleData
    global numArticles
    
    log(getCurrentRunTime() + " Querying new stories...")
    page = requests.get('https://hacker-news.firebaseio.com/v0/newstories.json')
    articleIDList = json.loads(page.text)
    numArticles = len(articleIDList)
    log(getCurrentRunTime() + " Queried new story list!")

def printArticleCount():
    global numArticles
    log("\nArticle list count: " + str(numArticles) + "\n")

def retrieveArticleData():
    global articleIDList
    global articleData
    global numArticles
    global saved
    
    index = 0
    for articleID in articleIDList:
        #if (index > 10): break # DEBUG
        
        # skip this one if we've already done it
        if articleID in saved:
            index += 1
            continue
        
        # query the API for article data
        log(getCurrentRunTime() + " querying article " + str(articleID) + "...")
        articleData.append(json.loads(requests.get("https://hacker-news.firebaseio.com/v0/item/" + str(articleID) + ".json").text))

        # print out latest
        latest = articleData[len(articleData) - 1]
        index += 1
        
        log(getCurrentRunTime() + " \"" + safe(latest["title"]) + "\" - " + str(index) + "/" + str(numArticles))
                
        # save temporary files
        saved.append(articleID)
        saveDataset(True) # save temp in case of failure

log("\n" + getCurrentRunTime() + " Initializing scraper...")

loadSaved()
obtainNewArticles()
printArticleCount()
retrieveArticleData()
saveDataset()

log("\n" + getCurrentRunTime() + " Scrape completed successfully!\n")
