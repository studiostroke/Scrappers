import requests
from bs4 import BeautifulSoup
import csv
def scrape_amazon_product(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, "lxml")

    try:
        title = soup.find(id="productTitle").get_text(strip=True)
    except AttributeError:
        title = None

    try:
        price = soup.find("span", {"class": "a-price-whole"}).get_text(strip=True)
    except AttributeError:
        price = None

    try:
        rating = soup.find("span", {"class": "a-icon-alt"}).get_text(strip=True)
    except AttributeError:
        rating = None
    try:
        img = soup.find("div", {"class": "imageBlockRearch"})
    except AttributeError:
        img = None
    try:
        desc = soup.find("div", {"class": "centerColAlign"})
    except AttributeError:
        desc = None
    
    with open('amazon_product_detail.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Title', 'price', 'rating', 'Images','Description'])
        writer.writerow([title, price , rating, img, desc])
url = "https://www.amazon.com/Robux-Roblox-Online-Game-Code/dp/B07RZ74VLR/ref=sr_1_2?_encoding=UTF8&content-id=amzn1.sym.860dbf94-9f09-4ada-8615-32eb5ada253a&dib=eyJ2IjoiMSJ9.tzZE9RdE5p_lzPJ0Hx3KnFExVI5yfo95OrD7GXgjw8uy8ZhNxarWY1NxpkoasY5wjLfVxb2_910DKeL-U4IYvneA2c5IwDtCfAQphgt29boQGLn1DNnlALgAlUviPVyh2mAOtLbgPjOlO2vpb7IwE0wQbZzjSUwzao6PWhK4cb6PSk_Sc8n2G2R_K4-1ROmW7WKw-_-0PHCh4hyTFNTmZPLAMrG81Sjk8x3SwcojiNHWDWLCLGqVSv-0kKTOCPttewZiE7QSm2JcFWjT09hx4ZecFSG3_WbNW0wJWlNxWiEGqAPXIuZjCjN2GZXn20y-tlkIIVVqF2WNsRio1bzLzBl-d1odoejMD1Dx1iFg8Bdxx1JIDhItoUIYbORpoHKGcGq_FY2sHMHwEPszO1Jfhv8LRrNvley7_Lr09Q-IyDrjPTR7EPP7r76pJChwQkzi.jBdLFZNKzLu7Utvlu21469gWfn47NoBJcecQiOvJnRs&dib_tag=se&keywords=gaming&pd_rd_r=c0cd0fdd-5f3c-40db-8884-060bc49edf68&pd_rd_w=Eez5n&pd_rd_wg=EfMMu&pf_rd_p=860dbf94-9f09-4ada-8615-32eb5ada253a&pf_rd_r=QHBWJFEPYBBJV9GRGWSP&qid=1737463353&sr=8-2&th=1"  # Replace with a valid product URL
scrape_amazon_product(url)

