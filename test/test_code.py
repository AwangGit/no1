# Test code created by AskTheCode assistant

import unittest
from advanced_file_upload_webapp_20240528_1 import app

class BasicTests(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_upload_page(self):
        with self.app.session_transaction() as sess:
            sess['username'] = 'admin'
        response = self.app.get('/upload', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_file_upload(self):
        with self.app.session_transaction() as sess:
            sess['username'] = 'admin'
        with open('uploads/testfile.txt', 'w') as f:
            f.write('This is a test file.')
        with open('uploads/testfile.txt', 'rb') as f:
            response = self.app.post('/upload', data={'file': f}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'文件上传成功', response.data)

if __name__ == '__main__':
    unittest.main()
