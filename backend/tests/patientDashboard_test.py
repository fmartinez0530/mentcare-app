import pytest, json
from unittest import mock
from datetime import datetime
from app import *

# @mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
# def test_patientDashboardData(mock_connection):
    # mock_cursor = mock.MagicMock()
    # mock_connection.cursor.return_value = mock_cursor
    
    # mock_cursor.execute.return_value = None
    # mock_cursor.description = [
    #     ('journalID', 'journalEntry', 'timeDone',),
    #     ('feedbackID', 'feedback', 'feedbackDate', 'userName',),
    #     ('calories', 'dailySurveyID', 'dateCreated', 'energy',),
    #     ('exercise', 'height', 'sleep', 'stress', 'water', 'weight',),
    #     ('dateCreated', 'survey', 'surveyID', 'userName',),
    #     ('amountDue', 'dateCreated', 'invoiceID', 'userName',)
    # ]
    # mock_cursor.rowcount = mock.PropertyMock(side_effect=[1, 1, 1, 1, 3, 1, 1, 1, 3])
    # mock_cursor.fetchall.side_effect = [
    #     [{'Feeling down today', 1, 'Sun, 01 Oct 2023 00:00:00 GMT'}],
    #     [{'Keep on exercising!', 'Mon, 02 Oct 2023 00:00:00 GMT', 1, 'Linda White'}],
    #     [{500, 1, 'Sun, 10 Nov 2024 00:00:00 GMT', 5, 2, 70.0, 8, 9, 1, 150}],
    #     [{'Sun, 17 Nov 2024 00:00:00 GMT', '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 1, 'Linda White'}],
    #     [{'[{"q1": "Great!"}, {"q2": 150}, {"q3": true}, {"q4": 9}]', 1, 'Fri, 06 Oct 2023 00:00:00 GMT', '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 'Linda White'}],
    #     [{10.0, 'Sun, 10 Nov 2024 00:00:00 GMT', 3, 'Linda White'}]
    # ]

    # mock_cursor.fetchone.side_effect = [(datetime(2024, 11, 10, 0, 0, 0),), 1]

    # response = app.test_client().post('/patientDashboardData', json={"patientId": 1})
    # response_data = json.loads(response.data.decode("utf-8"))
    # print("Response Data: \n", response_data)

    # assert response.status_code == 200
    # assert {'journalEntry': 'Feeling down today', 'journalID': 1, 'timeDone': 'Sun, 01 Oct 2023 00:00:00 GMT'} == json.loads(response.data.decode("utf-8"))[0][0]
    # assert {'feedback': 'Keep on exercising!', 'feedbackDate': 'Mon, 02 Oct 2023 00:00:00 GMT', 'feedbackID': 1, 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[1][0]
    # assert {'calories': 500, 'dailySurveyID': 1, 'dateCreated': 'Sun, 10 Nov 2024 00:00:00 GMT', 'energy': 5, 'exercise': 2, 'height': 70.0, 'sleep': 8, 'stress': 9, 'water': 1, 'weight': 150} == json.loads(response.data.decode("utf-8"))[2][0]
    # assert {'dateCreated': 'Sun, 17 Nov 2024 00:00:00 GMT', 'survey': '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 'surveyID': 1, 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[3][0]
    # assert {'answers': '[{"q1": "Great!"}, {"q2": 150}, {"q3": true}, {"q4": 9}]', 'completionID': 1, 'dateDone': 'Fri, 06 Oct 2023 00:00:00 GMT', 'questions': '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[4][0]
    # assert {'amountDue': 10.0, 'dateCreated': 'Sun, 10 Nov 2024 00:00:00 GMT', 'invoiceID': 3, 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[5][0]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getJournals(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.description = [
        ('journalID',),
        ('journalEntry',),
        ('timeDone',)
    ]
    mock_cursor.fetchall.return_value = [
        (1, 'Feeling down today', 'Sun, 01 Oct 2023 00:00:00 GMT')
    ]
    
    response = app.test_client().post('/getJournals', json={
        "patientID": 1,
    })
    assert response.status_code == 200
    assert {'journalEntry': 'Feeling down today', 'journalID': 1, 'timeDone': 'Sun, 01 Oct 2023 00:00:00 GMT'} == json.loads(response.data.decode("utf-8"))[0]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getFeedback(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.description = [
        ('feedbackID',), ('feedback',), ('feedbackDate',), ('userName',),
    ]
    mock_cursor.fetchall.return_value = [
        (1, 'Keep on exercising!', 'Mon, 02 Oct 2023 00:00:00 GMT', 'Linda White')
    ]
    
    response = app.test_client().post('/getFeedback', json={
        "patientID": 1,
    })
    assert response.status_code == 200
    assert {'feedbackID': 1, 'feedback': 'Keep on exercising!', 'feedbackDate' : 'Mon, 02 Oct 2023 00:00:00 GMT', 'userName' : 'Linda White'} == json.loads(response.data.decode("utf-8"))[0]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getDailySurveys(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [datetime(2024, 12, 13, 0, 0, 0)]  # mock dateCreated from last survey
    
    # Mock the second SELECT for fetching daily survey data
    mock_cursor.description = [
        ('dailySurveyID',),
        ('dateCreated',),
        ('weight',),
        ('height',),
        ('calories',),
        ('water',),
        ('exercise',),
        ('sleep',),
        ('energy',),
        ('stress',)
    ]
    mock_cursor.fetchall.return_value = [
        (1, '2024-12-13 00:00:00', 150.0, 70.0, 500, 2, 30, 8, 5, 3)
    ]
    response = app.test_client().post('/getFeedback', json={
        "patientID": 1,
    })
    assert response.status_code == 200
    assert {'dailySurveyID': 1,'dateCreated': '2024-12-13 00:00:00','weight': 150.0,'height': 70.0,'calories': 500,'water': 2,'exercise': 30,'sleep': 8,'energy': 5,'stress': 3} == json.loads(response.data.decode("utf-8"))[0]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getIncompleteTherapistSurveys(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.description = [
        ('dateCreated',),
        ('survey',),
        ('surveyID',),
        ('userName',)
    ]
    mock_cursor.fetchall.return_value = [
        ('Sun, 17 Nov 2024 00:00:00 GMT', '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 1, 'Linda White')
    ]
    
    response = app.test_client().post('/getIncompleteTherapistSurveys', json={
        "patientID": 1,
    })
    assert response.status_code == 200
    assert {'dateCreated': 'Sun, 17 Nov 2024 00:00:00 GMT', 'survey': '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 'surveyID': 1, 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[0]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getCompleteTherapistSurveys(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.description = [
        ('answers',),
        ('completionID',),
        ('dateDone',),
        ('questions',),
        ('userName',)
    ]
    mock_cursor.fetchall.return_value = [
        ('[{"q1": "Great!"}, {"q2": 150}, {"q3": true}, {"q4": 9}]', 1, 'Fri, 06 Oct 2023 00:00:00 GMT', '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 'Linda White')
    ]
    
    response = app.test_client().post('/getCompleteTherapistSurveys', json={
        "patientID": 1,
    })
    assert response.status_code == 200
    assert {'answers': '[{"q1": "Great!"}, {"q2": 150}, {"q3": true}, {"q4": 9}]', 'completionID': 1, 'dateDone': 'Fri, 06 Oct 2023 00:00:00 GMT', 'questions': '[{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]', 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[0]

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_getInvoices(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_cursor.execute.return_value = 0
    mock_cursor.description = [
        ('amountDue',),
        ('dateCreated',),
        ('invoiceID',),
        ('userName',)
    ]
    mock_cursor.fetchall.return_value = [
        (10.0, 'Sun, 10 Nov 2024 00:00:00 GMT', 3, 'Linda White')
    ]
    
    response = app.test_client().post('/getInvoices', json={
        "patientID": 1,
    })
    assert response.status_code == 200
    assert {'amountDue': 10.0, 'dateCreated': 'Sun, 10 Nov 2024 00:00:00 GMT', 'invoiceID': 3, 'userName': 'Linda White'} == json.loads(response.data.decode("utf-8"))[0]

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

@mock.patch("flask_mysqldb.MySQL.connection", autospec=True)
def test_completeTherapistSurvey(mock_connection):
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None
    mock_cursor.rowcount = 1
    mock_cursor.fetchall.return_value = []

    request_payload = {
        "userID": 1,
        "patientID": 1,
        "surveyID": 1,
        "questions": [{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}],
        "answers": [{"q1": "Great!"}, {"q2": 150}, {"q3": True}, {"q4": 9}]
    }

    response = app.test_client().post('/completeTherapistSurvey', json=request_payload)
    assert response.status_code == 200
    assert "Success" == json.loads(response.data.decode("utf-8"))["message"]