import newshub as nh
import time

hub = nh.Hub("./test")
scraper = hub.getHNScraper()

scraper.articleMode = "new"
scraper.numArticles = 10
scraper.scrape("test")

#scraper.resume("test")

filters = hub.getFilters()
filters.loadScrapedDataset("test")

filters.copyCol("title", "title_cleaned")
filters.lowercase(["title_cleaned"])
filters.replaceNonLetters(["title_cleaned"])
filters.removeStopwords(["title_cleaned"])
filters.saveWorkingDataset()
#print(hub.utils.printify(filters.workingData))




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
