import os 

class API_KEY_STORE():
    def __init__(self, model):
        self.WIKIMEDIA_ACCESS_TOKEN = str(os.getenv("WIKIMEDIA_ACCESS_TOKEN"))
        self.WIKIMEDIA_CLIENT_SECRET = str(os.getenv("WIKIMEDIA_CLIENT_SECRET"))
        self.WIKIMEDIA_CLIENT_ID = str(os.getenv("WIKIMEDIA_CLIENT_ID"))
        self.WIKIMEDIA_EMAIL_ADDRESS = str(os.getenv("WIKIMEDIA_EMAIL_ADDRESS"))
        self.WIKIMEDIA_ORES_ENDPOINT = f"https://api.wikimedia.org/service/lw/inference/v1/models/{model}:predict"

