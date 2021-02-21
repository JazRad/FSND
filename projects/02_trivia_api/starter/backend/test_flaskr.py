import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('caryn', 'mypass', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.error_questions = {
            'question':'Testing my again',
            'answer':'ok',
            'difficulty':'james',
            'category':'sally'
        }

        self.new_question = {
            'question': 'How old was Einstein when he died?',
            'answer': '76',
            'difficulty': 3,
            'category': 1
        }

        self.new_search = {
            'searchTerm':'burton'
        }

        self.new_quiz = {
            "previous_questions": [17],
            "quiz_category": {"type":"Geography", "id":"2"}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertFalse(data['current_category'])
    
    
    def test_delete_question(self):
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 12).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)


    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def search_questions(self):
        res = self.client().post('/searchQuestions', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], None)


    def test_get_categories_question(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],5)

    def test_quiz_answers(self):
        res = self.client().post('/quizzes', json=self.new_quiz)
        data  = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['previousQuestions'])
        self.assertTrue(data['question'])         

    def test_404_if_quiz_question_not_exist(self):
        res = self.client().get('/sa?page=600')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'Not found')

    def test_400_method_not_allowed(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_422_unprocessable(self):
        res = self.client().post('/questions', json=self.error_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()