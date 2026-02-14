import re
from unicodedata import digit
import requests
from bs4 import BeautifulSoup

class SongFetcher:
    def __init__(self, base_url, data):
        self.base_url = base_url
        self.data = data
    
    def fetch_webpage(self, url):
        
        r = requests.get(url or self.base_url)
        if r.status_code != 200:
            print(f"Failed to retrieve the webpage: {self.base_url}")
            return None
        print(f"Webpage retrieved successfully: {self.base_url}")
        return BeautifulSoup(r.content, 'html.parser')
    
    def get_urls_song(self, soup):
        titles_div = soup.find_all('div', class_='musicFileContainer')

        titles_label = []
        urls = []
        for a in titles_div:
            titles_a = a.find_all('a')
            link = a.find('a')['href']
            full_url = 'https://www.jw.org' + link
            urls.append(full_url)
            for title in titles_a:
                titel_text = title.get_text(strip=True)
                titel_text = re.sub(r'\s+\(.*?\)$', '', titel_text)  # Remove trailing parenthetical info
                while titel_text[0].isdigit() or titel_text[0] in ['.', ' ']:
                    titel_text = titel_text[1:].strip()  # Remove leading number and dot
                titles_label.append(titel_text)
        print(f'total songs found: {len(titles_label)}')
        if 'chanson' in titles_label:
            titles_label.remove('chanson')
        
        print(f'total songs found before removing duplicates: {len(titles_label)}')

        list_titlesData = [item['title'] for item in self.data]
        print(f'longueur des titre existants: {len(list_titlesData)}')

        for t in list_titlesData:
            print('Checking for duplicate song:', t)

            #t = t.lower()
            if t in titles_label:
                print('Removing duplicate song:', t)
                index = titles_label.index(t)
                print(f'index', index)
                del urls[index]
                titles_label.remove(t)
                print(len(urls), len(titles_label))
        print(f"Total songs found: {len(urls)}")       
        
        return urls

class SongScraper(SongFetcher):

    def get_song_lyrics(self, url=None):
        strophes = []
        verse_else_text = ""
        title_text = ""
        verse_text = ""
        r1 = self.fetch_webpage(url or self.base_url)
        if r1 is None:
            print(f"Failed to retrieve {url}")
        else:
            title_tag = r1.find('h1', id ='p2')
            if title_tag:
                title_text = title_tag.get_text(strip=True)

            verse_tag = r1.find('p', id ='p3')
            if verse_tag:
                verse_text = verse_tag.get_text(strip=True)
                print(verse_text)

            lirycs_tag = r1.find('ol', class_='source')
            if lirycs_tag:
                lyrics_text = lirycs_tag.get_text(separator='\n', strip=True)
                lyrics_text = re.sub(r'\r', '', lyrics_text).strip()
                strophes = re.split(r'(?=\n?\s*\d+\.\s*|\(BRIDGE\)\s*)', lyrics_text)
                strophes = [strophe.strip() for strophe in strophes if strophe.strip()]
                print(f"Total strophes found: {len(strophes)}")
            
            verse_else = r1.find('div', class_ ='closingContent')
            if verse_else:
                verse_else_text = verse_else.get_text(strip=True)
                print(verse_else_text)

        return title_text, verse_text, strophes, verse_else_text
        
    def song_details(self, title, verse, strophes, verse_else):
        song_data = {
            'id': len(self.data) + 1,
            'title': title,
            'verse': verse,
            'first': strophes[0] if len(strophes) > 0 else "",
            'second': strophes[1] if len(strophes) > 1 else "",
            'third': strophes[2] if len(strophes) > 2 else "",
            'forth': strophes[3] if len(strophes) > 3 else "",
            'verse_else': verse_else
        }
        self.data.append(song_data)
        print(f"Added song: {title}")
        print(song_data)
        return song_data




if __name__ == '__main__':
    baseurl = 'https://www.jw.org/mg/zavatra-misy/hira-sy-mozika/mihira-aminny-fo-hoani-jehovah/'
    scraper = SongFetcher(baseurl, []) 
    soup = scraper.fetch_webpage(baseurl)
    urls = scraper.get_urls_song(soup)
    print(urls)  # Limiting to first 2 URLs for demonstration
    lirycs = SongScraper(base_url=urls[0], data= [])
    lirycs.get_song_lyrics()