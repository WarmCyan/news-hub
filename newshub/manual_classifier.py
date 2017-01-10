import json

class ManualClassifier:

    utils = None
    
    originalData = []
    workingData = []

    usedTags = []

    displayCols = []

    def __init__(self, utils):
        self.utils = utils
        self.log("Setting up manual classifier...") 
    
    def loadDataset(self, suffix):
        self.originalData = self.utils.loadDataset("cleaned")
        self.workingData = self.originalData.copy()

    def loadSession(self):
        sessionData = self.utils.loadSession("classified")
        self.workingData = sessionData["workingData"]
        self.originalData = sessionData["originalData"]
        self.usedTags = sessionData["usedTags"]
        self.displayCols = sessionData["displayCols"]

    def saveDataset(self, suffix, temp=False):
        if not temp:
            self.utils.saveDataset(suffix, self.workingData)
            self.utils.saveExtraData(suffix, self.usedTags)
        else:
            self.utils.saveSession("classified", False, workingData=self.workingData, originalData=self.originalData, usedTags=self.usedTags, displayCols=self.displayCols)

    # displayCols = which cols to display before prompting for user input

    def resumeClassification(self):
        self.log("Resuming classification session...")
        self.loadSession()
        self.classify()

    def startClassification(self, displayCols):
        self.displayCols = displayCols
        self.log("Starting classification session...")
        #self.loadDataset()
        self.classify()

    def classify(self):
        self.log("Classifying...")

        index = 0
        for row in self.workingData:
            index += 1

            # skip row if done already
            try:
                if row["classification"] != None:
                    continue
            except:
                pass
            
            
            print("\n" + str(index) + "/" + str(len(self.workingData)))
            print("Previous tags: " + str(self.usedTags))
            
            # display any cols that were requested
            for col in row:
                if col in self.displayCols:
                    print("(" + col + ") \"" + self.utils.printify(row[col]) + "\"")
            
            # get the users tag list
            tagsString = input()
            tags = tagsString.split(",")

            # remove this line from the dataset if no tags supplied
            #if tags[0] == "":
                #self.workingData.remove(row)
                #continue

            #check if not already in used tags list
            for tag in tags:
                if tag not in self.usedTags: self.usedTags.append(tag)
                
            # sort the tags for convenience
            self.usedTags.sort()
            
            row["classification"] = tags
            self.saveDataset("classified", True)
        #self.saveDataset()

    def log(self, msg):
        self.utils.log("classifier", self.utils.printify(msg))
