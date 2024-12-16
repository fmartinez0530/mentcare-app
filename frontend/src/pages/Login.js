import React, { useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../presets.css';
import './styles/Login.css';
import showPassword from './assets/images/show-password.png';
import hidePassword from './assets/images/hide-password.png';


function Login() {
    const inputRefs = useRef({
        email: null,
        password: null
    });

    const passRef = useRef(null);

    //  Need this to redirect user to their dashboard page
    const navigate = useNavigate();

    function checkLogin(e) {
        e.preventDefault();
        const email = inputRefs.current.email.value;
        const password = inputRefs.current.password.value;

        fetch('https://mentcare-backend.onrender.com/patientOrTherapist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        })
            .then(res => res.json())
            .then(data => {
                if (data.userType === 'Patient') {
                    localStorage.setItem('userType', data.userType);
                    localStorage.setItem('userID', data.userID);
                    localStorage.setItem('realUserID', data.realUserID);
                    navigate('/dashboard');
                }
                else if (data.userType === 'Therapist') {
                    localStorage.setItem('userType', data.userType);
                    localStorage.setItem('userID', data.userID);
                    localStorage.setItem('realUserID', data.realUserID)
                    localStorage.setItem('isActive', data.isActive);
                    if (data.isActive === 0) {
                        navigate('/deactivated');
                    }
                    else {
                        navigate('/dashboard');
                    }
                }
            })
            .catch(err => console.error('Error fetching data:', err));
    }

    function togglePasswordVisibility() {
        if (inputRefs.current.password.type === 'password') {
            inputRefs.current.password.type = 'text';
            passRef.current.src = showPassword;
            passRef.current.style.top = '44px';
        }
        else {
            inputRefs.current.password.type = 'password';
            passRef.current.src = hidePassword;
            passRef.current.style.top = '42px';
        }
    }

    return (
        <div className="default-form-container">
            <h1>LOG IN</h1>
            <form>
                <div className='flex-col input-container'>
                    <label>Email</label>
                    <input type="text" className='email-input' ref={el => (inputRefs.current.email = el)} required={true}></input>
                </div>

                <div className='flex-col input-container'>
                    <label>Password</label>
                    <input type="password" className='password-input' ref={el => (inputRefs.current.password = el)}></input>
                    <img
                        src={hidePassword}
                        alt='reveal-password'
                        ref={el => (passRef.current = el)}
                        className='password-toggle-btn'
                        onClick={() => togglePasswordVisibility()}
                    />
                    {/* <Link to={'/forgot_password'}>Forgot Password?</Link> */}
                </div>

                <div className='flex-col flex-centered margin-top-15'>
                    <input className='loginBtn' type='submit' value={'LOG IN'} onClick={(e) => checkLogin(e)}></input>
                    <div className='flex-row flex-centered redirect-register'>
                        New to MentCare?&nbsp;
                        <Link to={'/register'} className='clickable-register'>Register Now</Link>
                    </div>
                </div>
            </form>
        </div>
    );
}

export default Login;