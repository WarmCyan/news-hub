import json

class ManualClassifier:

    utils = None
    runName = ""

    originalData = []
    workingData = []

    usedTags = []

    displayCols = []

    def __init__(self, utils):
        self.utils = utils
        self.log("Setting up manual classifier...") 
    
    def loadDataset(self):
        self.log("Attempting to load dataset...")
        
        try:
            dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_cleaned.json", 'r')
            self.originalData = json.loads(dataFile.read())
            dataFile.close()

            self.log("Successfully loaded dataset!")

            self.workingData = self.originalData.copy()
        except Exception as e:
            self.log("ERROR - Failed to load dataset - " + str(e))

    def loadSave(self):
        self.log("Attemping to load previous classification session...")
        try:
            dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_classified_temp.json", 'r')
            self.workingData = json.loads(dataFile.read())
            dataFile.close()
            
            saveFile = open(self.utils.workFolder + "/data/" + self.runName + "_classified_session.json", 'r')
            saveData = json.loads(saveFile.read())

            self.originalData = saveData["originalData"]
            self.usedTags = saveData["usedTags"]
            self.displayCols = saveData["displayCols"]
        except Exception as e:
            self.log("ERROR - Failed to load previous session - " + str(e))

    def saveDataset(self, temp=False):
        try:
            dataFile = None
            if temp: dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_classified_temp.json", 'w')
            else: dataFile = open(self.utils.workFolder + "/data/" + self.runName + "_classified.json", 'w')


            dataFile.write(json.dumps(self.workingData))
            dataFile.close()

            if temp:
                saveFile = open(self.utils.workFolder + "/data/" + self.runName + "_classified_session.json", 'w')
                saveData = {"originalData":self.originalData, "usedTags":self.usedTags, "displayCols":self.displayCols}
                saveFile.write(json.dumps(saveData))
                saveFile.close()
            else:
                tagsFile = open(self.utils.workFolder + "/data/" + self.runName + "_classified_tags.json", 'w')
                tagsFile.write(json.dumps(self.usedTags))
                tagsFile.close()
            
        except Exception as e:
            self.log("ERROR - Failed to save dataset - " + str(e))

    # displayCols = which cols to display before prompting for user input

    def resumeClassification(self, runName):
        self.runName = runName
        self.log("Resuming classification session...")
        self.loadSave()
        self.classify()

    def startClassification(self, runName, displayCols):
        self.runName = runName
        self.displayCols = displayCols
        self.log("Starting classification session...")
        self.loadDataset()
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
            #print(self.utils.printify(promptString))
            
            #promptString = ""
            for col in row:
                if col in self.displayCols:
                    print("(" + col + ") \"" + self.utils.printify(row[col]) + "\"")
                    #promptString += "|" + col + ": " + row[col] + " "
            

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
            self.saveDataset(True)
        self.saveDataset()

    def log(self, msg):
        self.utils.log("classifier", self.utils.printify(msg))
