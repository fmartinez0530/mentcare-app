import pytest, json
from unittest import mock
from app import *

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_sendTestimonial(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = 123

    response = app.test_client().post('/sendTestimonial', json={
        "userId": 1,
        "content": "Wow good website!",
    })

    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]

# def test_getTestimonials():
@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getTestimonials(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = (
        (1, 'Testimonial1', None, 'John Smith'),
        (2, 'Testimonial2', None, 'Jane Doe'),
        (3, 'Testimonial3', None, 'Linda White'),
    )

    response = app.test_client().get('/getTestimonials')
    print(response.data)
    print( json.loads(response.data.decode("utf-8")))
    assert response.status_code == 200
    assert "Testimonial1" == json.loads(response.data.decode("utf-8"))[0]["content"]
    assert 1 == json.loads(response.data.decode("utf-8"))[0]["id"]
    assert None == json.loads(response.data.decode("utf-8"))[0]["img"]
    assert "John Smith" == json.loads(response.data.decode("utf-8"))[0]["username"]