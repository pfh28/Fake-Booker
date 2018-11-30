import re

from pymongo import MongoClient

from server.model.book_model import SongBook
from server.model.song_model import Song
from server.model.chord_model import Chord
import scrapers.songscraper as scraper
import json

client = MongoClient()  # assumes local
db = client['fake_booker_365']
'''
url = "https://tabs.ultimate-guitar.com/tab/elvis_presley/cant_help_falling_in_love_chords_1086983"
raw_song = scraper.get_raw_song(url)
song = Song(raw_song)
song.transpose_up_one()
print(str(song.get_song_text()))
'''

def complex_handler(obj):
    if hasattr(obj, 'jsonable'):
        return obj.jsonable()


def song_decoder(obj):
    if '__type__' in obj:
        if obj["__type__"] == 'Chord':
            return Chord(obj["string"])
        elif obj["__type__"] == 'Song':
            return Song(obj, is_restore=True)
        elif obj["__type__"] == 'SongBook':
            rv = SongBook(obj['title'], obj['preferred_chords'], obj["_id"])
            for song_id in obj['songs']:
                songs = get_songs_matching({"_id": song_id})
                if len(songs) > 0:
                    rv.add_song(songs[0])
            return rv
    else:
        return obj


'''
serialized = json.dumps(song, default=complex_handler)
print(serialized)
dicted = json.loads(serialized)
ser = json.dumps(dicted)
deserialized = json.loads(serialized, object_hook=complex_decoder)
print(type(deserialized))
'''


def store_song(song):
    collection = db['song']
    serialized = json.dumps(song, default=complex_handler)
    dicted = json.loads(serialized)
    collection.insert(dicted)


def get_songs_matching(search_term):
    collection = db['song']
    sresult = collection.find(search_term)
    rv = []
    for record in sresult:
        serialized = json.dumps(record)
        deserialized = json.loads(serialized, object_hook=song_decoder)
        rv.append(deserialized)
    return rv


def delete_song(song):
    collection = db['song']
    collection.delete_one({"_id": song._id})


def replace_song(song):
    collection = db['song']
    delete_song(song)
    store_song(song)


def store_book(book):
    collection = db['book']
    serialized = json.dumps(book, default=complex_handler)
    dicted = json.loads(serialized)
    collection.insert(dicted)

def get_book_list():
    collection = db['book']
    sresult = collection.find({})
    rv = []
    for record in sresult:
        serialized = json.dumps(record)
        deserialized = json.loads(serialized, object_hook=song_decoder)
        rv.append(deserialized)
    return rv


def delete_book(book):
    collection = db['book']
    collection.delete_one({"_id": book._id})


def replace_book(book):
    collection = db['book']
    delete_book(book)
    store_book(book)

'''
with open("/home/patrick/pfhFiles/PersonalProgramming/python/guitar/fake-booker/scrapers/song_url_all.txt", 'r') as song_file:
    for url in song_file:
        if re.search("https://tabs.ultimate-guitar.com/tab/\w*/\w*", url):
            print(url)
            url_song_data = {}
            url_song_data['url'] = url
            url = url.split("/tab/")[1]
            url_song_data['artist'] = url.split("/")[0].replace("_", " ")
            url_song_data['song_name'] = url.split("/")[1].replace("_", " ")
            song = Song(url_song_data, is_restore=True)
            store_song(song)


with open("/home/patrick/pfhFiles/PersonalProgramming/python/guitar/fake-booker/scrapers/InFile.txt", 'r') as song_file:
    for url in song_file:
        raw_song = scraper.get_raw_song(url)
        song = Song(raw_song)
        store_song(song)
'''
