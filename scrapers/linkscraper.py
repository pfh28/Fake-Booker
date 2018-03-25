import requests
from html.parser import HTMLParser
import json
import time
import random
import sys


class songLinkHTMLParser(HTMLParser):
    in_script = False
    songs = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.in_script = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

    def add_if_new_or_more_voted(self, records, record_info):
        for i in range(len(records)):
            if records[i]['name'] == record_info['name']:       #if the list contains a duplicate
                if records[i]['votes'] <= record_info['votes']: #pick the one with more votes
                    records[i] = record_info
                return                                          #once you've found a match and discarded one, you're done
        records.append(record_info)                             #append if there was no match

    def handle_data(self, data):
        if self.in_script and "window.UGAPP.store.page = " in data:
            try:
                data = data.split("= ", 1)[1]
                parsed_data = json.loads(data[:-2])
                for record in parsed_data['data']['other_tabs']:
                    record_info = {}
                    record_info['name'] = record['song_name']
                    record_info['votes'] = record['votes']
                    record_info['link'] = record['tab_url']
                    self.add_if_new_or_more_voted(self.songs, record_info)
            except TypeError:
                print(TypeError)


class artistLinkHTMLParser(HTMLParser):
    in_script = False
    artists = []

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
                for artist in parsed_data['data']['artists']:
                    self.artists.append(artist['artist_url'])
            except TypeError:
                print(TypeError)


def write_artists_to_file():
    artist_parser = artistLinkHTMLParser()
    artist_url_format = "https://www.ultimate-guitar.com/bands/{}{}.htm"
    artist_count = len(artist_parser.artists)
    with open("artist_urls2.txt", "a") as artistFile:
        for letter in range(ord('v'), ord('v')+1):
            print(chr(letter))
            for number in range(1,201):
                if artist_count > 1000:                 # every 1000 artists
                    for artist in artist_parser.artists:#
                        artistFile.write(artist+"\n")   # write to the file
                    artist_parser.artists = []          # free some memory
                    print("throttle")
                    time.sleep(random.randint(3,10))    # throttle a bit
                page = requests.get(artist_url_format.format(chr(letter), number))
                artist_parser.feed(page.content.decode())
                if artist_count == len(artist_parser.artists):  #if the last page yielded nothing new
                    print(number)
                    break
                else:
                    artist_count = len(artist_parser.artists)
        for artist in artist_parser.artists:  #get last few items
            artistFile.write(artist + "\n")

def get_all_songs_from_artist(url_prototype, parser):
    song_count = len(parser.songs)
    error_count = 0
    for i in range(1,201):
        try:
            page = requests.get(url_prototype.format(i))
            parser.feed(page.content.decode())
            if song_count == len(parser.songs):
                print("pages: "+str(i))
                break                   #no more songs from that artist
            else:
                song_count = len(parser.songs)
        except requests.exceptions.ConnectionError:
            print(requests.exceptions.ConnectionError)
            i -= 1
            time.sleep(10)
            error_count += 1
            if error_count > 10:
                sys.exit(1)


#write_artists_to_file()

song_list_parser = songLinkHTMLParser()
with open("artist_url_list.txt", 'r') as artist_suffixes:
    with open("song_urls.txt", 'a', 1) as out_file:
        for artist_suffix in artist_suffixes:
            url = 'https://www.ultimate-guitar.com'+artist_suffix+'?filter=chords&page={}'
            print(artist_suffix)
            get_all_songs_from_artist(url, song_list_parser)
            for record in song_list_parser.songs:
                out_file.write(record['link']+"\n")
            song_list_parser.songs = []
            time.sleep(random.randint(3,10))
