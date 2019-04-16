from bs4 import BeautifulSoup 
import requests, json 
import csv
from advanced_expiry_caching import Cache #importing from the cache code from Jackie
import pandas as pd
import numpy as np

FILENAME = "exrx_cache.json"

program_cache = Cache(FILENAME) 


#exploring one exercise page
base_url = "https://exrx.net/WeightExercises/Sternocleidomastoid/CBNeckFlx"

data = program_cache.get(base_url)
if not data:
    data = requests.get(base_url).text

    program_cache.set(base_url, data, expire_in_days=10) # this data isn't going to change very much

soup = BeautifulSoup(data, "html.parser")

obj =  soup.find_all("div", class_="col-sm-6")[1]

print(obj.find_all("ul")[0])

synergists = []

for x in obj.find_all("ul")[1].text:
    synergists.append(x)

print(synergists)
    
    

#class Exercise():
#    def __init__(self, page):
#        self.utility = page.find_all("td")[1].text
#        self.mechanics = page.find_all("td")[3].text
#        self.force = page.find_all("td")[5].text
#        self.instructions = page.find_all("p")[2].text +page.find_all("p")[4].text
#        self.target_muscle = page.find_all("div", class_="col-sm-6")[1].find_all("ul")[0]
#        
#new_ex = Exercise(soup)
#
#print(new_ex.instructions)


        