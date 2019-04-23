from bs4 import BeautifulSoup 
import requests
from advanced_expiry_caching import Cache #importing from the cache code from Jackie
import time
import csv


#
class ExerciseObj():
    def __init__(self, page):
        self.name = page.find("h1").text
        
        try:
            self.utility = page.find_all('td')[1].text.strip()
        except:
            self.utility = "N/A"
        try:
            self.mechanics = page.find_all("td")[3].text.strip()
        except IndexError:
            self.mechanics = "N/A"
        try:
            self.force = page.find_all("td")[5].text.strip()
        except IndexError:
            self.force = "N/A"
        try:
            self.instructions = page.find_all("p")[2].text +page.find_all("p")[4].text.strip()
        except IndexError:
            self.instructions = "N/A"
        try: 
            self.target_muscle = page.find_all("div", class_="col-sm-6")[1].find_all("ul")[0].text.strip()
        except IndexError:
            self.target_muscle = "N/A"
        
#        try:
#            for child in page.find_all('td')[1].find_all('a'):
#                self.utility.append(child.text.strip())
#        except IndexError:
#            self.utility.append("N/A")
    
    def csv_row(self):
        return [self.name,self.utility,self.mechanics,self.force,self.instructions,self.target_muscle]

FILENAME = "exrx_cache.json"

program_cache = Cache(FILENAME) 


#exploring one exercise page
#base_url = "https://exrx.net/WeightExercises/Sternocleidomastoid/CBNeckFlx"
#
#data = program_cache.get(base_url)
#if not data:
#    data = requests.get(base_url).text
#
#    program_cache.set(base_url, data, expire_in_days=10) # this data isn't going to change very much
#
#soup = BeautifulSoup(data, "html.parser")
#
#obj =  soup.find_all("div", class_="col-sm-6")[1]





top_directory_url = "https://exrx.net/Lists/Directory"

data = program_cache.get(top_directory_url)
if not data:
    data = requests.get(top_directory_url).text

    program_cache.set(top_directory_url, data, expire_in_days=10) # this data isn't going to change very much

soup = BeautifulSoup(data, "html.parser")

obj =  soup.select("div > ul > li > a", class_="col-sm-6")

#
#for x in obj:
#    print(x['href'])
    


def create_level2_url(url):
    level2_directory_url = "https://exrx.net/Lists/"
    return level2_directory_url + str(url)

level2_urls = []

for x in obj:
    if "https" not in x['href']: 
        level2_urls.append(create_level2_url(x['href']))


exercise_directory_url = "https://exrx.net/"
exercise_urls = []


for url in level2_urls:
    test_data = program_cache.get(url)
    if not test_data:
        test_data = requests.get(url).text
        program_cache.set(url,test_data,expire_in_days=10)
    test_soup = BeautifulSoup(test_data,"html.parser")
    links = test_soup.select("div > ul > li > ul> li > a", class_="col-sm-6")
    second_links = test_soup.select("div > ul > li > ul> li > ul > li > a", class_="col-sm-6")
    
    
#    count = 0
    for link in links:
#        count +=1
        ### only want weight exercises
        if "../../WeightExercises" in link['href']:
            new_link = exercise_directory_url + str(link['href'])[6:]
#            print(new_link, count)
        ###sometimes the links include the full link
        elif "https://exrx.net/WeightExercises" in link['href']:
            new_link = link['href']
#            print(new_link, count)
        exercise_urls.append(new_link)
            
    for link in second_links:
#        count +=1
        if "../../WeightExercises" in link['href']:
            new_link = exercise_directory_url + str(link['href'])[6:]
#            print(new_link, count)
        elif "https://exrx.net/WeightExercises" in link['href']:
            new_link = link['href']
#            print(new_link, count)
        exercise_urls.append(new_link)
            
### removing any duplicate links
final_exercise_urls = []

for x in exercise_urls:
    if x not in final_exercise_urls:
        final_exercise_urls.append(x)
        
        

exercises_list = []

for url in final_exercise_urls:
    data = program_cache.get(url)
    if not data:
        data = requests.get(url).text

        program_cache.set(url, data, expire_in_days=10) # this data isn't going to change very much
        time.sleep(.5)

    soup = BeautifulSoup(data, "html.parser")

    new_ex = ExerciseObj(soup)
    exercises_list.append(new_ex)


with open("exercise_data.csv","w", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["Exercise","Utility","Mechanics","Force","Instructions","Muscle"])
    for ex in exercises_list:
        writer.writerow(ex.csv_row())





#### this variable (ex_pages) will be a list of all the links to exercise pages
## will write a function that pulls links from the directory and concatinates with base url to produce full URL and returns the list ex_pages
### for the first level of the directory, I will only need to links from the top level of 
## write something in that crawls through and only pulls data with the base URL for weight exercises
### potentially expand to include streches and piar them with a exercise?

#def get_exercise_links(start_page):
#    ex_pages = []
#    return ex_pages
#
#

                    
