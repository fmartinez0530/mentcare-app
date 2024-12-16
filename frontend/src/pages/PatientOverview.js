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
  const [selectedMetrics, setSelectedMetrics] = useState([]);
  const [multiMetric, setMultiMetric] = useState(false);

  useEffect(() => {
    const fetchPatientData = async () => {
      try {
        const response = await axios.get(
          `https://mentcare-backend.onrender.com/patient-overview/${userID}`
        );
        setPatientData(response.data);
        console.log(response.data)
        setLoading(false);
      } catch (err) {
        setError("Error fetching patient data.");
        setLoading(false);
      }
    };

    fetchPatientData();
  }, [userID]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  const { userName, profileImg, dailySurveys, feedback, journals } =
    patientData;

  const metrics = [
    { name: "Weight", key: "weight" },
    { name: "Height", key: "height" },
    { name: "Calories", key: "calories" },
    { name: "Water", key: "water" },
    { name: "Exercise", key: "exercise" },
    { name: "Sleep", key: "sleep" },
    { name: "Energy", key: "energy" },
    { name: "Stress", key: "stress" },
  ];

  const toggleMetric = (metricKey) => {
    if (multiMetric) {
      setSelectedMetrics((prev) =>
        prev.includes(metricKey)
          ? prev.filter((key) => key !== metricKey)
          : [...prev, metricKey]
      );
    } else {
      setSelectedMetrics([metricKey]);
    }
  };

  const toggleMultiMetric = () => {
    setMultiMetric(!multiMetric);
    setSelectedMetrics([]); // Reset selections
  };

  const uniqueDays = Array.from(
    new Set(dailySurveys.map((survey) => survey.surveyDate))
  );

  const formattedSurveys = uniqueDays
    .map((date) => {
      const survey = dailySurveys.find((s) => s.surveyDate === date);
      return {
        ...survey,
        surveyDate: new Date(date).toLocaleDateString(), // Format date as MM/DD/YYYY
      };
    })
    .sort((a, b) => new Date(a.surveyDate) - new Date(b.surveyDate)); // Sort dates in ascending order

  return (
    <div className="patient-overview">
      <div className="profile-section flex-col flex-centered">
        <img
          src={profileImg ? `/assets/profile-pics/${profileImg}` : "https://via.placeholder.com/100"}
          alt="Profile"
          className="profile-picture"
        />
        <h2 className="patient-name">{userName}</h2>
      </div>

      <div className="overview-cards-section">
        <div className="overview-card">
          <h3>Feedback</h3>
          <div className="overview-card-content">
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
        </div>

        <div className="overview-card">
          <h3>Journals</h3>
          <div className="overview-card-content">
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
        </div>
      </div>

      <div className="add-feedback-section">
        <h3 className="add-feedback-title">Add Feedback</h3>
        <textarea
          className="styled-textarea"
          placeholder="Write feedback..."
        />
        <button className="add-button">Submit</button>
      </div>

      <div className="graph-section">
        <div className="graph-controls">
          <label style={{ fontWeight: "bold", color: "#20c997" }}>
            Which metric(s) do you want to see?
          </label>
          <div className="metric-buttons">
            {metrics.map((metric) => (
              <button
                key={metric.key}
                style={{
                  backgroundColor: selectedMetrics.includes(metric.key)
                    ? "#20c997"
                    : "#ddd",
                  color: selectedMetrics.includes(metric.key)
                    ? "white"
                    : "black",
                }}
                onClick={() => toggleMetric(metric.key)}
              >
                {metric.name}
              </button>
            ))}
            <label style={{ marginTop: "10px" }}>
              <input
                type="checkbox"
                checked={multiMetric}
                onChange={toggleMultiMetric}
              />
              Show Multiple Metrics
            </label>
          </div>
        </div>
        <div className="graph-container">
          <Plot
            data={
              selectedMetrics.length > 0
                ? selectedMetrics.map((metricKey) => ({
                  x: formattedSurveys.map((survey) => survey.surveyDate),
                  y: formattedSurveys.map((survey) => survey[metricKey]),
                  type: "scatter",
                  mode: "lines+markers",
                  name: metrics.find((metric) => metric.key === metricKey)
                    .name,
                }))
                : []
            }
            layout={{
              xaxis: { title: "Date" },
              yaxis: { title: "Value" },
              showlegend: true,
              margin: { t: 100 },
              title: {
                text: "Patient Metrics",
                font: {
                  color: "#20c997",
                  family: "Arial, sans-serif",
                  size: 23,
                  weight: "bold",
                },
              },
            }}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
      </div>
    </div>
  );
};

export default PatientOverview;

























