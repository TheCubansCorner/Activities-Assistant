from configparser import ConfigParser

import os

config = ConfigParser()
config.read(os.path.join("config", "config_activities.ini"))


print(config["KEYS"]["alphabet"])