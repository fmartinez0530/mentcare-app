import React from 'react';
import './App.css';
import { ToastContainer, toast } from 'react-toastify';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import TherapistProfile from './pages/TherapistProfile';
import Chat from './pages/Chat';
import TherapistListPage from './pages/TherapistListPage';
import SettingsPage from './pages/Settings';
import TherapistList from './pages/TherapistList';
import PatientOverview from './pages/PatientOverview';
import Payment from './pages/Payment';
import Deactivated from './pages/Deactivated';

function App() {
  return (
    <Router>
      <Navbar />
      <ToastContainer />
      <Routes>
        <Route index element={<LandingPage />} />
        <Route path='/login' element={<Login />} />
        <Route path='/register' element={<Register />} />
        <Route path='/dashboard' element={<Dashboard />} />
        <Route path='/therapistprofile' element={<TherapistProfile />} />
        <Route path='/chat' element={<Chat />} />
        <Route path="/therapistlist" element={<TherapistListPage />} />
        <Route path='/settings' element={<SettingsPage />} />
        <Route path="/patient-overview/:userID" element={<PatientOverview />} />
        <Route path="/therapistprofilelist" element={<TherapistList />} />
        <Route path="/therapistprofile/:userId" element={<TherapistProfile />} />
        <Route path="/payment" element={<Payment />} />
        <Route path="/deactivated" element={<Deactivated />} />
      </Routes>
    </Router>
  );
}

export default App;
