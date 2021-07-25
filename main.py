import requests
from bs4 import BeautifulSoup as bs

def get_soup(url):
    response = requests.get(url)
    if response.ok:
        soup = bs(response.text, "html.parser")
    else:
        soup = ""
    return soup

def detailed_information():
    try:
        pass
    except:
        pass]

def main():
    url = "https://www.pixiv.net/en/tags/alice/artworks?s_mode=s_tag"
    get_soup(url)

if __name__ == "__main__":
    main()

