import pytest, json
from unittest import mock
from app import *

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_therapistProfileInfo(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchone.side_effect = [('Name Name', 'Abt Me', 'Schooling', 'Available Time', 'Pricing Info', 'Relationship,Anxiety', None, 1, 20), [1,]]
    mock_cursor.fetchall.return_value = ((3,), (4,), (5,), (1,), (5,))

    response = app.test_client().post('/therapistProfileInfo', json={
        "urlUserId": 4,
    })
    assert response.status_code == 200
    print(response.data)
    assert "Name Name" == json.loads(response.data.decode("utf-8"))["Therapist"][0]
    assert "Abt Me" == json.loads(response.data.decode("utf-8"))["Therapist"][1]
    assert "Schooling" == json.loads(response.data.decode("utf-8"))["Therapist"][2]
    assert "Available Time" == json.loads(response.data.decode("utf-8"))["Therapist"][3]
    assert "Pricing Info" == json.loads(response.data.decode("utf-8"))["Therapist"][4]
    assert "Relationship,Anxiety" == json.loads(response.data.decode("utf-8"))["Therapist"][5]
    assert None == json.loads(response.data.decode("utf-8"))["Therapist"][6]
    assert 1 == json.loads(response.data.decode("utf-8"))["Therapist"][7]
    assert 20 == json.loads(response.data.decode("utf-8"))["Therapist"][8]
    assert 2 == json.loads(response.data.decode("utf-8"))["fives"]
    assert 1 == json.loads(response.data.decode("utf-8"))["fours"]
    assert 1 == json.loads(response.data.decode("utf-8"))["threes"]
    assert 0 == json.loads(response.data.decode("utf-8"))["twos"]
    assert 1 == json.loads(response.data.decode("utf-8"))["ones"]