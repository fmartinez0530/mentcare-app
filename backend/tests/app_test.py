import pytest, json
from unittest import mock
from app import *

# Test backend is online
def test_defaultFunc():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b"Backend is alive" in response.data

# Mock the DB connection so pytest doesn't change anything in the DB
@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_endpointNumberOneFunc(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = 123

    response = app.test_client().post('/endpointOne', json={})
    assert response.status_code == 200
    assert b"someSQLdata" in response.data

# Mock the DB connection so pytest doesn't change anything in the DB
@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_navbarDataFunc(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.description = ((('userID'),), (('userName'),), (('userType'),), (('isActive'),))
    mock_cursor.fetchall.side_effect = [
        ((4, 'Linda White', 'Therapist', 1),), # User Data 1
        False, # Notifs
        ((1, 'John Smith', 'Patient'),), # User Data 2
        ((1, 'Therapist started a chat!', '/chat'), (2, 'Therapist has retired!', None), (3, 'Therapist sent you feedback!', '/dashboard'), (4, 'Testing Notification!', None)), # Notifs
        False, # User Data 3
    ]

    # post 1
    response = app.test_client().post('/navbarData', json={
        "fakeUserID": 1,
        "userType": "Therapist"
    })
    assert response.status_code == 200
    assert b'"userName":"Linda White"' in response.data
    assert b'"userType":"Therapist"' in response.data
    assert b'"userType":"Patient"' not in response.data
    assert b'"isActive":1' in response.data

    # post 2
    response = app.test_client().post('/navbarData', json={
        "fakeUserID": 1,
        "userType": "Patient"
    })
    assert response.status_code == 200
    assert b'"userName":"John Smith"' in response.data
    assert b'"userType":"Patient"' in response.data
    assert b'"userType":"Therapist"' not in response.data

    # post 3
    response = app.test_client().post('/navbarData', json={
        "fakeUserID": -1,
        "userType": "Patient"
    })
    assert response.status_code == 404
    assert b'User not found' in response.data

# @mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
# def test_settingsRemAccFunc(mock_connection):
#     mock_cursor = mock.MagicMock()
#     mock_connection.cursor.return_value = mock_cursor
#     mock_cursor.rowcount = 0
#     mock_cursor.execute.return_value = 0

#     response = app.test_client().post('/settingsRemoveAccount', json={
#         "userId": 1,
#         "userType": "Therapist"
#     })
#     assert response.status_code == 200

#     response = app.test_client().post('/settingsRemoveAccount', json={
#         "userId": 1,
#         "userType": "Patient"
#     })
#     assert response.status_code == 200
#     assert "successful" == json.loads(response.data.decode("utf-8"))["deletion"]