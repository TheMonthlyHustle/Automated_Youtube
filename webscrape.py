from nturl2path import url2pathname
from unicodedata import category
import requests
import pypandoc
import progressbar
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

def get_titles(url_list):
    #Gets all of the titles from the pages
    titles = []

    for url in url_list:
        review_page = collect_website_data(url)
        title = review_page.h1.text
        titles.append(title)

    return(titles)

def markdown_formatting(records_list):
    #Creates markdown farmatted string from data
    markdown_string = ""

    for item in records_list:
        line = "#" + " " + item + "\n\n"
        markdown_string += line

    return markdown_string

def get_page_data(url_list):
    #Takes the list of urls and returns markdown formatted string

    markdown_string = ""

    print('Gathering product review data for each page:')
    with progressbar.ProgressBar(max_value=len(url_list)) as bar:
        for counter, url in enumerate(url_list):
            review_page = collect_website_data(url)
            title = review_page.h1.text
            title_md = "#" + " " + title + "\n\n"
            markdown_string += title_md
            for data in url_list:
                data_page = collect_website_data(data)
                product_title = data_page.h2.text
                review_md = "##" + " " + product_title + "\n"
                markdown_string += review_md
                try:
                    review_data = data_page.find_all('p').get_text()
                    review_md = review_data + "\n\n"
                    markdown_string += review_md
                except AttributeError:
                    markdown_string += '\n\n'
        markdown_string += '\\newpage'
        bar.update(counter)
    return markdown_string

def convert_to_word(markdown_string):
    #Converts markdown to a word document
    filters = ['pandoc-docx-pagebreakpy']
    output = pypandoc.convert_text(markdown_string, 'docx', format='md', outputfile="output.docx", filters=filters)
    pass

#Main Script Logic
if __name__ == "__main__":
    base_url = "https://www.reviewed.com/best-right-now"
    substring = 'https://www.reviewed.com/'
    soupy = collect_website_data(base_url)
    product_links = get_urls(soupy, substring)
    #titles = get_titles(product_links)
    #markdown = markdown_formatting(titles)
    review_data = get_page_data(product_links)
    convert_to_word(review_data)


    #Loop through each URL and pull all p tag text for that page
    """for i in range(len(product_links)):
        page_data = collect_website_data(product_links[i])
        fname = f'/Users/josh/Python/Data/output{i}.txt'
        with open(fname, 'w', encoding="utf-8") as f:
            for data in page_data.find_all('p'):
                f.write(data.get_text())
                f.close

    #to-do pull header tags - done
    #to-do search amazon api and generate affiliate links for products
    #to-do use markdown to format word doc just like webpage for blog posts
    #to-do pull images related to product"""








