import json
import nltk
import re

from nltk.corpus import stopwords

class Filters:
    
    utils = None

    originalData = None
    workingData = None
    
    def __init__(self, utils):
        self.utils = utils
        self.utils.makeTimePoint("filters")
        self.log("Initializing filters...") 

    def loadDataset(self, suffix):
        self.originalData = self.utils.loadDataset(suffix)
        self.workingData = self.originalData.copy()

    def saveDataset(self, suffix):
        self.utils.saveDataset("suffix", self.workingData)

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
                    
                    row[col] = " ".join(newWords)

        self.log("Stopword removal filter completed!")

    def log(self, msg):
        self.utils.log("filters", "(" + self.utils.getTime("filters") + ") :: " + self.utils.printify(msg))
