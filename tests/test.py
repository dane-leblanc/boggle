from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUP(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        
    def test_show_homepage(self):
        response = self.client.get('/')
        self.assertIn('board', session)
        self.assertIsNone(session.get("highscore"))
        self.assertIsNone(session.get("numplays"))
        