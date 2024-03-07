import unittest
from flask import Flask, url_for
from urllib.parse import urlparse
from flask_testing import TestCase
from app import app, db, Task

class TestTodoApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assertRedirects(self, response, location):
        # Extract the path from the absolute URL
        parsed_location = urlparse(response.location)
        self.assertEqual(parsed_location.path, location, 'URLs do not match')

    def test_index_page(self):
        response = self.client.get(url_for('index'))
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_add_task(self):
        response = self.client.post(url_for('add'), data={'content': 'Test Task'})
        self.assertRedirects(response, url_for('index'))

        task = Task.query.first()
        self.assertIsNotNone(task)
        self.assertEqual(task.content, 'Test Task')

    def test_delete_task(self):
        task = Task(content='Task to delete')
        db.session.add(task)
        db.session.commit()

        response = self.client.get(url_for('delete', id=task.id))
        self.assertRedirects(response, url_for('index'))

        deleted_task = Task.query.get(task.id)
        self.assertIsNone(deleted_task)

if __name__ == '__main__':
    unittest.main()

