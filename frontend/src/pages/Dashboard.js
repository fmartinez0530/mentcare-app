import PatientDashboard from './PatientDashboard';
import TherapistDashboard from './TherapistDashboard';

function Dashboard() {
    const userType = localStorage.getItem('userType');
    if (userType === 'Patient') {
        return <PatientDashboard />;
    } else if (userType === 'Therapist') {
        return <TherapistDashboard />;
    }

    return <div>Loading...</div>;
}

export default Dashboard;