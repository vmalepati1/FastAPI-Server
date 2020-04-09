import yaml
import os

class ServerConfig:

    def __init__(self):
        self.file = 'server_config.yml'
        self.cache_stamp = 0
        self.config = {}

    def get_config(self):
        stamp = os.path.getmtime(self.file)
        
        if stamp != self.cache_stamp:
            with open(self.file, 'r') as ymlfile:
                self.config = yaml.safe_load(ymlfile)
        
        return self.config
