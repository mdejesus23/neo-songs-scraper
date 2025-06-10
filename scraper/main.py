import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep

BASE_URL = "https://neocatechumenalway.wixsite.com/song/liturgical"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_song_links():
    print(f"🔍 Fetching song list from: {BASE_URL}")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    anchors = soup.find_all('a', href=True)
    song_links = []
    
    for a in anchors:
        href = a['href']
        if "song/cantos/" in href:
            song_links.append((a.text.strip(), href))
    
    print(f"🎶 Found {len(song_links)} song links.")
    print(f"🔗 Example link: {song_links[0] if song_links else 'None'}")
    return song_links

def download_image(image_url, filename):
    try:
        os.makedirs("images", exist_ok=True)
        filepath = os.path.join("images/liturgical", filename)
        res = requests.get(image_url, headers=HEADERS)
        with open(filepath, 'wb') as f:
            f.write(res.content)
        print(f"✅ Saved image: {filename}")
    except Exception as e:
        print(f"❌ Failed to download image: {e}")

def extract_image_url(subpage_url):
    try:
        print(f"🌐 Visiting: {subpage_url}")
        res = requests.get(subpage_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')

        wow_images = soup.find_all('wow-image')

        for tag in wow_images:
            img = tag.find('img', src=True)
            if img and "static.wixstatic.com/media" in img['src']:
                # Check if width attribute is 800
                if img.has_attr('width') and img['width'] == '800':
                    return img['src'], img.get('alt', 'song_image.jpg')
                
                # Or check if URL includes w_800 or w_800h_ (width 800)
                if '/w_800' in img['src']:
                    return img['src'], img.get('alt', 'song_image.jpg')

        print("❌ No valid 800px width image found in <wow-image> tags.")

    except Exception as e:
        print(f"⚠️ Error scraping image: {e}")

    return None, None

def run():
    links = get_song_links()
    
    for title, url in links:
        img_url, alt = extract_image_url(url)
        if img_url:
            safe_title = title.replace(' ', '_').replace('/', '_')
            ext = os.path.splitext(urlparse(img_url).path)[1]
            filename = f"{safe_title}{ext}"
            download_image(img_url, filename)
            sleep(1)  # Be polite to the server

if __name__ == "__main__":
    run()
