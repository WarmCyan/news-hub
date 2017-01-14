import newshub as nh
import time

hub = nh.Hub("./space")
hub.setRunName("first")

#scraper = hub.getHNScraper()
#scraper.articleMode = "new"
#scraper.numArticles = 10
#scraper.scrape()
#scraper.saveDataset("scrape")
#scraper.resume()

#filters = hub.getFilters()
#filters.loadDataset("scrape")
#filters.copyCol("title", "title_cleaned")
#filters.lowercase(["title_cleaned"])
#filters.replaceNonLetters(["title_cleaned"])
#filters.removeStopwords(["title_cleaned"])
#filters.saveDataset("cleaned")

classifier = hub.getManualClassifier()
#classifier.loadDataset("cleaned")
#classifier.startClassification(["title", "title_cleaned"])
classifier.resumeClassification()
classifier.saveDataset("classified")


#from newshub import Hub
#from newshub.utils import *

#hub = nh.Hub()
#hub.Test()

#nh.utils.HelloThere()
#utils = nh.Utils()
#utils.makeTimePoint("run")

#utils.helloThere()

#utils.log("run", "Attempting to sleep...")
#time.sleep(.001)
#utils.log("run", "Slept successfully!")


#print("run time: " + utils.getTime("run"))
#utils.dumpLogs()
