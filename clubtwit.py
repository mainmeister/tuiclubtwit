import os
import xml.etree.ElementTree as ET
import requests
from html2txt import converters

class Shows:
    def __init__(self):
        try:
            self.url = os.environ["twitcluburl"]
        except KeyError:
            print(
                "Set environment string twitcluburl to the url for your twitclub stream"
            )
            quit(1)
        try:
            self.streamer = os.environ["twitclubstreamer"]
        except KeyError:
            print("Set environment string twitclubstreamer to the command line to stream the url")
            print("For example:")
            print("\tvlc {url}")
            quit(2)
        r = requests.get(self.url)
        self.root = ET.fromstring(r.text)

    def shows(self):
        for show in self.root.iter("item"):
            self.item(show)
            yield show

    def item(self, show):
        self.description = converters.Html2Markdown().convert(
            show.find("description").text
        )
        self.title = self.cleanTitle(show.find("title").text)
        self.pubDate = show.find("pubDate").text
        self.enclosure = show.find("enclosure")
        self.url = self.enclosure.attrib["url"]
        self.urllength = self.enclosure.attrib["length"]
        self.urltype = self.enclosure.attrib["type"]
        self.filename = self.title + ".mp4"

    def cleanTitle(self, title):
        newTitle = str(title)
        badCharacters = "\\/:.+?*"
        for badCharacter in badCharacters:
            newTitle = newTitle.replace(badCharacter, "")
        return newTitle
