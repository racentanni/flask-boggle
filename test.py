from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle




class FlaskTests(TestCase):
     
     

    # TODO -- write tests for every view function / feature!
     def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
         
    def test_home_page(self):
        """
        Test whether the home page appears
        """
        with self.client:
            resp = self.client.get('/')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form id="start_form"', html)
            self.assertIn('action="/start"', html)
            self.assertIn('method="post">', html)
            self.assertIn('<input type="submit"', html)
      
    def test_session_info(self):
        """
        Test that the board is saved to the session
        """
        with self.client:
            # make a request to the route
            self.client.post("/start")
            
            # Test if the board is in the session
            with self.client.session_transaction() as session:
                self.assertIn('board', session)

    def test_start_page(self):
        """
        Test that board and text input for guess appears
        """
        with self.client:
            resp = self.client.post('/start')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form id="user_guess_form"', html)
            self.assertIn('action="/validate_guess"', html)
            self.assertIn('id="board"', html)
            self.assertIn('<input type="text"', html)
            self.assertIn('id="feedback_area"', html)
            
            
    def test_guess_validation(self):
        """
        Test guess is validated and for a response
        """
        with self.client:
            with self.client.session_transaction() as session:
                session['board'] = [['L', 'S', 'L', 'N', 'V'], ['J', 'B', 'Y', 'D', 'F'], ['Z', 'S', 'Z', 'I', 'S'], ['R', 'F', 'J', 'V', 'X'], ['U', 'G', 'E', 'T', 'U']]
        resp = self.client.post('/validate_guess', json={'guess':'get'})
        self.assertEqual(resp.json['result'], 'ok')
        
        resp_2 = self.client.post('/validate_guess', json={'guess':'error'})
        self.assertEqual(resp_2.json['result'], 'not-on-board')
        
        resp_3 = self.client.post('/validate_guess', json={'guess':'asdfgh'})
        self.assertEqual(resp_3.json['result'], 'not-word')
        
    def test_update_game_stats(self):
        """
        Test that stats are being updated and sent back to display to user.
        """
        with self.client.session_transaction() as session:
            session['board'] = [['L', 'S', 'L', 'N', 'V'], ['J', 'B', 'Y', 'D', 'F'], ['Z', 'S', 'Z', 'I', 'S'], ['R', 'F', 'J', 'V', 'X'], ['U', 'G', 'E', 'T', 'U']]

        resp = self.client.post('/game_over', json={"gameScore": 3})

        with self.client.session_transaction() as updated_session:
            # Getting the values from the updated session
            games_played = updated_session['games']
            high_score = updated_session['high_score']

            # Asserting that the session contains 'high_score' and 'games'
            self.assertIn('games', updated_session)
            self.assertIn('high_score', updated_session)

            # Comparing the response JSON data with the expected dictionary
            self.assertEqual(resp.json, {"games": games_played, "high_score": high_score})

                    
                         



