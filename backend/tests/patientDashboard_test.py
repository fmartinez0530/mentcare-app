import pytest, json
from unittest import mock
from app import *

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_patientDashboardData(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.side_effect = 123
    response = app.test_client().post('/patientDashboardData', json={
        "patientId": 1,
    })

    assert response.status_code == 200
    assert {'journalEntry': 'Feeling down today', 'journalID': 1, 'timeDone': 'Sun, 01 Oct 2023 00:00:00 GMT'} == json.loads(response.data.decode("utf-8"))[0][0]
    assert {'feedback': 'Keep on exercising!', 'feedbackDate': 'Mon, 02 Oct 2023 00:00:00 GMT', 'feedbackID': 1, 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[1][0]
    assert {'calories': 500, 'dailySurveyID': 1, 'dateCreated': 'Sun, 10 Nov 2024 00:00:00 GMT', 'energy': 5, 'exercise': 2, 'height': 70.0, 'sleep': 8, 'stress': 9, 'water': 1, 'weight': 150} == json.loads(response.data.decode("utf-8"))[2][0]
    assert {'dateCreated': 'Sun, 17 Nov 2024 00:00:00 GMT', 'survey': '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 'surveyID': 1, 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[3][0]
    assert {'answers': '[{"q1": "Great!"}, {"q2": 150}, {"q3": true}, {"q4": 9}]', 'completionID': 1, 'dateDone': 'Fri, 06 Oct 2023 00:00:00 GMT', 'questions': '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[4][0]
    assert {'amountDue': 10.0, 'dateCreated': 'Sun, 10 Nov 2024 00:00:00 GMT', 'invoiceID': 3, 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[5][0]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_saveJournal(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = 123
    response = app.test_client().post('/saveJournal', json={
        "journalEntry": "Feeling down today",
        "patientId":2,
        "journalId":1
    })
    assert response.status_code == 200
    assert "Journal saved successfully" == json.loads(response.data.decode("utf-8"))["message"]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_sendFeedback(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = 123
    response = app.test_client().post('/sendFeedback', json={
        "therapistID":1,
        "patientID":1,
        "feedback":"Go to the gym"
    })
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_completeDailySurvey(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.fetchall.return_value = 123
    response = app.test_client().post('/completeDailySurvey', json={
        "patientID": 1, 
        "userID": 1,
        "dailySurveyID": 5, 
        "weight": 150, 
        "height": 6, 
        "calories": 1000, 
        "water": 2, 
        "exercise": 1, 
        "sleep": 8, 
        "energy": 5, 
        "stress": 5
    })
    assert response.status_code == 200
    assert "Survey data submitted successfully!" == json.loads(response.data.decode("utf-8"))["message"]