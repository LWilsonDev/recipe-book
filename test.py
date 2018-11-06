from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    
    #ensure index page found and flask set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    # ensure correct page loads by checking for page title
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue('Vanlife Recipes' in response.data)
        
    # ensure login works with correct credentials 
    def test_correct_login_message(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                    data=dict(username="test_username", password="test_password"),
                    follow_redirects=True)
        self.assertIn('Welcome back', response.data)
        
    # ensure login shows error message with incorrect credentials 
    def test_incorrect_login_message(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                    data=dict(username="wrong_username", password="wrong_password"),
                    follow_redirects=True)
        self.assertIn('Invalid username/password', response.data)    
        
    
    # ensure login error message with incorrect credentials     
        
if __name__ == '__main__':
    unittest.main()