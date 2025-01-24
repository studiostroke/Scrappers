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
                writer.writerow(['id', 'Title', 'price', 'Description',"images","SizeChart","weight","ProductCode","Category","Stock"])

                for loc in loc_tags:
                    url_1 = loc.text
                    # url_1 = "https://amnaismail.com/Product-Details/339"
                    response = requests.get(url_1, headers=headers)
                    response.raise_for_status()

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        last_id = url_1.split("/")[-1]
                        title = soup.find("h4", {"class": "js-name-detail"}).get_text(strip=True)
                        price = soup.find("span", {"name": "ProductPrice"}).get_text(strip=True)
                        desc = soup.find("div", {"id": "description"})
                        ul_tag = soup.find("div", {"class": "row"})
                        img_tags = ul_tag.find_all('img')
                        src_links = [img['src'] for img in img_tags]
                        
                        weight = soup.find("p", {"style": "font-weight:bold;padding:20px;"})
                        weight_text = weight.get_text(strip=True)
                        weight_value = weight_text.split(":")[1].strip()
                        product_code = soup.find("span", {"class": "stext-107"})
                        product_code = product_code.get_text(strip=True)
                        product_code = product_code.split(":")[1].strip()
                        category = soup.find("div", {"class": "size-302"})
                        category = category.find_all("span")
                        category = category[1].get_text(strip=True)
                        category= category.split(":")[1].strip()
                        if category.upper() == "SAREE":
                            size = "https://amnaismail.com/Images/1320SAREE SC.jpg"
                        elif category.upper() == "COUTURE":
                            size = "https://amnaismail.com/Images/2584BLACK DRESS.jpg"
                        elif category.upper() == "PISHWAS":
                            size = "https://amnaismail.com/Images/78794054PG PISHWAS.jpg"
                        elif category.upper() == "SEMI FORMAL":
                            size = "https://amnaismail.com/Images/5371SHORT SHIRT & TROUSER.jpg"
                        elif category.upper() == "AKS BY AMNA ISMAIL":
                            size = "https://amnaismail.com/Images/41746SIZE CHART SHALWAR KAMEEZ.jpg"
                        else:
                            size = "Default size chart URL"
                        p_tag = soup.find("p", {"class": "bg-warning"})
                        if p_tag:
                            stock_status = "Out of Stock"
                        else:
                            stock_status = "In Stock"
                        
                        writer.writerow([last_id, title, price, desc, ', '.join(src_links), size, weight_value, product_code, category, stock_status])
                    else:
                        print(f"Failed to retrieve: {url_1} with status code: {response.status_code}")
        else:
            print("No <loc> tags found.")
    else:
        print(f"Failed to retrieve sitemap. Status code: {response.status_code}")

fetch_html_and_get_by_id(url)
