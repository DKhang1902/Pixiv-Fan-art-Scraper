#!/usr/bin/env python3
# TODO
#   1. 
#   2.
#   3.
#   4.
#   5.


import requests
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

def get_soup(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.ok:
        soup = bs(response.text, "html.parser")
    else:
        soup = ""
    return soup

def link_generator(query,page):
    page = str(page)
    query = query.split(" ")
    query = "%20".join(query)
    link = "https://pixiv.net/en/tags/"+query+"/artworks?p="+ page + "&s_mode=s_tag"
    return link

def get_links(page_link):
    soup = get_soup(page_link)
    print(soup)
    links = soup.find("ul",class_="l7cibp-1 iTgRcY").find_all("a",class_='rp5asc-16 kdmVAX sc-AxjAm MksUu')
    print(links)
    return links


def detailed_information(the_links):
    # Artist
    # Likes
    # Bookmarks
    # Views
    try:
        pass
    except:
        pass

def csv_writer():
    pass

def main():
    query = input("What is the keyword: ")
    page_number = 1
    while True:
        page_link = link_generator(query,page_number)
        print(page_link)
        the_links = get_links(page_link)
        page_number += 1
        break
    print(the_links)

if __name__ == "__main__":
    main()


