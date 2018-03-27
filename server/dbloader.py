import pymongo
from server.model.song_model import Song
import scrapers.songscraper as scraper

url = "https://tabs.ultimate-guitar.com/tab/elvis_presley/cant_help_falling_in_love_chords_1086983"
raw_song = scraper.get_raw_song(url)
song = Song(raw_song, url)
song.transpose_up_one()
print(str(song.get_song_text()))