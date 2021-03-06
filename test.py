from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """check to make sure everything starts up correctly"""
        with self.client:
            response = self.client.get("/")
            self.assertIn('board', session)
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("numplays"))
            self.assertIn(b'Score:', response.data)
            self.assertIn(b"Your highest score is", response.data)
        
    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["N", "A", "R", "T", "T"], 
                                 ["C", "E", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')
        
    def test_not_on_board(self):
        """test if word is not on board"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["N", "A", "R", "T", "T"], 
                                 ["C", "E", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=board')
        self.assertEqual(response.json['result'], 'not-on-board')
        
    def test_not_word(self):
        """test if a non-english word is submitted"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["N", "A", "R", "T", "T"], 
                                 ["C", "E", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=qwwertty')
        self.assertEqual(response.json['result'], 'not-word')