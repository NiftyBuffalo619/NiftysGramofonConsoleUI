import json

class Config():
    username = ""
    password = ""
    def __init__(self, filepath):
        """Load the config file"""
        self.load_config(filepath)

    def load_config(self,filepath):
        if filepath == "":
            filepath == "config.json"
        try:
            with open(filepath, "r") as json_file:
                data = json.load(json_file)
                self.username = data["username"]
                self.password = data["password"]
        except:
            """Error"""