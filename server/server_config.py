import yaml
import os

# Enables access to the server config YAML file and automatically reloads changes
# each time get_config is called if necessary.
class ServerConfig:

    def __init__(self):
        # Path to the server config file
        self.file = 'server_config.yml'
        # Last timestamp file was updated
        self.cache_stamp = 0
        # Dictionary containing config info (database credentials, token
        # configs, etc.)
        self.config = {}

    def get_config(self):
        # Get the time when the config was last modified
        stamp = os.path.getmtime(self.file)

        # If we have not loaded in the current changes, reload the file
        if stamp != self.cache_stamp:
            with open(self.file, 'r') as ymlfile:
                self.config = yaml.safe_load(ymlfile)
        
        return self.config
