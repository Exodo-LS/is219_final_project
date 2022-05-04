import pytest
from app.db.models import User


def test_nav_bar_authentication_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data


def test_templates_in_auth_directory(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200


def test_login_form(client):
    """ Unit Test for Incorrect Password for Login """
    response = client.post("/login")
    test_user = 'IS219_TestUser@email.com'
    test_password = 'invalid_password'
    if User.email == test_user:
        if test_password != User.password:
            assert 'Invalid password' in response.data
        else:
            assert 'Login Successful' in response.data
    elif User.email is None:
        assert 'Invalid username' in response.data


def test_registration_form_email(client):
    """ Unit Test for Invalid Email for Registration"""
    response = client.post("/register")
    test_email = 'test'
    if User.email is None:
        User.email = test_email
        if '@' not in User.email:
            assert 'Please include an ' @ ' in the email address' in response.data
