import os
import sqlite3
import xml.etree.ElementTree as ET

import requests
from html2txt import converters


class Data:
    def __init__(self):
        sql_create = """
        create table if not exists file (filename text unique);
        """
        self.data = sqlite3.connect("dltwit.sqlite")
        self.data.executescript(sql_create)

    def isfilename(self, filename):
        sql_select = """
        select count(*) from file where filename=?
        """
        row = self.data.execute(sql_select, (filename,))
        result = row.fetchone()
        return result[0] > 0

    def addfilename(self, filename):
        sql_insert = """
insert into file (filename)
values (?);        """
        self.data.execute(sql_insert, (filename,))
        self.data.commit()


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
            self.blocksize = int(os.environ["twitclubblocksize"])
        except KeyError:
            self.blocksize = 1048576
        try:
            self.twitclubdestination = os.environ["twitclubdestination"]
        except KeyError:
            self.twitclubdestination = os.path.abspath("./")
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
        self.outputFilename = os.path.join(self.twitclubdestination, self.filename)
        self.downloadfilename = os.path.join(
            self.twitclubdestination, "twitclubdownload"
        )

    def cleanTitle(self, title):
        newTitle = str(title)
        badCharacters = "\\/:.+?*"
        for badCharacter in badCharacters:
            newTitle = newTitle.replace(badCharacter, "")
        return newTitle
