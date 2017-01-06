import json
import nltk
import re

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

    def saveWorkingDataset(self):
        try:
            dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_cleaned.json", 'w')
            dataFile.write(json.dumps(self.workingData))
            dataFile.close()

        except Exception as e:
            self.log("ERROR - Failed to save dataset - " + str(e))

    #def checkStopwords(self):
        #try:

    def copyCol(self, colName, newColName):
        self.log("")
        self.log("Copying '" + colName + "' to new column '" + newColName + "'...")
        for row in self.workingData:
            row[newColName] = row[colName]
        self.log("Column data copied.")
            
    # turns every letter to lowercase 
    def lowercase(self, colNames):
        self.log("")
        self.log("Executing lowercase filter on columns " + self.utils.printify(colNames) + "...")
        for row in self.workingData:
            for col in row:
                if col in colNames:
                    row[col] = row[col].lower()
                    # print(self.utils.printify(row[col])) # DEBUG
        self.log("Lowercase filter completed!")

    # replaces every non-letter with a space
    def replaceNonLetters(self, colNames):
        self.log("")
        self.log("Executing non-letter replacement filter on columns " + self.utils.printify(colNames) + "...")
        for row in self.workingData:
            for col in row:
                if col in colNames:
                    row[col] = re.sub("[^a-zA-Z]", " ", row[col])
                    # print(self.utils.printify(row[col])) # DEBUG
        self.log("Non letter replacement filter completed!")

    def removeStopwords(self, colNames):
        self.log("")
        self.log("Executing stopword removal filter on columns " + self.utils.printify(colNames) + "...")
        
        for row in self.workingData:
            for col in row:
                if col in colNames:
                    # split into word array
                    words = row[col].split(" ")
                    newWords = []
                    for word in words: 
                        if word not in stopwords.words("english") and word != " " and word != "":
                            newWords.append(word)
                    
                    # turn into a string
                    wordsString = ""
                    for word in newWords:
                        wordsString += word + " "

                    # reassign
                    #print(wordsString.strip()) # DEBUG
                    row[col] = wordsString.strip() 

        self.log("Stopword removal filter completed!")

    def log(self, msg):
        self.utils.log("filters", "(" + self.utils.getTime("filters") + ") :: " + self.utils.printify(msg))
