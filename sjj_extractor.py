import json

from sjj import SongFetcher, SongScraper

with open("sjj_en.json", 'r') as f:
    data = json.load(f)

print(data[0:2])
baseurl = 'https://www.jw.org/en/library/music-songs/sing-out-joyfully/'
scraper = SongFetcher(baseurl, data) 
soup = scraper.fetch_webpage(baseurl)
urls = scraper.get_urls_song(soup)

for url in urls:  # Limiting to first 2 URLs for demonstration
    song_scraper = SongScraper(url, data)
    title, verse, strophes, verse_else = song_scraper.get_song_lyrics(url)
    if title and strophes:
        song_scraper.song_details(title, verse, strophes, verse_else)
    with open("sjj_en.json", 'w') as f:
        json.dump(data, f, indent=4)