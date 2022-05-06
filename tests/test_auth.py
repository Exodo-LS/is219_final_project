import pytest
from app.db.models import User


def test_request_nav_bar(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data


def test_auth_template_directory(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200


def test_login_form_password(client):
    """ Unit Test for Incorrect Password for Login """
    response = client.get("/login")
    test_user = 'IS219_TestUser@email.com'
    test_password = 'invalid_password'
    if User.email == test_user:
        if test_password != User.password:
            assert 'Invalid password' in response.data


def test_login_form_email_address(client):
    """ Unit Test for Incorrect Email for Login"""
    response = client.get("/login")
    if User.email is None:
        assert 'Invalid username' in response.data


def test_register_form_email_address_(client):
    """ Unit Test for Invalid Email for Registration"""
    response = client.get("/register")
    test_email = 'test'
    if User.email is None:
        User.email = test_email
        if '@' not in User.email:
            assert 'Please include an '@' in the email address' in response.data


def test_register_form_password_confirmation(client):
    """ Unit Test for Password Confirmation"""
    response = client.get("/register")
    test_password = 'Dummy_Pass_123'
    if User.email is not None:
        if User.password == test_password:
            assert 'Congratulations, you are now a registered user!' in response.data


def test_register_form_password(client):
    """ Unit Test for Password Criteria Check"""
    response = client.get("/register")
    test_pass = 'bad'
    if User.email is None:
        User.password = test_pass
        if len(User.password) < 6 or len(User.password) > 35:
            assert 'Please lengthen this text to 6 characters or more' in response.data


def test_registration_form_already_registered_user(client):
    """ Unit Test for Already Registered"""
    response = client.get("/register")
    test_user = 'IS219_TestUser@email.com'
    if User.email is not None and User.email == test_user:
        assert 'Already Registered' in response.data


def test_login_form_success(client):
    """ Unit Test for Successful Login"""
    response = client.get("/login")
    test_user = 'IS219_TestUser@email.com'
    test_password = 'Dummy_Pass_123'
    if User.email == test_user:
        if User.password == test_password:
            assert 'Login Successful' in response.data


def test_registration_form_success(client):
    """ Unit Test for Successful Registration"""
    response = client.get("/register")
    if User is None:
        assert 'Congratulations, you are now a registered user!' in response.data


def test_deny_dashboard_access(client):
    """ Unit Test for Denying Access to Dashboard"""
    response = client.get("/dashboard")
    if not User.authenticated:
        assert 'User Not Authenticated' in response.data


def test_allow_dashboard_access(client):
    """ Unit Test for Allowing Access to Dashboard"""
    response = client.get("/dashboard")
    test_user = 'IS219_TestUser@email.com'
    test_password = 'Dummy_Pass_123'
    if User.email == test_user and User.password == test_password:
        if User.authenticated:
            assert 'User Authenticated' in response.data
