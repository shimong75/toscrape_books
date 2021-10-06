import requests
import re
from bs4 import BeautifulSoup
import json


def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)
    
def get_all_pages_urls():
    pages_urls = []

    new_page = "http://books.toscrape.com/catalogue/page-1.html"
    while requests.get(new_page).status_code == 200:
        print(f"Appended url: {new_page}")
        pages_urls.append(new_page)
        new_page = pages_urls[-1].split("-")[0] + "-" + str(int(pages_urls[-1].split("-")[1].split(".")[0]) + 1) + ".html"
    return pages_urls

def parse_book_data(booksURLs: list):
    names = []
    # scrape data for every book URL: this may take some time
    for url in booksURLs:
        soup = getAndParseURL(url)
        # product name
        names.append(soup.find("div", class_ = re.compile("product_main")).h1.text)
        

def getBooksURLs(url):
    soup = getAndParseURL(url)
    # remove the index.html part of the base url before returning the results
    res = (["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])
    print (res)
    return res





if __name__ == "__main__":
    
    all_pages_urls = get_all_pages_urls()
    booksURLs = []
    for page in all_pages_urls:
        booksURLs.extend(getBooksURLs(page))
    books_names_with_link = {}

    for url in booksURLs:
        soup = getAndParseURL(url)
        # product name
        book_name = soup.find("div", class_ = re.compile("product_main")).h1.text
        books_names_with_link[book_name] = url
        print(f"name: {book_name}")
        print(f"url: {books_names_with_link[book_name]}")


    with open("books.json", "w") as outfile:
        json.dump(books_names_with_link, outfile)