import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv

url = "https://usamaahmad.info/sitemap.xml"
# target_id = "sitemap"

def fetch_html_and_get_by_id(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    response = requests.get(url, headers=headers)  # Added headers to the request for better compatibility
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        
        # Find all <loc> elements in the XML and print their text content
        loc_tags = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')  # Find all <loc> tags in the XML
        if loc_tags:
            with open('sitemap_links.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write a header row for the CSV
                writer.writerow(['URL', 'Title', 'Image', 'Description',"Technology"])

                for loc in loc_tags:
                    url_1 = loc.text
                    response = requests.get(url_1, headers=headers)
                    response.raise_for_status()

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title = "elementskit-section-title"
                        img = "blog-image"
                        desc = "blog-container"
                        texch = "info-container"
                        # Extracting the elements based on class names
                        element = soup.find(class_=title)
                        element1 = soup.find(class_=img)
                        element2 = soup.find(class_=desc)
                        element3 = soup.find(class_=texch)
                        # Write the extracted data into the CSV
                        writer.writerow([url_1, element , element1['src'] if element1 else "", element2, element3])
                    
                    else:
                        print(f"Failed to retrieve: {url_1} with status code: {response.status_code}")
        else:
            print("No <loc> tags found.")
    else:
        print(f"Failed to retrieve sitemap. Status code: {response.status_code}")

fetch_html_and_get_by_id(url)
