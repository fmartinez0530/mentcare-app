import pytest, json
from unittest import mock
from app import *
from datetime import datetime

def test_getDetails():
# @mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
# def test_getDetails(mock_connection):
#     mock_cursor = mock.MagicMock()
#     mock_connection.cursor.return_value = mock_cursor
#     mock_cursor.rowcount = 0
#     mock_cursor.execute.return_value = 0
#     mock_cursor.fetchall.return_value = ((1, 1, 999.99, 1, datetime(2024, 12, 31), '1', '1', '1', '1', '1', '1', 1, '1'),)

    response = app.test_client().post('/getDetails', json={
        "patientId": 1,
    })
    assert response.status_code == 200
    print(response.data)
    assert 1 == json.loads(response.data.decode("utf-8"))[0][0]
    assert 1 == json.loads(response.data.decode("utf-8"))[0][1]
    assert 999.99 == json.loads(response.data.decode("utf-8"))[0][2]
    assert 1 == json.loads(response.data.decode("utf-8"))[0][3]
    assert "Tue, 31 Dec 2024 00:00:00 GMT" == json.loads(response.data.decode("utf-8"))[0][4]
    assert "1" == json.loads(response.data.decode("utf-8"))[0][5]
    assert "1" == json.loads(response.data.decode("utf-8"))[0][6]
    assert "1" == json.loads(response.data.decode("utf-8"))[0][7]
    assert "1" == json.loads(response.data.decode("utf-8"))[0][8]
    assert "1" == json.loads(response.data.decode("utf-8"))[0][9]
    assert "1" == json.loads(response.data.decode("utf-8"))[0][10]
    assert 1 == json.loads(response.data.decode("utf-8"))[0][11]
    assert "1" == json.loads(response.data.decode("utf-8"))[0][12]
    assert 1==2

def test_submitPayment():
    response = app.test_client().post('/submitPayment', json={
        "invoiceId": 2,
        "patientId": 1,
        "amount": 100,
        "cardNum": "1",
        "cvc": "1",
        "expDate": "2024-12-31",
        "firstName": "1",
        "lastName": "1",
        "city": "1",
        "billingAddress": "1",
        "state": "1",
        "country": "1",
        "zip": "1",
        "phone": "1",
        "check": False,
        "alreadyIn": False,
    })
    print(response.data)
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]
