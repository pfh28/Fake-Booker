import random
import time
from pprint import pprint

import requests
from html.parser import HTMLParser
import json
import re


class MyHTMLParser(HTMLParser):
    in_script = False
    song_data = {}

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.in_script = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_script and "window.UGAPP.store.page = " in data:
            try:
                data = data.split("= ", 1)[1]
                parsed_data = json.loads(data[:-2])
            #    pprint(parsed_data["data"]['tab_view']['wiki_tab']['content'])
                self.song_data['rating'] = parsed_data["data"]["tab"]["rating"]
                self.song_data['favorites'] = parsed_data["data"]["tab_view"]["stats"]["favorites_count"]
                self.song_data['views'] = parsed_data["data"]["tab_view"]["stats"]["view_total"]
                self.song_data['votes'] = parsed_data["data"]["tab"]["votes"]
                self.song_data['song_name'] = parsed_data["data"]['tab']['song_name']
                self.song_data['artist'] = parsed_data["data"]['tab']['artist_name']
                self.song_data['song'] = parsed_data["data"]['tab_view']['wiki_tab']['content']
            except TypeError:
                self.song_data = None
        #    print(trimmed_data['song'].replace('[ch]', '').replace('[/ch]',''))
        #    print(parsed_data["data"]['tab_view']['wiki_tab']['content'])


def get_raw_song(url):
    page = requests.get(url)
    parser = MyHTMLParser()
    parser.feed(page.content.decode())
    rv = parser.song_data
    rv['url'] = url
    return rv

get_raw_song("https://tabs.ultimate-guitar.com/tab/queen/bohemian_rhapsody_chords_40606")