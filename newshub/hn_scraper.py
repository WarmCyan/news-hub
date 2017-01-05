import requests
import json
import sys
import time

from newshub.utils import Utils

class HNScraper:

    utils = None
    runName = ""

    numArticles = -1 # use -1 to represent getting as many as it can
    articleMode = "top" # set to 'new' to get newest instead   

    articleIDList = None
    articleData = []
    obtainedIDList = [] # ID's for which we've retrieved data (for resuming from later point)

    retrievalTimes = []
    averageRetrievalTime = None
    totalTime = None

    def __init__(self, utils):
        self.utils = utils

    def saveDataset(self, temp=False):
        try:
            # write the article data
            dataFile = None
            if temp: dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_scrape_temp.json", 'w')
            else: dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_scrape.json", 'w')
            dataFile.write(json.dumps(self.articleData))
            dataFile.close()

            # write the list of already obtained IDs
            idlist = {"articleIDList":self.articleIDList, "obtainedIDList":self.obtainedIDList, "numArticles":self.numArticles}
            saveFile = open(self.utils.workFolder + "/data/" + self.runName + "_scrape_idlist.json", 'w')
            saveFile.write(json.dumps(idlist))
            saveFile.close()
        except Exception as e:
            self.log("ERROR - Failed to save dataset - " + str(e))

    def loadDataset(self):
        self.log("Attempting to load previous dataset to continue from...")
        try:
            # get the id lists
            saveFile = open(self.utils.workFolder + "/data/" + self.runName + "_scrape_idlist.json", 'r')
            idlist = json.loads(saveFile.read())
            saveFile.close()
            
            self.articleIDList = idlist["articleIDList"]
            self.obtainedIDList = idlist["obtainedIDList"]
            self.numArticles = idlist["numArticles"]
            
            # get the dataset
            dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_scrape_temp.json", 'r')
            self.articleData = json.loads(dataFile.read())
            dataFile.close()
            
            self.log("Successfully read previous data files!")
            
        except Excetion as e:
            self.log("ERROR - failed to load previous dataset - " + str(e))

    def obtainArticleIDList(self):
        self.log("Querying " + self.articleMode + " stories...")
        page = requests.get("https://hacker-news.firebaseio.com/v0/" + self.articleMode + "stories.json")
        self.articleIDList = json.loads(page.text)
        if self.numArticles == -1:
            self.numArticles = len(self.articleIDList)
         
        self.log("Obtained story list")

    def printArticleCount(self):
        self.log("Found " + str(self.numArticles) + " articles")

    # cut down if a numArticles had been specified
    def trimArticles(self):
        self.articleIDList = self.articleIDList[:self.numArticles]

    def calculateAverageRetrievalTime(self):
        totalSum = 0
        for number in self.retrievalTimes:
            totalSum += number
        average = float(totalSum) / float(len(self.retrievalTimes))
        return average

    def fillStats(self):
        self.averageRetrievalTime = self.utils.makeSaneFloat(self.calculateAverageRetrievalTime())
        self.totalTime = self.utils.getTime("scrape")

    def printStats(self):
        self.log("Average article query time: " + self.averageRetrievalTime + " seconds")
        self.log("Total scrape time: " + self.totalTime + " seconds")

    def retrieveArticleData(self):
        index = 0
        for articleID in self.articleIDList:
            index += 1
            
            # check if this article has already been obtained before
            if articleID in self.obtainedIDList:
                continue

            # query the Attempting for article data
            startTime = time.clock()
            self.log("Querying article " + str(articleID) + "...")
            self.articleData.append(json.loads(requests.get("https://hacker-news.firebaseio.com/v0/item/" + str(articleID) + ".json").text))
            retrievalTime = time.clock() - startTime
            self.retrievalTimes.append(retrievalTime)

            # print out data on the article just retrieved
            latest = self.articleData[len(self.articleData) - 1]

            #self.log("\"" + self.utils.printify(latest["title"]) + "\" - " + str(index) + "/" + str(self.numArticles))
            self.log("\tArticle obtained. - " + str(index) + "/" + str(self.numArticles))
            self.obtainedIDList.append(articleID)
            self.saveDataset(True)

    def scrape(self, runName):
        self.runName = runName
        self.utils.makeTimePoint("scrape")
        self.log("Starting Hacker News scraper...")
        self.log("")
        self.obtainArticleIDList()
        self.printArticleCount()
        self.trimArticles()
        self.retrieveArticleData()
        self.saveDataset()
        self.fillStats()
        self.log("")
        self.log("Scrape complete.")
        self.printStats()

    def resume(self, runName):
        self.runName = runName
        self.utils.makeTimePoint("scrape")
        self.log("Resuming previous Hacker News scraper run...")
        self.log("")
        self.loadDataset()
        self.retrieveArticleData()
        self.saveDataset()
        self.fillStats()
        self.log("")
        self.log("Scrape complete.")
        self.printStats()

    def log(self, msg):
        self.utils.log("scrape", "(" + self.utils.getTime("scrape") + ") :: " + self.utils.printify(msg))
