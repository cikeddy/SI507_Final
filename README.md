# Exercise Generator by Cassie Eddy

[Link to this repository](https://github.com/cikeddy/SI507_Final)

---

## Project Description
My project aggregates information about exercises from ExRx.net (through web scraping) and allows users to search by exercise name to get information about an exercise. The project  also allows users to search for a muscle and recieve a list of associated exercises that target that muscle. There is a route for the homepage with a greeting and count of number of exercises. There are also routes for searching by exercise, by muscle, and for viewing a randomly selected exercise with corresponding information. Finally there are routes that show all exercises and muscles in the database.


## My Database Schema
![Exercise Generator Project Schema](images/database_diagram.jpg)

## How to run

1. Install all requirements with `pip install -r requirements.txt`
2. Check that `exercises.db` and `exrx_cache.json` are in the directory with the project
3. Run `python SI507project_tools.py` 
    - to prevent too many requests to exrx.net, I have inserted a sleep function into the scraping script (.5 seconds per exercise page that is requested). Because there are almost 1000 pages, the scraping process takes over 10 minutes. I have uploaded my populated cache  `exrx_cache.json` and database `exercises.db` files so users do not have to scrape unless they choose to
    - if you would like to scrape the data yourself, remove the `exrx_cache.json` and `exercises.db` files from the directory before running the `SI507project_tools.py` file
4. Navigate to the [home route](http://localhost:5000/home) to begin using the application

## How to use

1. When the application is running the following will be visible in the terminal ![picture of local server runnning](images/app_run.JPG)
2. When you are on the [home page](http://localhost:5000/home) you should see the following ![the homepage of the exercise generator project](images/homepage.JPG)

3. From the home page you can chose to search by exercise, by muscle, or randomly generate an exercise. You can also view a full list of exercises by clicking the "View all exercises" button or you can view a full list of muscles by clicking the "View all muscles" button.
    - VIEW ALL EXERCISES button will take you to a page that looks like this ![the view all exercises page](images/all_exercises.JPG)
    - VIEW ALL MUSCLES button will take you to a page that looks like this ![the view all muscles page](images/all_muscles.JPG)
4. You can start by searching `Cable Neck Flexion`, `Triceps Dip`, or another exercise you find on the full list of exercises
    - The search page for exercises will look like this ![the exercise search page](images/exercise_search.JPG)
    - The results page of an exercise will look like this ![an exercise search result page](images/exercise_result.JPG)
    - You can expand the accordion menu by clicking on panels to find out more information about an exercise ![expanding the accordion menu of the exercise search result page](images/accordion.JPG)
5. You can also start by searching for a muscle, such as `pectoralis major, clavicular`, on the muscle search page
    - The search page for muscles will look like this ![a muscles search page](images/muscle_search.JPG)
    - The result page for a muscle search will look like this ![a muscles search result page](images/muscle_result.JPG)
6. Alternatively, you can randomly pull data about an exercise and search for the target muscle for that exercse to find other related exercises


## Routes in this application
- `/home` -> this is the home page with a count of exercises
- `/all-exercises` -> this is page with a list of all exercises in the database
- `/all-muscles` -> this is the page with a list of all muscles in the database
- `/search` -> this route has a form for user input for either searching an exercise by name or randomly
- `/muscle-search` -> this route has a form for user input for either searching an exercises by target muscle  or randomly
- `/result` -> this route is where the form sends the result and displays information about an exercise when it is searched by name
- `/muscle` -> this route is where the form sends the result and displays a list of exercises related to a target muscle
- `/random` -> this route is where the form sends the result and displays information about a randomly selected exercise

## How to run tests
- make sure you have run the project before running the tests
1. Run `SI507project_tests.py`
2. If everything is running correctly, all tests will be passed and you will see the following in your terminal: ![a screenshot of tests passing](images/tests.JPG)

## In this repository:
- SI507project_data.py
- SI507project_tools.py
- SI507project_models.py
- SI507project_tests.py
- advanced_expiry_caching.py
- exercises.db
- database_diagram.jpg
- requirements.txt
- README.md
- /images
    - accordion.JPG
    - app_run.JPG
    - exercise_search.JPG
    - muscle_search.JPG
    - all_exercises.JPG
    - database_diagram.jpg
    - homepage.JPG
    - all_muscles.JPG
    - exercise_result.JPG
    - muscle_result.JPG
- /templates
    - accordion_script.js
    - index.html
    - muscle_search_result.html
    - all_exercises.html
    - invalid_search.html
    - search_form.html
    - all_muscles.html
    - muscle_search.html
    - search_result.html
-/static
    -/css
        - html5reset.css

---
## Code Requirements for Grading

### General
- [x] Project is submitted as a Github repository
- [x] Project includes a working Flask application that runs locally on a computer
- [x] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [x] Includes a diagram of your database schema
- [x] Includes EVERY file needed in order to run the project
- [x] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [x] Includes at least 3 different routes
- [x] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [x] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [ ] Use of a new module
- [ ] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [x] A many-to-many relationship in your database structure
- [x] At least one form in your Flask application
- [x] Templating in your Flask application
- [x] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [x] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [ ] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [x] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!
