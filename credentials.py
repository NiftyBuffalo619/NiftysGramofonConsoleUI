from config import Config
import os
import base64

class credentials:
    def __init__(self):
        config = Config(os.path.abspath("config.json"))
        self.username = config.username
        self.password = config.password
        credentials = f"{self.username}:{self.password}"
        credentials_bytes = credentials.encode("utf-8")
        self.base64_credentials = base64.b64encode(credentials_bytes).decode("utf-8")