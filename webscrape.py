from distutils.command.clean import clean
import requests
from bs4 import BeautifulSoup

# check status code for reponse received

def collect_website_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

if __name__ == "__main__":

    #Get Content
    links = []
    base_url = "https://www.reviewed.com/best-right-now"
    substring = 'https://www.reviewed.com/'

    soupy = collect_website_data(base_url)

    for link in soupy.find_all('a'):
        clean_link= link.get('href')
        try:    
            if substring in clean_link:
                links.append(clean_link)
        except Exception:
            pass
    
    links = list(set(links))

    #Search List of URL and pull all p tag text
    
    for i in range(len(links)):
        page_data = collect_website_data(links[i])
        fname = f'c:\\temp\\output{i}.txt'
        with open(fname, 'w', encoding="utf-8") as f:
            for data in page_data.find_all('p'):
                f.write(data.get_text())
                f.close

    #to-do pull header tags
    #to-do search amazon api and generate affiliate links for products
    #to-do use markdown to format word doc just like webpage for blog posts
    #to-do pull images related to product








