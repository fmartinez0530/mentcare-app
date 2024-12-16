import pytest, json
from unittest import mock
from app import *
from datetime import datetime

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getDetails(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = ((2, 1, '1234123412341234', 999.99, datetime(2024, 12, 31), 'John', 'Smith', 'City', 'Address123', 'State', 'USA', 12345, '1231231234'),)

    response = app.test_client().post('/getDetails', json={
        "patientId": 1,
    })
    assert response.status_code == 200
    assert 2 == json.loads(response.data.decode("utf-8"))[0][0]
    assert 1 == json.loads(response.data.decode("utf-8"))[0][1]
    assert "1234123412341234" == json.loads(response.data.decode("utf-8"))[0][2]
    assert 999.99 == json.loads(response.data.decode("utf-8"))[0][3]
    assert "Tue, 31 Dec 2024 00:00:00 GMT" == json.loads(response.data.decode("utf-8"))[0][4]
    assert "John" == json.loads(response.data.decode("utf-8"))[0][5]
    assert "Smith" == json.loads(response.data.decode("utf-8"))[0][6]
    assert "City" == json.loads(response.data.decode("utf-8"))[0][7]
    assert "Address123" == json.loads(response.data.decode("utf-8"))[0][8]
    assert "State" == json.loads(response.data.decode("utf-8"))[0][9]
    assert "USA" == json.loads(response.data.decode("utf-8"))[0][10]
    assert 12345 == json.loads(response.data.decode("utf-8"))[0][11]
    assert "1231231234" == json.loads(response.data.decode("utf-8"))[0][12]


# def test_submitPayment():
@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_submitPayment(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0

    response = app.test_client().post('/submitPayment', json={
        "invoiceId": 2,
        "patientId": 1,
        "amount": 100,
        "cardNum": "1111222233334444",
        "cvc": "001",
        "expDate": "2024-12-31",
        "firstName": "Firstname",
        "lastName": "Lastname",
        "city": "Cityname",
        "billingAddress": "123 Sesame Street",
        "state": "New Jersey",
        "country": "United States of America",
        "zip": "55555",
        "phone": "7775551234",
        "check": False,
        "alreadyIn": False,
    })
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]

    response = app.test_client().post('/submitPayment', json={
        "invoiceId": 2,
        "patientId": 1,
        "amount": 100,
        "cardNum": "1111222233334444",
        "cvc": "001",
        "expDate": "2024-12-31",
        "firstName": "Firstname",
        "lastName": "Lastname",
        "city": "Cityname",
        "billingAddress": "123 Sesame Street",
        "state": "New Jersey",
        "country": "United States of America",
        "zip": "55555",
        "phone": "7775551234",
        "check": True,
        "alreadyIn": False,
    })
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]

    response = app.test_client().post('/submitPayment', json={
        "invoiceId": 2,
        "patientId": 1,
        "amount": 100,
        "cardNum": "1111222233334444",
        "cvc": "001",
        "expDate": "2024-12-31",
        "firstName": "Firstname",
        "lastName": "Lastname",
        "city": "Cityname",
        "billingAddress": "123 Sesame Street",
        "state": "New Jersey",
        "country": "United States of America",
        "zip": "55555",
        "phone": "7775551234",
        "check": False,
        "alreadyIn": True,
    })
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]

    response = app.test_client().post('/submitPayment', json={
        "invoiceId": 2,
        "patientId": 1,
        "amount": 100,
        "cardNum": "1111222233334444",
        "cvc": "001",
        "expDate": "2024-12-31",
        "firstName": "Firstname",
        "lastName": "Lastname",
        "city": "Cityname",
        "billingAddress": "123 Sesame Street",
        "state": "New Jersey",
        "country": "United States of America",
        "zip": "55555",
        "phone": "7775551234",
        "check": True,
        "alreadyIn": True,
    })
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]