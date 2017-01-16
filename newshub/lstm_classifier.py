import json
import tensorflow as tf

class LSTMClassifier:
    
    utils = None

    originalData = []
    workingData = []

    def __init__(self, utils):
        self.utils = utils
        self.log("Setting up LSTM classifier...")

    def loadDataset(self, suffix):
        self.originalData = self.utils.loadDataset(suffix)
        self.workingData = self.originalData.copy()

    def classify():
        pass

    def train():
        pass
