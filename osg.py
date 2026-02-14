import re
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
        titles_div = soup.find_all('div', class_='syn-body')
        titles_label = []
        urls = []
        for a in titles_div:
            titles_a = a.find_all('a')
            link = a.find('a')['href']
            full_url = 'https://www.jw.org' + link
            urls.append(full_url)
            for title in titles_a:
                titel_text = title.get_text(strip=True)
                titles_label.append(titel_text.lower())
        if 'song' in titles_label:
            titles_label.remove('song')

        list_titlesData = [item['title'] for item in self.data]

        for t in list_titlesData:
            t = t.lower()
            if t in titles_label:
                print('Removing duplicate song:', t)
                index = titles_label.index(t)
                print(urls[index])
                del urls[index]
        print(f"Total songs found: {len(urls)}")       
        
        return urls

class SongScraper(SongFetcher):

    def get_song_lyrics(self, url=None):
        r1 = self.fetch_webpage(url or self.base_url)
        if r1 is None:
            print(f"Failed to retrieve {url}")
        else:
            title_tag = r1.find('h1', id ='p1')
            if title_tag:
                title_text = title_tag.get_text(strip=True)

            lirycs_tag = r1.find('ol', class_='source')
            if lirycs_tag:
                lyrics_text = lirycs_tag.get_text(separator='\n', strip=True)
                lyrics_text = re.sub(r'\r', '', lyrics_text).strip()
                strophes = re.split(r'(?=\n?\s*\d+\.\s*|\(BRIDGE\)\s*)', lyrics_text)
                strophes = [strophe.strip() for strophe in strophes if strophe.strip()]
                
            return title_text, strophes
        
    def song_details(self, title, strophes):
        song_data = {
            'id': len(self.data) + 1,
            'title': title,
            'first': strophes[0] if len(strophes) > 0 else "",
            'second': strophes[1] if len(strophes) > 1 else "",
            'third': strophes[2] if len(strophes) > 2 else "",
            'forth': strophes[3] if len(strophes) > 3 else "",
        }
        self.data.append(song_data)
        print(f"Added song: {title}")
        return song_data




if __name__ == '__main__':
    baseurl = 'https://www.jw.org/mg/zavatra-misy/hira-sy-mozika/hira'
    scraper = SongFetcher(baseurl, []) 
    soup = scraper.fetch_webpage(baseurl)
    urls = scraper.get_urls_song(soup)
    print(urls[0:2])  # Limiting to first 2 URLs for demonstration
    lirycs = SongScraper(base_url=urls[0], data= [{
        'id': 1,
        'title': "Ny Mamy Tsy mba ho Lany",
        'first': "1. Raha hoe tsisy namana aho hoatr’izay, dia angamba aho efa tsy hay. \n’Zao kosa aho te ho ando hampahery, ho an’ny hafa indray. \nRaha toa aho ’zao lasa tia tena, dia ho ketraka ny foko. \nRaha toa aho mahafoy tena, fifaliana maro loko, \nFa tsy hitoloko.\n\n(FIVERENANA)\nRaha mbola haiko dia tiako hatao. Raha mbola an’ahy dia tiako ho anao, \nF’izay no tsara ’ndrindra am’izao. \nKa mandrakizay, tsy izao ihany. \nNy fiainako ho hoatr’izany: Ny mamy tsy mba ho lany.",
        'second': "2. Raha mbola misy hery hanao soa ny tanako ankiroa, \nTsy hijanona aho fa handrandrana tady mampifandray ny fo. \nRaha toa aho ’zao lasa tia tena, dia ho ketraka ny foko. \nRaha toa aho mahafoy tena, fifaliana maro loko, \nFa tsy hitoloko. \n\n(FIVERENANA) \nRaha mbola haiko dia tiako hatao. Raha mbola an’ahy dia tiako ho anao, \nF’izay no tsara ’ndrindra am’izao. \nKa mandrakizay, tsy izao ihany. \nNy fiainako ho hoatr’izany: Ny mamy tsy ho lany.",
        'third': "(TETEZANA) \n’Zaho tsy mba hiala, ’zaho tsy hanahy. \nNy fiainako izao no mahasambatra ahy. Sambatra aho, tsisy ahiahy. \n\n(FIVERENANA) \nKa ’zao no hataoko fomba fiaina: Raha misy tsara dia zaraina.\nFaly ny fo, tony ny saina. \nKa mandrakizay, tsy izao ihany. ’Ndao dia ho hitanao: \nNy mamy tsy mba ho lany. \nNy mamy tsy mba ho lany.",
        'forth': "",
        }])
    lirycs.get_song_lyrics()