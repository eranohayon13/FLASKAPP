import unittest

from flask import abort, url_for
from flask_testing import TestCase

from application import app,db
from application.models import Users, Posts
class TestBase(TestCase):
    def create_app(self):
        #pass in configs for test database
        config_name='testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI="mysql+pymysql://eran:password@localhost/test")
        return app
    
    def setUp(self):
    #called before every test.
        db.session.commit()
        db.drop_all()
        db.create_all()

    #create test admin user
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password="admin2016")
    #create test non-admin user
        employee = Users(first_name="test", last_name="user", email="test@user.com", password="test2016")

    #saves users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
    #called after every test.
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_homepage_view(self):
    #testing home page is accesible without login
    #200 will return if the homepage is accessible without logging on
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code,200)

    def test_post_route(self):
        login = client.post(first_name="admin", last_name="admin", email="admin@admin.com", password="admin2016")
        assertRedirect('login', 'post')
