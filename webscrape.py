from distutils.command.clean import clean
import requests
from bs4 import BeautifulSoup

# Collects data from base webpage
def collect_website_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

#Turns BeautifulSoup object as parameter, then returns list of urls
def get_urls(bs_object, substring):
    links = []
    a_elements = bs_object.find_all('a')
    for link in a_elements:
        clean_link= link.get('href')
        try:    
            if substring in clean_link:
                links.append(clean_link)
        except Exception:
            pass
    
    links = list(set(links))
    return links

#Main Script Logic
if __name__ == "__main__":
    base_url = "https://www.reviewed.com/best-right-now"
    substring = 'https://www.reviewed.com/'
    soupy = collect_website_data(base_url)
    product_links = get_urls(soupy, substring)

    #Loop through each URL and pull all p tag text for that page
    for i in range(len(product_links)):
        page_data = collect_website_data(product_links[i])
        fname = f'/Users/josh/Python/Data/output{i}.txt'
        with open(fname, 'w', encoding="utf-8") as f:
            for data in page_data.find_all('p'):
                f.write(data.get_text())
                f.close

    #to-do pull header tags
    #to-do search amazon api and generate affiliate links for products
    #to-do use markdown to format word doc just like webpage for blog posts
    #to-do pull images related to product








