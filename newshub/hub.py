from newshub.utils import Utils
from newshub.hn_scraper import HNScraper
from newshub.filters import Filters
from newshub.manual_classifier import ManualClassifier

class Hub:

    utils = None
    runName = ""
    
    def __init__(self, workFolder):
        print("----------------------------------------")
        self.utils = Utils(self, workFolder)
        self.utils.makeTimePoint("hub")
        self.utils.log("hub", "Initializing hub...")
        
    def __del__(self):
        try:
            self.utils.dumpLogs()
        except: print("@ WARNING! - deconstructor failed.")
        print("========================================")

    def setRunName(self, runName):
        self.runName = runName
        self.utils.log("hub", "Set run name to \"" + self.runName + "\"")

    def getHNScraper(self):
        scraper = HNScraper(self.utils)
        return scraper

    def getFilters(self):
        filters = Filters(self.utils)
        #filters.loadDataset()
        return filters

    def getManualClassifier(self):
        classifier = ManualClassifier(self.utils)
        return classifier

    def getLSTMClassifier(self):
        classifier = LSTMClassifier(self.utils)
        return classifier
