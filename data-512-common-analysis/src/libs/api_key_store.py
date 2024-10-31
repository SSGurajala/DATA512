import os 

class Api_Key_Store:
    def __init__(self):
        self.username = os.getenv("EPA_AQI_API_USERNAME")
        self.key = os.getenv("EPA_AQI_API_KEY")
