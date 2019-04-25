from SI507project_tools import *
import unittest
from bs4 import BeautifulSoup 
from sqlalchemy import create_engine
from advanced_expiry_caching import Cache
from SI507project_data import soup, program_cache,obj
from SI507project_tools import get_exercise_links
from SI507project_models import Muscle


## check that random_ex returns two different exercises
class PartOne(unittest.TestCase):    
    def test_get_random_ex(self):
        self.exercises_1 = get_random_exercise()
        self.exercises_2 = get_random_exercise()
        self.assertNotEqual(self.exercises_1,self.exercises_2, "Testing that the get_random_exercises function returns two different  exercises")
        

##  check that get_exercise_links returns a list and that https://exrx.net/WeightExercises/ is the pre-fix to links
class PartTwo(unittest.TestCase):
    def test_exercise_links(self):
        self.links = get_exercise_links(obj)
        self.type = [0,1]
        self.assertEqual(type(self.links),type(self.type))
    
    def test_exercise_links(self):
        self.links = get_exercise_links(obj)
        self.base = 'https://exrx.net/WeightExercises/'
        self.assertIn(self.base, self.links[1], "Testing that the URL for the first link has correct base")
        self.assertIn(self.base, self.links[20], "Testing that the URL for the 20th link has correct base")
        
##  check that get_exercise returns exercise object type
class PartThree(unittest.TestCase):
    def test_get_exercise(self):
        self.exercise = get_or_create_exercise('hello', 'random','random','random','random','random')
        self.assertIsInstance(self.exercise, Exercise, "Testing that get_or_create_exercise returns an instance of class/model Exercise")
        
# check that the id of an exercise I create with get_or_create_exercise is an integer
    def test_get_exercise_2(self):
        self.exercise = get_or_create_exercise('hello','random','random','random','random','random')
        self.int = 2
        self.assertEqual(type(self.exercise.id),type(self.int))
        



## check that soup is a beautiful soup object with data in it
class PartFour(unittest.TestCase):
    def test_soup(self):
        self.soup = soup
        self.assertEqual(str(type(self.soup)),"<class 'bs4.BeautifulSoup'>")
        
    def test_soup2(self):
        self.soup = soup
        self.assertIsNotNone(self.soup.find('h1').text, "Testing that there is data in the Beautiful Soup object")
        

## check that the database has all expected tables and that data has been populated
class PartFive(unittest.TestCase):
    def test_database_tables(self):
        self.engine = create_engine('sqlite:///./exercises.db')
        self.table_names = self.engine.table_names()
        self.assertEqual(self.table_names,['exercise_groups', 'exercises', 'forces', 'mechanics', 'muscles', 'utilities'])
    
    def test_database_data(self):
        self.query = Muscle.query.filter_by(name='sternocleidomastoid').first()
        self.assertIsNotNone(self.query)
        


if __name__ == "__main__":
    unittest.main(verbosity=2)
