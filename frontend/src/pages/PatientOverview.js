import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import Plot from "react-plotly.js";
import "./styles/PatientOverview.css";

const PatientOverview = () => {
  const { userID } = useParams();
  const [patientData, setPatientData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [newFeedback, setNewFeedback] = useState("");
  const [newJournalEntry, setNewJournalEntry] = useState("");
  const [selectedSurvey, setSelectedSurvey] = useState(null); // For modal details
  const [surveyDetails, setSurveyDetails] = useState(null);

  useEffect(() => {
    const fetchPatientData = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/patient-overview/${userID}`
        );
        setPatientData(response.data);
        setLoading(false);
      } catch (err) {
        setError("Error fetching patient data.");
        setLoading(false);
      }
    };

    fetchPatientData();
  }, [userID]);

  const fetchSurveyDetails = async (completionID) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/daily-survey-details/${completionID}`
      );
      setSurveyDetails(response.data);
    } catch (err) {
      setSurveyDetails(null);
      alert("Failed to fetch survey details.");
    }
  };

  const handleAddFeedback = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/add-feedback", {
        userID,
        feedback: newFeedback,
      });
      alert("Feedback added successfully.");
      setNewFeedback("");
    } catch (err) {
      alert("Failed to add feedback.");
    }
  };

  const handleAddJournal = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/add-journal", {
        userID,
        journalEntry: newJournalEntry,
      });
      alert("Journal entry added successfully.");
      setNewJournalEntry("");
    } catch (err) {
      alert("Failed to add journal.");
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  const {
    userName,
    profileImg,
    allRecordsViewable,
    dailySurveys,
    feedback,
    journals,
  } = patientData;

  const surveyGraphData = dailySurveys.map((survey) => ({
    x: survey.surveyDate,
    y: [
      survey.weight,
      survey.height,
      survey.calories,
      survey.water,
      survey.exercise,
      survey.sleep,
      survey.energy,
      survey.stress,
    ],
    type: "bar",
    name: survey.surveyDate,
  }));

  return (
    <div className="patient-overview">
      <div className="profile-section flex-col flex-centered">
        <img
          src={profileImg ? `/assets/profile-pics/${profileImg}` : "https://via.placeholder.com/100"}
          alt="Profile"
          className="profile-picture"
        />
        <h2 className="patient-name">{userName}</h2>
        <div className="share-records">
          <label>
            <input type="checkbox" checked={allRecordsViewable} readOnly />
            Share Records w/ other therapists
          </label>
        </div>
      </div>

      <div className="overview-cards-section">
        <div className="overview-card">
          <h3>Daily Surveys</h3>
          <div className="overview-card-content scrollable">
            {dailySurveys.length > 0 ? (
              dailySurveys.map((survey) => (
                <button
                  key={survey.completionID}
                  className="overview-card-row"
                  onClick={() => {
                    setSelectedSurvey(survey);
                    fetchSurveyDetails(survey.completionID);
                  }}
                >
                  {`${survey.surveyDate} - Health Status`}
                </button>
              ))
            ) : (
              <p>No daily surveys available</p>
            )}
          </div>
        </div>

        <div className="overview-card">
          <h3>Feedback</h3>
          <div className="overview-card-content scrollable">
            {feedback.length > 0 ? (
              feedback.map((fb) => (
                <button key={fb.feedbackID} className="overview-card-row">
                  {`${fb.feedbackDate} - ${fb.feedback}`}
                </button>
              ))
            ) : (
              <p>No feedback available</p>
            )}
          </div>
          <textarea
            value={newFeedback}
            onChange={(e) => setNewFeedback(e.target.value)}
            placeholder="Write feedback..."
            className="styled-textarea"
          />
          <button onClick={handleAddFeedback} className="add-button">
            Add Feedback
          </button>
        </div>

        <div className="overview-card">
          <h3>Journals</h3>
          <div className="overview-card-content scrollable">
            {journals.length > 0 ? (
              journals.map((journal) => (
                <button key={journal.journalID} className="overview-card-row">
                  {`${journal.timeDone} - ${journal.journalEntry}`}
                </button>
              ))
            ) : (
              <p>No journals available</p>
            )}
          </div>
          <textarea
            value={newJournalEntry}
            onChange={(e) => setNewJournalEntry(e.target.value)}
            placeholder="Write journal entry..."
            className="styled-textarea"
          />
          <button onClick={handleAddJournal} className="add-button">
            Add Journal
          </button>
        </div>
      </div>

      <div className="graph-section">
        <h3>Patient Health Graph</h3>
        <Plot
          data={surveyGraphData}
          layout={{
            title: "Daily Survey Data",
            xaxis: { title: "Survey Date" },
            yaxis: { title: "Metrics" },
            barmode: "group",
          }}
        />
      </div>

      {selectedSurvey && surveyDetails && (
        <div className="modal">
          <div className="modal-content">
            <h3>Daily Survey Details</h3>
            <p>Date: {surveyDetails.dateCreated}</p>
            <p>Weight: {surveyDetails.weight}</p>
            <p>Height: {surveyDetails.height}</p>
            <p>Calories: {surveyDetails.calories}</p>
            <p>Water: {surveyDetails.water}</p>
            <p>Exercise: {surveyDetails.exercise}</p>
            <p>Sleep: {surveyDetails.sleep}</p>
            <p>Energy: {surveyDetails.energy}</p>
            <p>Stress: {surveyDetails.stress}</p>
            <button onClick={() => setSelectedSurvey(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientOverview;







