from configparser import ConfigParser
import os

for _, _, file in os.walk("icons"):
    images: list = file

print(images)