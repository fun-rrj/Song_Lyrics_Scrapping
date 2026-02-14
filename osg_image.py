import os
import re
import requests
from bs4 import BeautifulSoup

from osg import SongFetcher

if not os.path.exists('images_scrapees'):
            os.makedirs('images_scrapees')

class ImageFetcher:
    def __init__(self, base_url, save_directory='images_scrapees'):
        self.base_url = base_url
        self.save_directory = save_directory

    
    def fetch_webpage(self, url):
        
        r = requests.get(url or self.base_url)
        if r.status_code != 200:
            print(f"Failed to retrieve the webpage: {self.base_url}")
            return None
        print(f"Webpage retrieved successfully: {self.base_url}")
        return BeautifulSoup(r.content, 'html.parser')
    

    def get_image_urls(self, soup):
        image_url = []
        titles_div = soup.find_all('div', class_='syn-body')
        urls = []
        i = 0
        for a in titles_div:
            link = a.find('a')['href']
            full_url = 'https://www.jw.org' + link
            urls.append(full_url)
        print(f"Total pages found for images: {len(urls)}")
        
        for url in urls:
            i += 1
            print(f"Processing page {i}: {url}")
            r = requests.get(url)
            if r.status_code != 200:
                print(f"Failed to retrieve the webpage: {url}")
                continue
            page_soup = BeautifulSoup(r.content, 'html.parser')
            img_tag = page_soup.find('div', class_='main-wrapper').find('img')
            if img_tag and 'src' in img_tag.attrs:
                img_src = img_tag['src']
                if not img_src.startswith('http'):
                    img_src = 'https://www.jw.org' + img_src
                image_url.append(img_src)
                print(f"Found image URL: {img_src}")
            else:
                print(f"No image found on page: {url}")
        return image_url

    def download_image(self, url):
        r = requests.get(url)
        ext = url.split('.')[-1]
        filename = f'images_scrapees/image_{url.split("/")[-1]}.{ext}'
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
            print(f"Image downloaded successfully: {filename}")
        else:
            print(f"Failed to download image: {url}")

    


if __name__ == "__main__":
    base_url = 'https://www.jw.org/en/library/music-songs/original-songs/'
    fetcher = ImageFetcher(base_url, save_directory='images_scrapees')
    soup = fetcher.fetch_webpage(url=None)
    if soup:
        image_urls = fetcher.get_image_urls(soup)
        for url in image_urls[0:5]:  # Print first 5 image URLs as a sample
            print(url)
    
        for url in image_urls:
            fetcher.download_image(url=url)

    
