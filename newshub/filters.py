import json
import nltk

from nltk.corpus import stopwords

class Filters:
    
    utils = None

    runName = ""

    originalData = None
    workingData = None
    
    #def __init__(self, utils, runName):
    def __init__(self, utils):
        #self.runName = runName
        self.utils = utils
        self.utils.makeTimePoint("filters")
        self.log("Initializing filters...") 

        #self.loadScrapedDataset()
        #self.workingData = self.originalData.copy()
        #self.log(self.workingData)

    def loadScrapedDataset(self, runName):
        self.log("Attempting to load scraped dataset...")
        self.runName = runName

        try:
            dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_scrape.json", 'r')
            self.originalData = json.loads(dataFile.read())
            dataFile.close()

            self.log("Successfully loaded dataset!")
            
            self.workingData = self.originalData.copy()
            # self.log(self.workingData) # DEBUG
            
        except Exception as e:
            self.log("ERROR - failed to load dataset - " + str(e))

    #def checkStopwords(self):
        #try:
            
    def lowercase(self, colNames):
        self.log("")
        self.log("Executing lowercase filter on columns " + self.utils.printify(colNames) + "...")
        for row in self.workingData:
            for col in row:
                if col in colNames:
                    row[col] = row[col].lower()
                    #print(self.utils.printify(row[col])) # DEBUG
        self.log("Lowercase filter completed!")

    def log(self, msg):
        self.utils.log("filters", "(" + self.utils.getTime("filters") + ") :: " + self.utils.printify(msg))
