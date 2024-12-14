import pytest, json
from unittest import mock
from app import *

# def test_patientOrTherapist():
@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_patientOrTherapist(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchone.side_effect = [(1, 'Patient'), (1,), (4, 'Therapist'), (1, 1)]

    response = app.test_client().post('/patientOrTherapist', json={
        "email": "john.smith@example.com",
        "password": "password123",
    })
    assert response.status_code == 200
    print(response.data)
    assert 0 == json.loads(response.data.decode("utf-8"))["isActive"]
    assert 1 == json.loads(response.data.decode("utf-8"))["realUserID"]
    assert 1 == json.loads(response.data.decode("utf-8"))["userID"]
    assert "Patient" == json.loads(response.data.decode("utf-8"))["userType"]

    response = app.test_client().post('/patientOrTherapist', json={
        "email": "linda.white@example.com",
        "password": "password123",
    })
    assert response.status_code == 200
    print(response.data)
    assert 1 == json.loads(response.data.decode("utf-8"))["isActive"]
    assert 4 == json.loads(response.data.decode("utf-8"))["realUserID"]
    assert 1 == json.loads(response.data.decode("utf-8"))["userID"]
    assert "Therapist" == json.loads(response.data.decode("utf-8"))["userType"]