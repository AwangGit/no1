# Test code created by AskTheCode assistant

import unittest
from advanced_file_upload_webapp_20240528_1 import app
import os

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.uploads_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(self.uploads_folder):
            os.makedirs(self.uploads_folder)

    def tearDown(self):
        self.app_context.pop()
        # 清理上传的测试文件
        for filename in os.listdir(self.uploads_folder):
            file_path = os.path.join(self.uploads_folder, filename)
            os.unlink(file_path)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'登录', response.data)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'登录', response.data)

    def test_successful_login(self):
        response = self.app.post('/login', data=dict(
            username='admin',
            password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'登录成功', response.data)

    def test_failed_login(self):
        response = self.app.post('/login', data=dict(
            username='admin',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'用户名或密码错误', response.data)

    def test_upload_page_access(self):
        self.app.post('/login', data=dict(
            username='admin',
            password='password123'
        ), follow_redirects=True)
        response = self.app.get('/upload', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'文件上传', response.data)

    def test_file_upload(self):
        self.app.post('/login', data=dict(
            username='admin',
            password='password123'
        ), follow_redirects=True)
        with open('test_upload.txt', 'w') as f:
            f.write('This is a test file.')
        with open('test_upload.txt', 'rb') as f:
            response = self.app.post('/upload', data={'file': f}, follow_redirects=True)
        os.remove('test_upload.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'文件上传成功', response.data)

    def test_file_already_exists(self):
        self.app.post('/login', data=dict(
            username='admin',
            password='password123'
        ), follow_redirects=True)
        with open(os.path.join(self.uploads_folder, 'testfile.txt'), 'w') as f:
            f.write('This is a test file.')
        with open(os.path.join(self.uploads_folder, 'testfile.txt'), 'rb') as f:
            response = self.app.post('/upload', data={'file': f}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'文件已存在', response.data)

    def test_logout(self):
        self.app.post('/login', data=dict(
            username='admin',
            password='password123'
        ), follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'您已登出登录', response.data)

if __name__ == '__main__':
    unittest.main()

