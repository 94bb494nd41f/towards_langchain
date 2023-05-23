import time

import requests
from bs4 import BeautifulSoup
import wikipediaapi


def scrape_wiki_pages(domain):
    print("in_function")
    # Get the content of the main page
    response = requests.get(domain)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all the links to the wiki pages
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith(domain) and href.endswith('.html'):
            links.append(href)

    # Scrape the content of each wiki page
    wiki_text = ""
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        wiki_text += soup.get_text()

    return wiki_text


def scrape_wikipedia_article(url):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main content section of the page
    content_div = soup.find(id='mw-content-text')

    # Find all the text within the article's paragraphs
    paragraphs = content_div.find_all('p')

    # Concatenate all the paragraphs into a single string
    article_text = '\n'.join([p.get_text() for p in paragraphs])

    return article_text
def save_asHTML(response,url):
    html_split = url.split("/")
    html_path = "html/" + html_split[-2]
    f = open(html_path, "wb")
    f.write(response.content)
    f.close
    print("HTML saved")
    return

def scrape_johner_article(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    # save html
    save_asHTML(response, url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')


    # Find the main content section of the page
    #content_div = soup.find(id='mw-content-text')
    if soup.find(class_='entry-content') is not None:

        content_div = soup.find(class_='entry-content')
        # Find all the text within the article's paragraphs
        paragraphs = content_div.find_all('p')

        # Concatenate all the paragraphs into a single string
        article_text = '\n'.join([p.get_text() for p in paragraphs])
    else:
        article_text = ""
    return article_text

def get_blog_entrys():
    url = "https://www.johner-institut.de/blog/page/0"
    i = 0
    links = []
    neg_list = ["johner-institut.de/blog/page", "#comment", "#respond", "johner-institut.de/blog/author"]
    while i<50 and requests.get(url).status_code<400:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "johner-institut.de/blog" in href:
                if "johner-institut.de/blog/page" not in href  and "#comment" not in href and "#respond" not in href  and "johner-institut.de/blog/author" not in href :
                    if href not in links:
                        links.append(href)
        i+=1
        len_str=len(str(i))
        url = url[:-len_str]+str(i)
        print(i, url)
    return links


if __name__ == '__main__':
    #total_text=scrape_wiki_pages('https://wiki.computertruhe.de/')
    #url = 'https://wiki.computertruhe.de/Spezial:Alle_Seiten'

    #links = get_blog_entrys()

    url = "https://www.johner-institut.de/sitemap.xml?sitemap=pages&cHash=93156a4149e483476118183ba7e2acc0"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    ##creat url_list
    urls_raw = soup.get_text()
    urls_raw = urls_raw.split("\n")
    urls_raw = list(filter(None, urls_raw)) #remove empty elements from list
    urls = []
    for url in urls_raw:
        if url[0] == "h":
            urls.append(url)
    for link in soup.find_all('a'):
        print(link.get('href'))
####
    #verwendung von blog_based
    #urls = links
    #f = open("links.txt", "a", encoding="utf-8")
    #f.write("new \n")
    #f.write("\n".join(links))
    #f.close
    f = open("links.txt", "r")
    links = f.read().splitlines()
    print("Urls imported")
    urls = list(set(links))
####
    total_text = []
    total_url = []
    t1 = time.perf_counter()
    i = 0
    #urls=["https://www.johner-institut.de/blog/regulatory-affairs/mpbetreibv-medizinprodukte-betreiberverordnung/", "https://www.johner-institut.de/blog/category/regulatory-affairs/", "https://www.johner-institut.de/blog/regulatory-affairs/unterschiede-zwischen-der-ivdr-und-ivdd/" ]
    for link in urls:
        print("Nr:", i, "current URL:", link)
       # link = "https://www.johner-institut.de"
       # link= "https://www.johner-institut.de/blog/regulatory-affairs/mpbetreibv-medizinprodukte-betreiberverordnung/" for debugging
        inc_text = scrape_johner_article(link)
        total_text.append(inc_text)
        total_url.append((link, inc_text))
        i += 1
       # if i == 500:
         #   break
    print("finish, took:", time.perf_counter()-t1)

    total_text = list(filter(None, total_text))
    total_text = "\n \n".join(total_text)
    f = open("dumb_text.txt", "a", encoding="utf-8")
    f.write("new \n")
    f.write(total_text)
    f.close
    print("file saved")
    #total_text=scrape_wikipedia_article('https://wiki.computertruhe.de/')
    #print(total_text)