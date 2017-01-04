import time
import sys
import datetime
import os

class Utils:

    FULL_LOG = True
    OVERWRITE_LOGS = False
    
    timePoints = {} # holds the starting time.clock()'s 
    logs = {} # holds the open file pointers
    
    workFolder = "./"

    def __init__(self, workFolder):
        self.workFolder = workFolder

        # take away trailing slash if supplied
        lastLetter = workFolder[len(workFolder) - 1]
        if lastLetter == "/" or lastLetter == "\\":
            self.workFolder = workFolder[:-1]

        self.setupWorkFolder()

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

    # NOTE: if a name that's already in use is passed in, this will reset that
    # name to the current time
    def makeTimePoint(self, name):
        #if name in self.timePoints: return False
        self.timePoints[name] = time.clock()
        return True

    def getTime(self, name):
        if name not in self.timePoints: return "-1"
        timespan = time.clock() - self.timePoints[name]
        stringtime = "{0:.3f}".format(timespan)
        return stringtime

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
