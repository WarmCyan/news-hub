import time
import sys
import datetime

class Utils:

    timePoints = {} # holds the starting time.clock()'s 
    logs = {} # holds the open file pointers

    def makeTimePoint(self, name):
        if name in self.timePoints: return False
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
        if name not in self.logs:
            logFile = open("logs/" + name + ".log", 'a')
            logFile.write("\n# Opened logfile. (" + str(datetime.datetime.now()) + ")\n")
            self.logs[name] = logFile
        self.logs[name].write(msg + "\n")
        print(name.upper() + " - " + self.printify(msg))
    
    def dumpLogs(self):
        for pointer in self.logs:
            
            try: self.logs[pointer].write("# Closing logfile.")
            except: pass
            
            try: self.logs[pointer].close()
            except: print("# ERROR! - Failed to close file pointer '" + self.printify(pointer) + "'")
    
    def helloThere(self):
        print("Hello there!")
