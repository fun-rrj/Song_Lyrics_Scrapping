import json

from osg import SongFetcher, SongScraper

with open("osg_en.json", 'r') as f:
    data = json.load(f)

baseurl = 'https://www.jw.org/en/library/music-songs/original-songs/'
scraper = SongFetcher(baseurl, data) 
soup = scraper.fetch_webpage(baseurl)
urls = scraper.get_urls_song(soup)

for url in urls:
    song_scraper = SongScraper(url, data)
    title, strophes = song_scraper.get_song_lyrics(url)
    if title and strophes:
        song_scraper.song_details(title, strophes)
    with open("osg_en.json", 'w') as f:
        json.dump(data, f, indent=4)