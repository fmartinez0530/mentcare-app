import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import '../presets.css';
import './styles/Register.css';
import defaultProfilePic from './assets/images/default-profile-pic.jpg';
import showPassword from './assets/images/show-password.png';
import hidePassword from './assets/images/hide-password.png';
import ManIcon from '@mui/icons-material/Man';
import WomanIcon from '@mui/icons-material/Woman';
import WcIcon from '@mui/icons-material/Wc';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';

const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
});

function Register() {
    const [patientFormVisibility, setPatientFormVisibility] = useState("visible");
    const [therapistFormVisibility, setTherapistFormVisibility] = useState('hidden');
    const [therapistPageOneVisibility, setTherapistPageOneVisibility] = useState("visible");
    const [therapistPageTwoVisibility, setTherapistPageTwoVisibility] = useState("hidden");
    const [pageOneVisibility, setPageOneVisibility] = useState("visible");
    const [pageTwoVisibility, setPageTwoVisibility] = useState("hidden");
    const [pageThreeVisibility, setPageThreeVisibility] = useState("hidden");
    const [pageFourVisibility, setPageFourVisibility] = useState("hidden");
    const [licenseValue, setLicenseValue] = useState('');
    const [selectedGender, setSelectedGender] = useState(null);

    const [patientProfilePic, setPatientProfilePic] = useState(null);
    const [patientProfilePicURL, setPatientProfilePicURL] = useState(defaultProfilePic);
    const [therapistProfilePic, setTherapistProfilePic] = useState(null);
    const [therapistProfilePicURL, setTherapistProfilePicURL] = useState(defaultProfilePic);

    const [hasUpdatedPatientProfilePic, setUpdatedPatientProfilePic] = useState(false);
    const [hasUpdatedTherapistProfilePic, setUpdatedTherapistProfilePic] = useState(false);

    //  Need this to redirect user to their dashboard page
    const navigate = useNavigate();

    const genderRefs = useRef({
        patientMaleBtn: null,
        patientFemaleBtn: null,
        patientOtherBtn: null,
        therapistMaleBtn: null,
        therapistFemaleBtn: null,
        therapistOtherBtn: null
    })

    const passRef = useRef({
        patientPass: null,
        therapistPass: null
    });

    const formRefs = useRef({
        patientPageOne: null,
        patientPageThree: null,
        patientRegister: null,
        therapistPageOne: null,
        therapistRegister: null
    });

    const infoRefs = useRef({
        firstName: null,
        lastName: null,
        email: null,
        password: null,
        license: null,
        tosAgreement: null,
        patientBtn: null,
        therapistBtn: null
    });

    const insuranceRefs = useRef({
        company: null,
        id: null,
        tier: null
    });

    const answersRefs = useRef({
        weight: null,
        height: null,
        calories: null,
        water: null,
        exercise: null,
        sleep: null,
        energy: null,
        stress: null
    });

    const infoTherapistRefs = useRef({
        fname: null,
        lname: null,
        email: null,
        password: null,
        license: null,
        tosAgreement: null,
        gridContainer: null
    });

    async function validateEmail(e, userType) {

        const email = userType === 'Patient' ? infoRefs.current.email.value : infoTherapistRefs.current.email.value;
        try {
            const response = await fetch('https://mentcare-backend.onrender.com/validateUserEmail', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });
            if (response.status === 200) {
                console.log("Email is available for registration.");
                return true;
            } else {
                clearWaitingQueue();
                toast.error("Email already in use! Please use a different email to continue.");
                return false;
            }
        } catch (err) {
            console.error('Error during email validation:', err);
            return false;  // In case of error (e.g., network issues)
        }
    }

    async function verifyLicense() {
        try {
            const formData = new FormData()
            formData.append('licenseNum', licenseValue);
            console.log(formData);
            const response = await fetch(`https://q0vvl.wiremockapi.cloud/verifyTherapistLicense?licenseNum=${licenseValue}`, {
                method: 'GET',
            });
            if (response.ok) {
                // alert("LICENSE NUMBER IS VALID!")
                return true;
            } else {
                toast.error("License number invalid! Please use a valid number to continue.");
                return false;
            }
        } catch (err) {
            console.error('Error duing therapist registration:', err);
            return false;  // In case of error (e.g., network issues)
        }
    }

    async function registerPatient(e) {
        e.preventDefault();
        const form = formRefs.current.patientRegister;
        if (form.checkValidity()) {
            const fname = infoRefs.current.firstName.value;
            const lname = infoRefs.current.lastName.value;
            const email = infoRefs.current.email.value;
            const password = infoRefs.current.password.value;
            const tosAgreement = infoRefs.current.tosAgreement.checked;
            const company = insuranceRefs.current.company.value;
            const insuranceId = insuranceRefs.current.id.value;
            const tier = insuranceRefs.current.tier.value;
            const weight = answersRefs.current.weight.value;
            const height = answersRefs.current.height.value;
            const calories = answersRefs.current.calories.value;
            const water = answersRefs.current.water.value;
            const exercise = answersRefs.current.exercise.value;
            const sleep = answersRefs.current.sleep.value;
            const energy = answersRefs.current.energy.value;
            const stress = answersRefs.current.stress.value;

            const formData = new FormData();
            formData.append('fname', fname);
            formData.append('lname', lname);
            formData.append('email', email);
            formData.append('password', password);
            formData.append('gender', selectedGender);
            formData.append('company', company);
            formData.append('insuranceId', insuranceId);
            formData.append('tier', tier);
            formData.append('weight', weight);
            formData.append('height', height);
            formData.append('calories', calories);
            formData.append('water', water);
            formData.append('exercise', exercise);
            formData.append('sleep', sleep);
            formData.append('energy', energy);
            formData.append('stress', stress);

            if (hasUpdatedPatientProfilePic) {
                console.log(patientProfilePic);
                formData.append('profileImg', patientProfilePic);
            }

            try {
                const response = await fetch('https://mentcare-backend.onrender.com/registerPatient', {
                    method: 'POST',
                    body: formData,
                });
                if (response.ok) {
                    const data = await response.json()
                    localStorage.setItem('userID', data.patientID);
                    localStorage.setItem('realUserID', data.userID)
                    localStorage.setItem('userType', 'Patient');
                    navigate('/dashboard');
                    return true;
                } else {
                    alert("Patient Registration Failed. Try Again!");
                    return false;
                }
            } catch (err) {
                console.error('Error duing patient registration:', err);
                return false;  // In case of error (e.g., network issues)
            }
        }
        else {
            form.reportValidity();
        }
    }

    async function registerTherapist(e) {
        e.preventDefault();
        const form = formRefs.current.therapistRegister;
        if (form.checkValidity()) {
            const isEmailValid = await validateEmail(e, 'Therapist');
            const isLicenseVaild = await verifyLicense(infoTherapistRefs.current.license.value);
            if (isEmailValid && isLicenseVaild) {
                const specsArr = infoTherapistRefs.current.gridContainer.children;
                let specializations = []
                Array.from(specsArr).forEach(element => {
                    if (element.className === 'grid-spec selected-spec') {
                        specializations.push(element.value);
                    }
                });
                const fname = infoTherapistRefs.current.fname.value;
                const lname = infoTherapistRefs.current.lname.value;
                const email = infoTherapistRefs.current.email.value;
                const password = infoTherapistRefs.current.password.value;
                const license = infoTherapistRefs.current.license.value;

                const formData = new FormData();
                formData.append('fname', fname);
                formData.append('lname', lname);
                formData.append('email', email);
                formData.append('password', password);
                formData.append('gender', selectedGender);
                formData.append('license', license);
                formData.append('specializations', specializations.join(','));

                if (hasUpdatedTherapistProfilePic) {
                    formData.append('profileImg', therapistProfilePic, therapistProfilePic.filename);
                }

                try {
                    const response = await fetch('https://mentcare-backend.onrender.com/registerTherapist', {
                        method: 'POST',
                        body: formData,
                    });
                    if (response.ok) {
                        const data = await response.json()
                        localStorage.setItem('userID', data.therapistID);
                        localStorage.setItem('realUserID', data.userID)
                        localStorage.setItem('userType', 'Therapist');
                        localStorage.setItem('isActive', true);
                        navigate('/dashboard');
                        return true;
                    } else {
                        alert("Therapist Registration Failed. Try Again!");
                        return false;
                    }
                } catch (err) {
                    console.error('Error duing therapist registration:', err);
                    return false;  // In case of error (e.g., network issues)
                }

                // fetch('https://mentcare-backend.onrender.com/registerTherapist', {
                //     method: 'POST',
                //     body: formData,
                // })
                //     .then((res) => {
                //         if (res.ok) {
                //             localStorage.setItem('userType', 'Therapist');
                //             navigate('/dashboard');
                //         }
                //         return res.json();
                //     })
                //     .then(data => {
                //         // console.log("UserID: ", data.userID);
                //         localStorage.setItem('userID', data.therapistID);
                //         localStorage.setItem('realUserID', data.userID)

                //     })
                //     .catch(err => console.error('Error updating rental:', err));
            }
        }
        else {
            form.reportValidity();
        }
    }

    function changeUserRegister(btn) {
        if (infoRefs.current.therapistBtn && infoRefs.current.patientBtn) {
            if (btn) {
                //  Swith to therapist button & de-select patient button
                infoRefs.current.therapistBtn.className = 'pt-button selected-pt-btn';
                infoRefs.current.patientBtn.className = 'pt-button';
                hidePatientForm();
            } else {
                //  Do the opposite
                infoRefs.current.therapistBtn.className = 'pt-button';
                infoRefs.current.patientBtn.className = 'pt-button selected-pt-btn';
                displayPatientForm();
            }
        }
    }

    //  Used to make the patient registration form visible
    function displayPatientForm() {
        setPatientFormVisibility("visible");
        setTherapistFormVisibility("hidden");
    }
    //  Used to hide the patient registration form
    function hidePatientForm() {
        setPatientFormVisibility("hidden");
        setTherapistFormVisibility("visible");
    }

    async function goToNextPage(e, page, userType) {
        e.preventDefault();
        if (userType === 'Patient') {
            if (page === 1) {
                const form = formRefs.current.patientPageOne;
                if (form.checkValidity()) {
                    const isEmailValid = await validateEmail(e, 'Patient');
                    if (isEmailValid) {
                        setPageOneVisibility('hidden');
                        setPageTwoVisibility('visible');
                        setPageThreeVisibility('hidden');
                        setPageFourVisibility('hidden');
                        console.log("success hide next");
                    }
                }
                else {
                    form.reportValidity();
                }
            }
            else if (page === 2) {
                setPageOneVisibility('hidden');
                setPageTwoVisibility('hidden');
                setPageThreeVisibility('visible');
                setPageFourVisibility('hidden');
            }
            else if (page === 3) {
                const form = formRefs.current.patientPageThree;
                if (form.checkValidity()) {
                    setPageOneVisibility('hidden');
                    setPageTwoVisibility('hidden');
                    setPageThreeVisibility('hidden');
                    setPageFourVisibility('visible');
                }
                else {
                    form.reportValidity();
                }
            }
        }
        else if (userType === 'Therapist') {
            if (page === 1) {
                const form = formRefs.current.therapistPageOne;
                if (form.checkValidity()) {
                    const isEmailValid = await validateEmail(e, 'Therapist');
                    if (isEmailValid) {
                        setTherapistPageOneVisibility('hidden');
                        setTherapistPageTwoVisibility('visible');
                    }
                }
                else {
                    form.reportValidity();
                }
            }
        }
    }

    function goToPreviousPage(userType) {
        if (userType === 'Patient') {
            if (pageTwoVisibility === 'visible') {
                setPageOneVisibility('visible');
                setPageTwoVisibility('hidden');
                setPageThreeVisibility('hidden');
                setPageFourVisibility('hidden');
                console.log("success hide");
            }
            else if (pageThreeVisibility === 'visible') {
                setPageOneVisibility('hidden');
                setPageTwoVisibility('visible');
                setPageThreeVisibility('hidden');
                setPageFourVisibility('hidden');
            }
            else if (pageFourVisibility === 'visible') {
                setPageOneVisibility('hidden');
                setPageTwoVisibility('hidden');
                setPageThreeVisibility('visible');
                setPageFourVisibility('hidden');
            }
        } else if (userType === 'Therapist') {
            if (therapistPageTwoVisibility === 'visible') {
                setTherapistPageOneVisibility('visible');
                setTherapistPageTwoVisibility('hidden');
            }
        }
    }

    function selectedSpecialization(e) {
        if (e.target.className === 'grid-spec') {
            e.target.className = 'grid-spec selected-spec';
        }
        else {
            e.target.className = 'grid-spec';
        }
    }

    function handleNumberFieldInput(e) {
        const inputValue = e.target.value.toString();
        const numericValue = inputValue.replace(/[^0-9]/g, '');
        setLicenseValue(String(numericValue));
    }

    function handleImageFileChange(event, user) {
        const file = event.target.files[0];
        if (file) {
            const fileURL = URL.createObjectURL(file);
            if (user === 'Patient') {
                setUpdatedPatientProfilePic(true);
                setPatientProfilePicURL(fileURL)
                setPatientProfilePic(file);
            } else {
                setUpdatedTherapistProfilePic(true);
                setTherapistProfilePicURL(fileURL)
                setTherapistProfilePic(file);
            }
        }
    };

    function togglePasswordVisibility(userType) {
        if (userType === 'Patient') {
            if (infoRefs.current.password.type === 'password') {
                infoRefs.current.password.type = 'text';
                passRef.current.patientPass.src = showPassword;
                passRef.current.patientPass.style.top = '44px';
            }
            else {
                infoRefs.current.password.type = 'password';
                passRef.current.patientPass.src = hidePassword;
                passRef.current.patientPass.style.top = '42px';
            }
        }
        else if (userType === 'Therapist') {
            if (infoTherapistRefs.current.password.type === 'password') {
                infoTherapistRefs.current.password.type = 'text';
                passRef.current.therapistPass.src = showPassword;
                passRef.current.therapistPass.style.top = '44px';
            }
            else {
                infoTherapistRefs.current.password.type = 'password';
                passRef.current.therapistPass.src = hidePassword;
                passRef.current.therapistPass.style.top = '42px';
            }
        }
    }

    function selectGender(gender, userType) {
        if (gender === 'Male') {
            if (selectedGender === 'Male') {
                genderRefs.current[`${userType}MaleBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}MaleBtn`].style.color = 'white';
                setSelectedGender(null);
            }
            else {
                genderRefs.current[`${userType}MaleBtn`].style.borderColor = 'blue';
                genderRefs.current[`${userType}MaleBtn`].style.color = 'blue';
                genderRefs.current[`${userType}FemaleBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}FemaleBtn`].style.color = 'white';
                genderRefs.current[`${userType}OtherBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}OtherBtn`].style.color = 'white';
                setSelectedGender('Male');
            }
        }
        else if (gender === 'Female') {
            if (selectedGender === 'Female') {
                genderRefs.current[`${userType}FemaleBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}FemaleBtn`].style.color = 'white';
                setSelectedGender(null);
            }
            else {
                genderRefs.current[`${userType}MaleBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}MaleBtn`].style.color = 'white';
                genderRefs.current[`${userType}FemaleBtn`].style.borderColor = 'pink';
                genderRefs.current[`${userType}FemaleBtn`].style.color = 'pink';
                genderRefs.current[`${userType}OtherBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}OtherBtn`].style.color = 'white';
                setSelectedGender('Female');
            }

        }
        else {
            if (selectedGender === 'Other') {
                genderRefs.current[`${userType}OtherBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}OtherBtn`].style.color = 'white';
                setSelectedGender(null);
            }
            else {
                genderRefs.current[`${userType}MaleBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}MaleBtn`].style.color = 'white';
                genderRefs.current[`${userType}FemaleBtn`].style.borderColor = 'white';
                genderRefs.current[`${userType}FemaleBtn`].style.color = 'white';
                genderRefs.current[`${userType}OtherBtn`].style.borderColor = 'purple';
                genderRefs.current[`${userType}OtherBtn`].style.color = 'purple';
                setSelectedGender('Other');
            }
        }
    }

    const clearWaitingQueue = () => {
        toast.clearWaitingQueue();
    }

    return (
        <>
            <ToastContainer
                limit={1}
                position="bottom-left"
                closeButton={false}
                hideProgressBar={true}
                pauseOnHover={false}
                autoClose={3000}
            />
            {/* Patient Registration Form */}
            <div className={patientFormVisibility}>

                {/* PAGE 1 OF 4 */}
                <div className={`register-form flex-col ${pageOneVisibility}`}>
                    <div className='flex-col flex-centered'>
                        <h1 className='title'>REGISTER</h1>
                        <div className='subtitle'>Are you a...</div>
                        <div style={{ display: 'flex', gap: '20px' }}>
                            <input type='button' value={'PATIENT'} className=' pt-button selected-pt-btn' ref={el => (infoRefs.current.patientBtn = el)} onClick={() => { changeUserRegister(0) }}></input>
                            <input type='button' value={'THERAPIST'} className='pt-button ' ref={el => (infoRefs.current.therapistBtn = el)} onClick={() => { changeUserRegister(1) }}></input>
                        </div>
                    </div>

                    <form onSubmit={goToNextPage} ref={el => (formRefs.current.patientPageOne = el)}>
                        <div className='flex-row' style={{ gap: '60px' }}>
                            <div className='patient-input-container'>
                                <div className='flex-row' style={{ justifyContent: 'space-between', width: '100%' }}>
                                    <div className='flex-col reg-input-container'>
                                        <label>First Name</label>
                                        <input type="text" required ref={el => (infoRefs.current.firstName = el)} className='reg-name-input reg-user-input'></input>
                                    </div>

                                    <div className='flex-col reg-input-container'>
                                        <label>Last Name</label>
                                        <input type="text" required ref={el => (infoRefs.current.lastName = el)} className='reg-name-input reg-user-input'></input>
                                    </div>
                                </div>

                                <div className='flex-col reg-input-container'>
                                    <label>Email</label>
                                    <input type="text" required ref={el => (infoRefs.current.email = el)} className='reg-user-input' style={{ width: 300 }}></input>
                                </div>

                                <div className='flex-col reg-input-container'>
                                    <label>Password</label>
                                    <input type="password" required ref={el => (infoRefs.current.password = el)} className='reg-user-input' style={{ width: 300 }}></input>
                                    <img
                                        src={hidePassword}
                                        alt='reveal-password'
                                        ref={el => (passRef.current.patientPass = el)}
                                        className='reg-password-toggle-btn'
                                        onClick={() => togglePasswordVisibility('Patient')}
                                    />
                                </div>

                                <div className='flex-centered'>
                                    <input type='checkbox' required name='checkboxInput' ref={el => (infoRefs.current.tosAgreement = el)}></input>
                                    <label htmlFor='checkboxInput'>
                                        I agree to the Terms of Service.
                                    </label>
                                </div>
                            </div>
                            <div className='flex-col'>
                                <div className='flex-col reg-input-container'>
                                    <label>Gender</label>
                                    <div className='flex-row' style={{ gap: '5px' }}>
                                        <Button
                                            variant="outlined"
                                            className='flex-col'
                                            style={{ backgroundColor: 'rgb(52, 196, 169)', color: 'white', borderColor: 'white', border: '2px solid', width: '50px' }}
                                            ref={el => (genderRefs.current.patientMaleBtn = el)}
                                            onClick={() => selectGender('Male', 'patient')}
                                        >
                                            <ManIcon sx={{ fontSize: 40 }}></ManIcon>
                                            <label style={{ fontSize: 13 }}>Male</label>
                                        </Button>
                                        <Button
                                            variant="outlined"
                                            className='flex-col'
                                            style={{ backgroundColor: 'rgb(52, 196, 169)', color: 'white', borderColor: 'white', border: '2px solid', width: '50px' }}
                                            ref={el => (genderRefs.current.patientFemaleBtn = el)}
                                            onClick={() => selectGender('Female', 'patient')}
                                        >
                                            <WomanIcon sx={{ fontSize: 40 }}></WomanIcon>
                                            <label style={{ fontSize: 13 }}>Female</label>
                                        </Button>
                                        <Button
                                            variant="outlined"
                                            className='flex-col'
                                            style={{ backgroundColor: 'rgb(52, 196, 169)', color: 'white', borderColor: 'white', border: '2px solid', width: '50px' }}
                                            ref={el => (genderRefs.current.patientOtherBtn = el)}
                                            onClick={() => selectGender('Other', 'patient')}
                                        >
                                            <WcIcon sx={{ fontSize: 40 }}></WcIcon>
                                            <label style={{ fontSize: 13 }}>Other</label>
                                        </Button>
                                    </div>
                                </div>
                                <div className='profile-pic-container'>
                                    <div className="img-circle-mask" style={{ width: '125px', height: '125px' }}>
                                        <img src={patientProfilePicURL} alt='PROFILE PIC' className="profile-pic" />
                                    </div>
                                    {/* <div>Upload Profile Picture</div>
                                <input type="file" style={{ width: "180px" }} onChange={(e) => handleImageFileChange(e, 'Patient')} /> */}
                                    <Button
                                        component="label"
                                        role={undefined}
                                        variant="contained"
                                        tabIndex={-1}
                                        size="small"
                                    >
                                        Upload Picture
                                        <VisuallyHiddenInput
                                            type="file"
                                            onChange={(e) => handleImageFileChange(e, 'Patient')}
                                            multiple
                                        />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </form>

                    <div className='flex-col' style={{ alignItems: "center" }}>
                        <button className='pageBtn' onClick={(e) => goToNextPage(e, 1, 'Patient')}>NEXT</button>
                    </div>
                </div >

                {/* PAGE 2 OF 4 */}
                < div className={`register-form flex-col flex-centered ${pageTwoVisibility}`}>
                    <div className='flex-col flex-centered'>
                        <h1 className='title'>REGISTER</h1>
                        <div className='subtitle'>Health Insurance (OPTIONAL)</div>
                    </div>

                    <div className='flex-col' style={{ gap: '20px', width: '300px' }}>
                        <div className='flex-col reg-input-container'>
                            <label>Insurance Company</label>
                            <input type="text" ref={el => (insuranceRefs.current.company = el)} className='reg-user-input'></input>
                        </div>

                        <div className='flex-col reg-input-container'>
                            <label>Insurance ID</label>
                            <input type="text" ref={el => (insuranceRefs.current.id = el)} className='reg-user-input'></input>
                        </div>

                        <div className='flex-col reg-input-container'>
                            <label>Insurance Tier</label>
                            <input type="text" ref={el => (insuranceRefs.current.tier = el)} className='reg-user-input'></input>
                        </div>
                    </div>

                    <div className='flex-row flex-centered' style={{ gap: '10px' }}>
                        <input className='pageBtn' type='button' value={'BACK'} onClick={() => goToPreviousPage('Patient')}></input>
                        <input className='pageBtn' type='button' value={'NEXT'} onClick={(e) => goToNextPage(e, 2, 'Patient')}></input>
                    </div>
                </div >

                {/* PAGE 3 OF 4 */}
                < div className={`register-form flex-col ${pageThreeVisibility}`}>
                    <div className='flex-col flex-centered'>
                        <h1 className='title'>REGISTER</h1>
                        <div className='subtitle'>Initial Questionnaire (1 of 2)</div>
                    </div>
                    <form onSubmit={goToNextPage} ref={el => (formRefs.current.patientPageThree = el)}>
                        <div className='flex-col reg-questionnaire-container'>
                            <div className='flex-row flex-centered reg-question-container' style={{ justifyContent: 'space-between' }}>
                                <label>What is your current weight? (in pounds)</label>
                                <input type="number" required className='userIntInput' ref={el => (answersRefs.current.weight = el)}></input>
                            </div>

                            <div className='flex-row flex-centered reg-question-container' style={{ justifyContent: 'space-between' }}>
                                <label>How tall are you? (in feet)</label>
                                <input type="number" step='0.1' required className='userIntInput' ref={el => (answersRefs.current.height = el)}></input>
                            </div>

                            <div className='flex-row flex-centered reg-question-container' style={{ justifyContent: 'space-between' }}>
                                <label>On average, how many calories do you consume per day? (in kcal)</label>
                                <input type="number" required className='userIntInput' ref={el => (answersRefs.current.calories = el)}></input>
                            </div>

                            <div className='flex-row flex-centered reg-question-container' style={{ justifyContent: 'space-between' }}>
                                <label>How many liters of water do you drink daily?</label>
                                <input type="number" required className='userIntInput' ref={el => (answersRefs.current.water = el)}></input>
                            </div>
                        </div>
                    </form>

                    <div className='flex-row flex-centered' style={{ gap: '10px' }}>
                        <input className='pageBtn' type='button' value={'BACK'} onClick={() => goToPreviousPage('Patient')}></input>
                        <input className='pageBtn' type='submit' value={'NEXT'} onClick={(e) => goToNextPage(e, 3, 'Patient')}></input>
                    </div>
                </div >

                {/* PAGE 4 OF 4 */}
                < div className={`register-form flex-col ${pageFourVisibility}`}>
                    <div className='flex-col flex-centered'>
                        <h1 className='title'>REGISTER</h1>
                        <div className='subtitle'>INITIAL QUESTIONNAIRE (2 of 2)</div>
                    </div>
                    <form onSubmit={registerPatient} ref={el => (formRefs.current.patientRegister = el)}>
                        <div className='flex-col reg-questionnaire-container'>
                            <div className='flex-row flex-centered reg-question-container' style={{ justifyContent: 'space-between' }}>
                                <label>How many minutes do you exercise each day on average?</label>
                                <input type="number" required className='userIntInput' ref={el => (answersRefs.current.exercise = el)}></input>
                            </div>

                            <div className='flex-row flex-centered reg-question-container' style={{ justifyContent: 'space-between' }}>
                                <label>How many hours of sleep do you get per night on average?</label>
                                <input type="number" required className='userIntInput' ref={el => (answersRefs.current.sleep = el)}></input>
                            </div>

                            <div className='flex-row flex-centered reg-question-container' style={{ justifyContent: 'space-between' }}>
                                <label>On a scale of 1 to 10, how would you rate your energy level this week?</label>
                                <input type="number" required className='userIntInput' ref={el => (answersRefs.current.energy = el)}></input>
                            </div>

                            <div className='flex-row flex-centered reg-question-container' style={{ justifyContent: 'space-between' }}>
                                <label>On a scale of 1 to 10, how would you rate your stress level this week?</label>
                                <input type="number" required className='userIntInput' ref={el => (answersRefs.current.stress = el)}></input>
                            </div>
                        </div>
                    </form>

                    <div className='flex-row flex-centered' style={{ gap: '10px' }}>
                        <button className='pageBtn' onClick={() => goToPreviousPage('Patient')}>BACK</button>
                        <button className='registerBtn' onClick={(e) => registerPatient(e)}>REGISTER</button>
                    </div>
                </div >
            </div >

            {/* Therapist Registration Form (PAGE 1 OF 2) */}
            <div className={therapistFormVisibility}>
                <div className={`register-form flex-col ${therapistPageOneVisibility}`}>
                    <div className='register-pic-container'>
                        <div className='flex-col flex-centered'>
                            <h1 className='title'>REGISTER</h1>
                            <div className='subtitle'>Are you a...</div>
                            <div style={{ display: 'flex', gap: '20px' }}>
                                <input type='button' value={'PATIENT'} className=' pt-button selected-pt-btn' ref={el => (infoRefs.current.patientBtn = el)} onClick={() => { changeUserRegister(0) }}></input>
                                <input type='button' value={'THERAPIST'} className='pt-button ' ref={el => (infoRefs.current.therapistBtn = el)} onClick={() => { changeUserRegister(1) }}></input>
                            </div>
                        </div>
                    </div>
                    <form onSubmit={goToNextPage} ref={el => (formRefs.current.therapistPageOne = el)}>
                        <div className='flex-row' style={{ gap: '60px' }}>
                            <div className='therapist-input-container'>
                                <div className='flex-row' style={{ justifyContent: 'space-between', width: '100%' }}>
                                    <div className='flex-col reg-input-container'>
                                        <label>First Name</label>
                                        <input type="text" required ref={el => (infoTherapistRefs.current.fname = el)} className='reg-name-input reg-user-input'></input>
                                    </div>

                                    <div className='flex-col reg-input-container'>
                                        <label>Last Name</label>
                                        <input type="text" required ref={el => (infoTherapistRefs.current.lname = el)} className='reg-name-input reg-user-input'></input>
                                    </div>
                                </div>

                                <div className='flex-col reg-input-container'>
                                    <label>Email</label>
                                    <input type="text" required ref={el => (infoTherapistRefs.current.email = el)} className='reg-user-input' style={{ width: 300 }}></input>
                                </div>

                                <div className='flex-col reg-input-container'>
                                    <label>Password</label>
                                    <input type="password" required ref={el => (infoTherapistRefs.current.password = el)} className='reg-user-input' style={{ width: 300 }}></input>
                                    <img
                                        src={hidePassword}
                                        alt='reveal-password'
                                        ref={el => (passRef.current.therapistPass = el)}
                                        className='reg-password-toggle-btn'
                                        onClick={() => togglePasswordVisibility('Therapist')}
                                    />
                                </div>

                                <div className='flex-centered'>
                                    <input type='checkbox' required name='checkboxInput' ref={el => (infoRefs.current.tosAgreement = el)}></input>
                                    <label htmlFor='checkboxInput'>
                                        I agree to the Terms of Service.
                                    </label>
                                </div>
                            </div>
                            <div className='flex-col'>
                                <div className='flex-col reg-input-container'>
                                    <label>Gender</label>
                                    <div className='flex-row therapistgenders' style={{ gap: '5px' }}>
                                        <Button
                                            variant="outlined"
                                            className='flex-col'
                                            style={{ backgroundColor: 'rgb(52, 196, 169)', color: 'white', borderColor: 'white', border: '2px solid', width: '50px' }}
                                            ref={el => (genderRefs.current.therapistMaleBtn = el)}
                                            onClick={() => selectGender('Male', 'therapist')}
                                        >
                                            <ManIcon sx={{ fontSize: 40 }}></ManIcon>
                                            <label style={{ fontSize: 13 }}>Male</label>
                                        </Button>
                                        <Button
                                            variant="outlined"
                                            className='flex-col'
                                            style={{ backgroundColor: 'rgb(52, 196, 169)', color: 'white', borderColor: 'white', border: '2px solid', width: '50px' }}
                                            ref={el => (genderRefs.current.therapistFemaleBtn = el)}
                                            onClick={() => selectGender('Female', 'therapist')}
                                        >
                                            <WomanIcon sx={{ fontSize: 40 }}></WomanIcon>
                                            <label style={{ fontSize: 13 }}>Female</label>
                                        </Button>
                                        <Button
                                            variant="outlined"
                                            className='flex-col'
                                            style={{ backgroundColor: 'rgb(52, 196, 169)', color: 'white', borderColor: 'white', border: '2px solid', width: '50px' }}
                                            ref={el => (genderRefs.current.therapistOtherBtn = el)}
                                            onClick={() => selectGender('Other', 'therapist')}
                                        >
                                            <WcIcon sx={{ fontSize: 40 }}></WcIcon>
                                            <label style={{ fontSize: 13 }}>Other</label>
                                        </Button>
                                    </div>
                                </div>
                                <div className='profile-pic-container'>
                                    <div className="img-circle-mask" style={{ width: '125px', height: '125px' }}>
                                        <img src={therapistProfilePicURL} alt='PROFILE PIC' className="profile-pic" />
                                    </div>
                                    {/* <div>Upload Profile Picture</div>
                                <input type="file" style={{ width: "180px" }} onChange={(e) => handleImageFileChange(e, 'Patient')} /> */}
                                    <Button
                                        component="label"
                                        role={undefined}
                                        variant="contained"
                                        tabIndex={-1}
                                        size="small"
                                    >
                                        Upload Picture
                                        <VisuallyHiddenInput
                                            type="file"
                                            onChange={(e) => handleImageFileChange(e, 'Therapist')}
                                            multiple
                                        />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </form>
                    <div className='flex-row flex-centered'>
                        <input className='pageBtn therapist' type='submit' value={'NEXT'} onClick={(e) => goToNextPage(e, 1, 'Therapist')}></input>
                    </div>
                </div>

                < div className={`register-form flex-col flex-centered ${therapistPageTwoVisibility} therapistinfo`} >
                    <div className='register-pic-container'>
                        <div className='flex-col' style={{ alignItems: 'center' }}>
                            <h1 className='title'>REGISTER</h1>
                            <div className='subtitle'>THERAPIST INFORMATION</div>
                        </div>
                    </div>
                    <form onSubmit={registerTherapist} ref={el => (formRefs.current.therapistRegister = el)}>
                        <div className='flex-col'>
                            <div className='flex-col flex-centered' style={{ gap: '20px' }}>
                                <div className='flex-col reg-input-container'>
                                    <label>License Number</label>
                                    <input
                                        type="text"
                                        required
                                        ref={el => (infoTherapistRefs.current.license = el)}
                                        className='reg-user-input'
                                        value={licenseValue}
                                        onChange={(e) => handleNumberFieldInput(e)}
                                    />
                                </div>
                                <div className='flex-col' style={{ gap: '5px' }}>
                                    <label style={{ fontSize: '14pt' }}>Specializations ( Choose all that apply )</label>
                                    <div className='grid-specs-container' ref={el => (infoTherapistRefs.current.gridContainer = el)}>
                                        <input type='button' value={'Relationship'} className='grid-spec' onClick={(e) => selectedSpecialization(e)}></input>
                                        <input type='button' value={'Depression'} className='grid-spec' onClick={(e) => selectedSpecialization(e)}></input>
                                        <input type='button' value={'Addiction'} className='grid-spec' onClick={(e) => selectedSpecialization(e)}></input>
                                        <input type='button' value={'Anxiety'} className='grid-spec' onClick={(e) => selectedSpecialization(e)}></input>
                                        <input type='button' value={'PTSD'} className='grid-spec' onClick={(e) => selectedSpecialization(e)}></input>
                                        <input type='button' value={'Family Therapy'} className='grid-spec' onClick={(e) => selectedSpecialization(e)}></input>
                                        <input type='button' value={'Anger Mgmt.'} className='grid-spec' onClick={(e) => selectedSpecialization(e)}></input>
                                        <input type='button' value={'Confidence'} className='grid-spec' onClick={(e) => selectedSpecialization(e)}></input>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </form>
                    <div className='flex-row flex-centered' style={{ gap: '10px' }}>
                        <input className='pageBtn' type='button' value={'BACK'} onClick={() => goToPreviousPage('Therapist')}></input>
                        <button className='registerBtn' onClick={(e) => registerTherapist(e)}>REGISTER</button>
                    </div>

                    {/* <div className='flex-col flex-centered'>
                        <button className='registerBtn' onClick={(e) => registerTherapist(e)}>REGISTER</button>
                    </div> */}
                </div>
            </div >
        </>
    );
}

export default Register;