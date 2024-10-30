import os 

class Api_Key_Store:
    def __init__(self):
        self.username = "sgura99@uw.edu"
        self.key = os.getenv("EPA_AQI_API_KEY")
