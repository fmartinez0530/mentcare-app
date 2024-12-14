import pytest, json
from unittest import mock
from app import *

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getCharging(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = ((20,),)

    response = app.test_client().post('/getCharging', json={
        "therapistId": 1,
    })
    assert response.status_code == 200
    assert 20 == json.loads(response.data.decode("utf-8"))[0][0]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_userChats(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = ((1, 'John Smith', '{"chats": [{"msg": "Message1", "sender": "P"}, {"msg": "Message2", "sender": "T"}]}', 'Inactive', 'Inactive'),)
    mock_cursor.description = (('patientID',), ('patientName',), ('content',), ('chatStatus',), ('requestStatus',))
    
    # post 1
    response = app.test_client().post('/userChats', json={
        "chooseId": 1,
        "userType": "Therapist",
    })
    assert response.status_code == 200
    assert 'Inactive' == json.loads(response.data.decode("utf-8"))[0]["chatStatus"]
    assert  json.loads(response.data.decode("utf-8"))[0]['content']
    assert 'Inactive' == json.loads(response.data.decode("utf-8"))[0]["requestStatus"]
    assert 1 == json.loads(response.data.decode("utf-8"))[0]["patientID"]
    assert "John Smith" == json.loads(response.data.decode("utf-8"))[0]["patientName"]

    mock_cursor.fetchall.return_value = ((1, 'Linda White', '{"chats": [{"msg": "Message1", "sender": "P"}, {"msg": "Message2", "sender": "T"}]}', 'Active', 'Inactive', 'Inactive'),)
    mock_cursor.description = (('therapistID',), ('therapistName',), ('content',), ('status',), ('chatStatus',), ('requestStatus',))
    
    # post 2
    response = app.test_client().post('/userChats', json={
        "chooseId": 1,
        "userType": "Patient",
    })
    assert response.status_code == 200
    assert 'Inactive' == json.loads(response.data.decode("utf-8"))[0]["chatStatus"]
    assert  json.loads(response.data.decode("utf-8"))[0]['content']
    assert 'Inactive' == json.loads(response.data.decode("utf-8"))[0]["requestStatus"]
    assert 'Active' == json.loads(response.data.decode("utf-8"))[0]["status"]
    assert 1 == json.loads(response.data.decode("utf-8"))[0]["therapistID"]
    assert "Linda White" == json.loads(response.data.decode("utf-8"))[0]["therapistName"]
    
    # post 3
    response = app.test_client().post('/userChats', json={
        "chooseId": 1,
        "userType": "BadValue",
    })
    print("response data", response.data)
    assert response.status_code == 500
    assert "Invalid user type" == json.loads(response.data.decode("utf-8"))["error"]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_startChat(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchone.side_effect = [(1,), None]

    response = app.test_client().post('/startChat', json={
        "patientId": 1,
        "therapistId": 1,
    })
    assert response.status_code == 200
    print(response.data)
    assert "Chat started successfully!" == json.loads(response.data.decode("utf-8"))["message"]

    response = app.test_client().post('/startChat', json={
        "patientId": -1,
        "therapistId": -1,
    })
    assert response.status_code == 500
    print(response.data)
    assert "\'NoneType\' object is not subscriptable" == json.loads(response.data.decode("utf-8"))["error"]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_endChat(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchone.side_effect = [(1,), None]

    response = app.test_client().post('/endChat', json={
        "patientId": 1,
    })
    assert response.status_code == 200
    print(response.data)
    assert "Chat ended successfully!" == json.loads(response.data.decode("utf-8"))["message"]

    response = app.test_client().post('/endChat', json={
        "patientId": -1,
        "therapistId": -1,
    })
    assert response.status_code == 500
    print(response.data)
    assert "\'NoneType\' object is not subscriptable" == json.loads(response.data.decode("utf-8"))["error"]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_requestChat(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchone.side_effect = [(1,), None]

    response = app.test_client().post('/requestChat', json={
        "patientId": 1,
        "therapistId": 1,
    })
    assert response.status_code == 200
    print(response.data)
    assert "Requested" == json.loads(response.data.decode("utf-8"))["message"]

    response = app.test_client().post('/requestChat', json={
        "patientId": -1,
        "therapistId": -1,
    })
    assert response.status_code == 500
    print(response.data)
    assert "\'NoneType\' object is not subscriptable" == json.loads(response.data.decode("utf-8"))["error"]

# def test_sendMessage():
@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_sendMessage(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchone.side_effect = [
      ('{"chats": [{"msg": "Message1", "sender": "P"}, {"msg": "Message2", "sender": "T"}]}',),
      (2,),
      ('{"chats": [{"msg": "Message1", "sender": "P"}, {"msg": "Message2", "sender": "T"}]}',),
      (2,),
      ["this is not json"]
    ]

    response = app.test_client().post('/sendMessage', json={
        "patientId": 1,
        "therapistId": 1,
        "message": "Helllo",
        "sender": "P",
    })
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]

    response = app.test_client().post('/sendMessage', json={
        "patientId": 1,
        "therapistId": 1,
        "message": "Helllo",
        "sender": "P",
    })
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]

    response = app.test_client().post('/sendMessage', json={
        "patientId": 1,
        "therapistId": 1,
        "message": "XFAIL",
        "sender": "P",
    })
    assert response.status_code == 500
    assert "Err: Expecting value: line 1 column 1 (char 0)" == json.loads(response.data.decode("utf-8"))["error"]