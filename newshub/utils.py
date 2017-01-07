import time
import sys
import datetime
import os
import json
import traceback

class Utils:

    FULL_LOG = True
    OVERWRITE_LOGS = False
    
    timePoints = {} # holds the starting time.clock()'s 
    logs = {} # holds the open file pointers
    
    workFolder = "./" # DOES NOT INCLUDE TRAILING SLASH

    hub = None

    def __init__(self, hub, workFolder):
        self.workFolder = workFolder
        self.hub = hub

        # take away trailing slash if supplied
        lastLetter = workFolder[len(workFolder) - 1]
        if lastLetter == "/" or lastLetter == "\\":
            self.workFolder = workFolder[:-1]

        self.setupWorkFolder()

    def handleError(self, e, msg):
        print("# ERROR: " + self.printify(msg))
        print(str(e))
        traceback.print_exc()
        exit()

    def makeDataFileName(self, suffix):
        return self.workFolder + "/data/" + self.hub.runName + "_" + suffix + ".json"

    def setupWorkFolder(self):
        #print("# Setting up work folder...")
        changed = False
        if not os.path.exists(self.workFolder + "/logs"):
            os.makedirs(self.workFolder + "/logs")
            changed = True
        if not os.path.exists(self.workFolder + "/data"):
            os.makedirs(self.workFolder + "/data")
            changed = True
        if changed: print("# Initialized work folders.")

    def loadDataset(self, suffix):
        fileName = self.makeDataFileName(suffix)
        self.log("utils", "Attempting to load dataset \"" + fileName + "\"...")
        
        dataset = None
        try:
            dataFile = open(fileName, 'r')
            dataset = json.loads(dataFile.read())
            dataFile.close()
        except Exception as e: self.handleError("Failed to load dataset.", e)
        self.log("utils", "Successfully loaded dataset!")
        return dataset
        
    def saveDataset(self, suffix, dataset):
        fileName = self.makeDataFileName(suffix)
        self.log("utils", "Attemping to save dataset \"" + fileName + "\"...")

        try:
            dataFile = open(fileName, 'w')
            dataFile.write(json.dumps(dataset))
            dataFile.close()
        except Exception as e: self.handleError("Failed to save dataset.", e)
        
        self.log("utils", "Successfully saved dataset!")

    def loadExtraData(self, suffix):
        fileName = self.makeDataFileName(suffix + "_data")
        self.log("utils", "Attempting to load helper data \"" + fileName + "\"...")

        data = None
        try:
            dataFile = open(fileName, 'r')
            data = json.loads(dataFile.read())
            dataFile.close()
        except Exception as e: self.handleError("Failed to load extra data.", e)
        
        self.log("utils", "Successfully loaded helper data!")
        return data

    def saveExtraData(self, suffix, data):
        fileName = self.makeDataFileName(suffix + "_data")
        self.log("utils", "Attempting to save helper data \"" + fileName + "\"...")
        
        try:
            dataFile = open(fileName), 'w')
            dataFile.write(json.dumps(data))
            dataFile.close()
        except Exception as e: self.handleError("Failed to save helper data.", e)
        
        self.log("utils", "Successfully saved helper data!")
    
    def loadSession(self, suffix):
        fileName = self.makeDataFileName(suffix + "_session")
        self.log("utils", "Attempting to load session \"" + fileName + "\"...")

        sessionData = None
        try:
            dataFile = open(fileName, 'r')
            sessionData = json.loads(dataFile.read())
            dataFile.close()
        except Exception as e: self.handleError("Failed to load session data.", e)

        self.log("utils", "Succsesfully loaded session data!")
        return sessionData

    # suffix should represent what area the data is coming from, not the _temp
    # or _session or whatever. (this function will add that
    def saveSession(self, suffix, verbose, **kwargs):
        fileName = self.makeDataFileName(suffix + "_session")
        if verbose: self.log("utils", "Attempting to save session \"" + fileName + "\"...")

        try:
            dataFile = open(fileName, 'w')
            dataFile.write(json.dumps(kwargs))
            dataFile.close()
        except Exception as e: self.handleError("Failed to save session data.", e)
        
        if verbose: self.log("utils", "Successfully saved session data!")

    # NOTE: if a name that's already in use is passed in, this will reset that
    # name to the current time
    def makeTimePoint(self, name):
        #if name in self.timePoints: return False
        self.timePoints[name] = time.clock()
        return True

    def getTime(self, name):
        if name not in self.timePoints: return "-1"
        timespan = time.clock() - self.timePoints[name]
        #stringtime = "{0:.3f}".format(timespan)
        stringtime = self.makeSaneFloat(timespan)
        return stringtime

    def makeSaneFloat(self, num):
        return "{0:.3f}".format(num)

    # remove any encoding issues for printing object out to console 
    def printify(self, obj):
        try: obj = str(obj) # convert to string first if necessary
        except: pass
        obj = str(obj.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))
        return obj

    def log(self, name, msg):
        if self.FULL_LOG and name != "_FULL_": self.log("_FULL_", name.upper() + " - " + msg)
        
        # get the log file pointer if we haven't written to it before
        if name not in self.logs:
            # determine whether adding to or overwriting log
            mode = 'a'
            if self.OVERWRITE_LOGS: mode = 'w'
            
            # open the log file
            logFile = open(self.workFolder + "/logs/" + name + ".log", mode)
            logFile.write("\n# Opened logfile. (" + str(datetime.datetime.now()) + ")\n")
            self.logs[name] = logFile

        # write to the log
        self.logs[name].write(msg + "\n")
        if name != "_FULL_": print(name.upper() + " - " + self.printify(msg))

    def dumpLogs(self):
        for pointer in self.logs:
            
            try: self.logs[pointer].write("# Closing logfile.\n")
            except: pass
            
            try: self.logs[pointer].close()
            except: print("# ERROR! - Failed to close file pointer '" + self.printify(pointer) + "'")
