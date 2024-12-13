import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const TherapistList = () => {
  const [therapists, setTherapists] = useState([]);
  const navigate = useNavigate();

  // Fetch therapist list from the backend
  useEffect(() => {
    fetch('https://mentcare-backend.onrender.com/api/therapists')
      .then((response) => response.json())
      .then((data) => setTherapists(data.Therapists))
      .catch((error) => console.error('Error fetching therapists:', error));
  }, []);

  const viewProfile = (userId) => {
    navigate(`/therapistprofile/${userId}`);
  };

  return (
    <div>
      <h1>Therapist List</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {therapists.map((therapist) => (
          <div
            key={therapist.UserID}
            style={{
              border: '1px solid #ccc',
              padding: '20px',
              margin: '10px',
              width: '200px',
            }}
          >
            <h3>{therapist.Username}</h3>
            <p>Specialization: {therapist.Specializations}</p>
            <button onClick={() => viewProfile(therapist.UserID)}>View Profile</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TherapistList;
