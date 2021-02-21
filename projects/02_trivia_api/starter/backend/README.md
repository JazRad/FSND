# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 
```

## Introduction

- The trivia app is built as a RESTful API and follow those conventions

## Getting Started

- Authentication: This version of the application does not require authentication or API keys.

## Error Handling

- Errors are returned as JSON objects in the following format:
  {
  "success": False,
  "error": 404,
  "message:" "Resource Not Found"
  }

## Endpoints

### GET '/categories'
- Fetches a dictionary of categories 
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

### GET '/questions'

- General:
  - Returns categories and question objects, current category, success value, and total number of questions
  * Results are paginated in groups of 10. Include a request argument to choose a page number, starting from 1
- Sample: curl -X GET http://127.0.0.1:5000/questions
  "categories": {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  },
  "current_category": "Sports",
  "questions": [
  {
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4,
  "id": 2,
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
  {
  "answer": "Tom Cruise",
  "category": 5,
  "difficulty": 4,
  "id": 4,
  "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
  "answer": "Maya Angelou",
  "category": 4,
  "difficulty": 2,
  "id": 5,
  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer": "Edward Scissorhands",
  "category": 5,
  "difficulty": 3,
  "id": 6,
  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
  "answer": "Muhammad Ali",
  "category": 4,
  "difficulty": 1,
  "id": 9,
  "question": "What boxer's original name is Cassius Clay?"
  },
  {
  "answer": "Brazil",
  "category": 6,
  "difficulty": 3,
  "id": 10,
  "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  {
  "answer": "Uruguay",
  "category": 6,
  "difficulty": 4,
  "id": 11,
  "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
  "answer": "George Washington Carver",
  "category": 4,
  "difficulty": 2,
  "id": 12,
  "question": "Who invented Peanut Butter?"
  },
  {
  "answer": "Lake Victoria",
  "category": 3,
  "difficulty": 2,
  "id": 13,
  "question": "What is the largest lake in Africa?"
  },
  {
  "answer": "The Palace of Versailles",
  "category": 3,
  "difficulty": 3,
  "id": 14,
  "question": "In which royal palace would you find the Hall of Mirrors?"
  }
  ],
  "success": true,
  "total_questions": 19
  }

### DELETE '/questions/<int:question_id>'

- General:
  - Deletes a question based on question_id and returns id of deleted question, success message and value
- Sample: curl -X DELETE http://127.0.0.1:5000/questions/23
  "deleted": 24,
  "message": "Successfully deleted!",
  "questions": [
  {
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4,
  "id": 2,
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
  {
  "answer": "Tom Cruise",
  "category": 5,
  "difficulty": 4,
  "id": 4,
  "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
  "answer": "Maya Angelou",
  "category": 4,
  "difficulty": 2,
  "id": 5,
  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer": "Edward Scissorhands",
  "category": 5,
  "difficulty": 3,
  "id": 6,
  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
  "answer": "Muhammad Ali",
  "category": 4,
  "difficulty": 1,
  "id": 9,
  "question": "What boxer's original name is Cassius Clay?"
  },
  {
  "answer": "Brazil",
  "category": 6,
  "difficulty": 3,
  "id": 10,
  "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  {
  "answer": "Uruguay",
  "category": 6,
  "difficulty": 4,
  "id": 11,
  "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
  "answer": "George Washington Carver",
  "category": 4,
  "difficulty": 2,
  "id": 12,
  "question": "Who invented Peanut Butter?"
  },
  {
  "answer": "Lake Victoria",
  "category": 3,
  "difficulty": 2,
  "id": 13,
  "question": "What is the largest lake in Africa?"
  },
  {
  "answer": "The Palace of Versailles",
  "category": 3,
  "difficulty": 3,
  "id": 14,
  "question": "In which royal palace would you find the Hall of Mirrors?"
  }
  ],
  "success": true,
  "total_questions": 19
  }

### POST '/questions'

- General:
  - Creates a new question using the submitted.

* Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Which was green and blue?", "answer":"green", "difficulty":"2", "category": "4"}'
  "created": 25,
  "questions": [
  {
  "answer": "Rugby answer",
  "category": "Sports",
  "difficulty": 2,
  "id": 22,
  "question": "Rugby"
  },
  {
  "answer": "Answer to quiz 24",
  "category": "History",
  "difficulty": 2,
  "id": 24,
  "question": "History Question 24"
  },
  {
  "answer": "Answer to quiz 25",
  "category": "History",
  "difficulty": 2,
  "id": 25,
  "question": "History Question 25"
  }
  ],
  "success": true,
  "total_questions": 3
  } "created": 25,
  "message": "Successfully created",
  "questions": [
  {
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4,
  "id": 2,
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
  {
  "answer": "Tom Cruise",
  "category": 5,
  "difficulty": 4,
  "id": 4,
  "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
  "answer": "Maya Angelou",
  "category": 4,
  "difficulty": 2,
  "id": 5,
  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer": "Edward Scissorhands",
  "category": 5,
  "difficulty": 3,
  "id": 6,
  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
  "answer": "Muhammad Ali",
  "category": 4,
  "difficulty": 1,
  "id": 9,
  "question": "What boxer's original name is Cassius Clay?"
  },
  {
  "answer": "Brazil",
  "category": 6,
  "difficulty": 3,
  "id": 10,
  "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  {
  "answer": "Uruguay",
  "category": 6,
  "difficulty": 4,
  "id": 11,
  "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
  "answer": "George Washington Carver",
  "category": 4,
  "difficulty": 2,
  "id": 12,
  "question": "Who invented Peanut Butter?"
  },
  {
  "answer": "Lake Victoria",
  "category": 3,
  "difficulty": 2,
  "id": 13,
  "question": "What is the largest lake in Africa?"
  },
  {
  "answer": "The Palace of Versailles",
  "category": 3,
  "difficulty": 3,
  "id": 14,
  "question": "In which royal palace would you find the Hall of Mirrors?"
  }
  ],
  "success": true,
  "total_questions": 20
  }

### POST '/questions/search'

- General:
  - Search for questions based on a search term and returns question objects.

* Sample: curl http://localhost:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"query" : { "category": "History" }}'
  "questions": [
  {
  "answer": "Maya Angelou",
  "category": 4,
  "difficulty": 2,
  "id": 5,
  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer": "Muhammad Ali",
  "category": 4,
  "difficulty": 1,
  "id": 9,
  "question": "What boxer's original name is Cassius Clay?"
  },
  {
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4,
  "id": 2,
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
  {
  "answer": "Tom Cruise",
  "category": 5,
  "difficulty": 4,
  "id": 4,
  "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
  "answer": "Edward Scissorhands",
  "category": 5,
  "difficulty": 3,
  "id": 6,
  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
  "answer": "Brazil",
  "category": 6,
  "difficulty": 3,
  "id": 10,
  "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  {
  "answer": "Uruguay",
  "category": 6,
  "difficulty": 4,
  "id": 11,
  "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
  "answer": "George Washington Carver",
  "category": 4,
  "difficulty": 2,
  "id": 12,
  "question": "Who invented Peanut Butter?"
  },
  {
  "answer": "Lake Victoria",
  "category": 3,
  "difficulty": 2,
  "id": 13,
  "question": "What is the largest lake in Africa?"
  },
  {
  "answer": "The Palace of Versailles",
  "category": 3,
  "difficulty": 3,
  "id": 14,
  "question": "In which royal palace would you find the Hall of Mirrors?"
  }
  ],
  "success": true,
  "total_questions": 10
  }

### GET '/questions/<int:category_id>'

- General:
  - Return questions based on category

* Sample: curl -X GET http://127.0.0.1:5000/questions/4 -H "Content-Type: application/json" -d '{"query" : { "category": "4" }}'
  "current_category": 4,
  "questions": [
  {
  "answer": "Maya Angelou",
  "category": 4,
  "difficulty": 2,
  "id": 5,
  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer": "Muhammad Ali",
  "category": 4,
  "difficulty": 1,
  "id": 9,
  "question": "What boxer's original name is Cassius Clay?"
  },
  {
  "answer": "George Washington Carver",
  "category": 4,
  "difficulty": 2,
  "id": 12,
  "question": "Who invented Peanut Butter?"
  },
  {
  "answer": "Scarab",
  "category": 4,
  "difficulty": 4,
  "id": 23,
  "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  {
  "answer": "2020",
  "category": 4,
  "difficulty": 1,
  "id": 24,
  "question": "Which year was the worst?"
  }
  ],
  "success": true,
  "total_questions": 5
  }

### POST '/quizzes'

- General:
  - Take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

* Sample: curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": {"type": "History", "id": 4}, "previous_questions":[2]}'
  "question": {
  "answer": "Scarab",
  "category": 4,
  "difficulty": 4,
  "id": 23,
  "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  }
  }

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```