from newshub.utils import Utils

class Hub:

    utils = None
    
    def __init__(self, workFolder):
        print("----------------------------------------")
        self.utils = Utils(workFolder)
        self.utils.makeTimePoint("hub")
        self.utils.log("hub", "Initializing hub...")
        
    def __del__(self):
        try:
            self.utils.dumpLogs()
        except: print("@ WARNING! - deconstructor failed.")
        print("========================================")

    def Test(self):
        print("Hello there from HubWorld!")
