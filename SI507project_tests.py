from SI507project_tools import *
import unittest
from bs4 import BeautifulSoup 


## check that random_ex returns something from a know muscle and that it returns two different exercises in one query 
class PartOne(unittest.TestCase):
    def test_get_random_ex(self):
        self.exercises = get_random_exercises('Sternocleiodomastoid')
        self.assertIsNotNone(self.exercises, "Testing that the get_random_exercise function returns something")
    
    def test_get_random_ex_2(self):
        self.exercises = get_random_exercises('Sternocleidomastoid')
        self.assertNotEqual(self.exercises[0],self.exercises[1], "Testing that the get_random_exercises function returns unique exercises")
        

##  check that https://exrx.net/WeightExercises/ is the pre-fix to the exercise links
class PartTwo(unittest.TestCase):
    def test_exercise_links(self):
        self.links = get_exercise_links('https://exrx.net/Lists/Directory')
        self.base = 'https://exrx.net/WeightExercises/'
        self.assertIn(self.base, self.links[1], "Testing that the URL for the first link has correct base")
        self.assertIn(self.base, self.links[20], "Testing that the URL for the 20th link has correct base")
        
##  check that get_exercise returns exercise object type
class PartThree(unittest.TestCase):
    def test_get_exercise(self):
        self.exercise = get_or_create_exercise('hello', 'random')
        self.assertIsInstance(self.exercise, Exercise, "Testing that get_or_create_exercise returns an instance of class/model Exercise")
        
# check that the id of an exercise I create with get_or_create_exercise is an integer
    def test_get_exercise_2(self):
        self.exercise = get_or_create_exercise('hello','random')
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
        

## check that the database has all expected tables
#class PartFive(unittest.TestCase):
#    def test_database_tables(self):
#        self.muscles_table = 
#        self.assertIsNoteNone(self.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
