import os
import re

import feedparser
import paho.mqtt.publish as publish
#from dotenv import load_dotenv

# .env file
#load_dotenv()

#auth = {'username':os.getenv("USERNAME"), 'password': os.getenv("PASSWORD")}

topic = "coronavirus/vaccinatie"
broker = "192.168.0.9"

def update_year(value):
    # TODO TLS support inbouwen
    publish.single(payload=value, topic=topic, hostname=broker, tls=None)

def rss_checker():
    rss_feed = feedparser.parse("https://www.rivm.nl/nieuws/rss.xml")

    for message in rss_feed.entries:
        # Pak datum uit titel als
        # "(...) 19XX uitgenodigd voor coronavaccinatie"
        match = re.search(r"((\b19[0-9]{2})|(\b200[0-9]))(?=\suitgenodigd)", message.title)
        if match:
            update_year(match.group())
            break

if __name__ == '__main__':
    rss_checker()
