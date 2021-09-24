from bs4 import BeautifulSoup
from bs4.element import Comment

import requests
import json



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_web(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts) 
    string = " ".join(t.strip() for t in visible_texts)
    wordlist = string.lower().split()
    return wordlist

def find_list_resources (tag, attribute,soup):
   list = []
   for x in soup.findAll(tag):
       try:
           list.append(x[attribute])
       except KeyError:
           pass
   return(list)

def find_all_list_resources(soup):
    elements = ["img", "script", "link", "video", "audio", "iframe", "embed", "object", "source"]
    attributes = ["src", "src", "href", "src", "src", "src", "src", "data", "src" ]
    resources_dict = {}
    for i in range(len(elements)):
      resources_dict[elements[i]] = find_list_resources(elements[i], attributes[i], soup)

    with open('data.json', 'w') as outfile:
      json.dump(resources_dict, outfile)

    return resources_dict


def create_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def find_privacy_policy(soup, currentURL):
    link = soup.find('a', string = 'Privacy Policy')
    newURL = currentURL + link['href']
    return newURL

def word_freq_count(wordlist):
  wordOccur = {}
  for i in wordlist:
    if i in wordOccur:
      wordOccur[i] += 1
    else:
      wordOccur[i] = 1

  with open('word_freqs.json', 'w') as outfile:
      json.dump(wordOccur, outfile)

  return wordOccur


def main():
  url = 'https://www.cfcunderwriting.com/en-gb/'
  soup = create_soup(url)
  newURL = find_privacy_policy(soup, url)
  newSoup = create_soup(newURL)
  wordlist = text_from_web(newSoup)

if __name__=="__main__":
  main()