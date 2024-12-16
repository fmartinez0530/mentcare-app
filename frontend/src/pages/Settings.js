import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/Settings.css'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AOS from 'aos';
import 'aos/dist/aos.css';

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


// const socket = io('https://mentcare-backend.onrender.com', {withCredentials:true, transports:['websocket', 'polling']});

function SettingsPage() {
    const [userName, setUserName] = useState();
    const [userNameUpd, setUserNameUpd] = useState("");

    const [email, setEmail] = useState();
    const [emailUpd, setEmailUpd] = useState("");

    const [pfp, setPfp] = useState();
    const [pfpUpd, setPfpUpd] = useState();
    const [pfpFile, setPfpFile] = useState();

    const [insComp, setInsComp] = useState();
    const [insID, setInsID] = useState();
    const [insTier, setInsTier] = useState();

    const [insCompUpd, setInsCompUpd] = useState("");
    const [insIDUpd, setInsIDUpd] = useState("");
    const [insTierUpd, setInsTierUpd] = useState("");

    const [patientPrivacy, setPatientPrivacy] = useState();
    const [accountActive, setAccountActive] = useState(null);
    const [accActionClass, setAccActionClass] = useState("settings-acc-action-btn");
    const [words, setWords] = useState();
    const accDeetsPopupRef = useRef(null);
    const insInfoPopupRef = useRef(null);
    const patientRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetch("https://mentcare-backend.onrender.com/updateSocketsNavbar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ 'realUserID': localStorage.getItem('realUserID') }),
        })
            .then((res) => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then((data) => {
                console.log(data.message)
            })
            .catch((err) => console.error("Error fetching data:", err));
    }, [])

    useEffect(() => {
        const realUserID = localStorage.getItem("realUserID");
        const userID = localStorage.getItem("userID");
        const userType = localStorage.getItem("userType");
        if (userType === "Patient") {
            patientRef.current.className = "";
        }

        fetch('https://mentcare-backend.onrender.com/settingsAccountData', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ realUserID: realUserID, userID: userID, userType: userType }),
        })
            .then(res => res.json())
            .then(data => {
                setUserName(data.userName);
                setUserNameUpd(data.userName);

                setEmail(data.email);
                setEmailUpd(data.email);

                setPatientPrivacy(data.patientPrivacy ? "True" : "False");

                setInsComp(data.insComp);
                setInsCompUpd(data.insComp);

                setInsID(data.insID);
                setInsIDUpd(data.insID);

                setInsTier(data.insTier);
                setInsTierUpd(data.insTier);

                setAccountActive(data.isActive);
            })
            .catch(err => console.error('Error fetching data:', err));

        let imageExists = false;
        fetch("https://mentcare-backend.onrender.com/retriveProfilePic", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",  // Ensure the request is sent as JSON
            },
            body: JSON.stringify({ realUserID }),
        })
            .then((res) => {
                if (res.ok) {
                    imageExists = true;
                }
                return res.json();
            })
            .then((data) => {
                if (imageExists) {
                    setPfp(`/assets/profile-pics/${data.profileImg}`);
                    setPfpUpd(`/assets/profile-pics/${data.profileImg}`);
                    imageExists = false;
                }
                else {
                    setPfp('/assets/images/default-profile-pic.jpg');
                    setPfpUpd('/assets/images/default-profile-pic.jpg');
                }
            })
            .catch((error) => {
                console.error("Error fetching image:", error);
            });
    }, []);

    useEffect(() => {
        const userType = localStorage.getItem("userType");

        if (userType === "Therapist") {
            setWords(accountActive ? "Deactivate" : "Activate");
            if (accountActive !== null) {
                setAccActionClass(parseInt(accountActive) ? "settings-acc-action-btn settings-red-btn" : "settings-acc-action-btn settings-green-btn")
            }
        }
        else if (userType === "Patient") {
            setWords("Delete");
            setAccActionClass("settings-acc-action-btn settings-red-btn")
        } else {
            setWords("Admin");
        }
    }, [accountActive]);

    useEffect(() => {
        AOS.init({ duration: 1500 });
    }, [])

    const editAccDetails = () => {
        accDeetsPopupRef.current.className = 'settings-popUp-background';
    }

    const cancelEditAccDetails = () => {
        accDeetsPopupRef.current.className = 'hidden settings-popUp-background';
        setPfpUpd(pfp);
        setUserNameUpd(userName);
        setEmailUpd(email);
    }

    const saveAccDetails = async (e) => {
        e.preventDefault();

        const realUserID = localStorage.getItem("realUserID");
        const userId = localStorage.getItem("userID");
        const userType = localStorage.getItem("userType");

        const formData = new FormData();
        formData.append('realUserID', realUserID);
        formData.append('userID', userId);
        formData.append('userType', userType);
        formData.append('userNameUpd', userNameUpd === "" ? userName : userNameUpd);
        formData.append('emailUpd', emailUpd === "" ? email : emailUpd);
        if (pfpFile) {
            formData.append('pfpFile', pfpFile, pfpFile.filename);
        }

        const response = await fetch('https://mentcare-backend.onrender.com/settingsUpdAccDetails', {
            method: 'POST',
            body: formData,
        });
        if (response.ok) {
            const data = await response.json()

            clearWaitingQueue();
            toast.success("Saved account details!");

            setUserName(data.userName);
            setUserNameUpd(data.userName);
            setEmail(data.email);
            setEmailUpd(data.email);
            // setPfp(`/assets/profile-pics/${data.profileImg}`);
            accDeetsPopupRef.current.className = 'hidden settings-popUp-background';
        } else {
            clearWaitingQueue();
            toast.error("Updating details failed. Try Again!");
        }
    }

    const editInsDetails = () => {
        insInfoPopupRef.current.className = 'settings-popUp-background';
    }

    const cancelEditInsDetails = () => {
        insInfoPopupRef.current.className = 'hidden settings-popUp-background';
        setInsCompUpd(insComp);
        setInsIDUpd(insID);
        setInsTierUpd(insTier);
    }

    const saveInsDetails = async (event) => {
        event.preventDefault();

        const userId = localStorage.getItem("userID");

        const response = await fetch('https://mentcare-backend.onrender.com/settingsUpdInsDetails', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userId: userId, insCompUpd: insCompUpd === "" ? insComp : insCompUpd,
                insIDUpd: insIDUpd === "" ? insID : insIDUpd, insTierUpd: insTierUpd === "" ? insTier : insTierUpd
            }),
        });
        if (response.ok) {
            const data = await response.json()
            clearWaitingQueue();
            toast.success('Saved insurance details!')

            setInsComp(data.insComp);
            setInsID(data.insID);
            setInsTier(data.insTier);
            insInfoPopupRef.current.className = 'hidden settings-popUp-background';
        } else {
            clearWaitingQueue();
            toast.error("Updating details failed. Try Again!");
        }
    }

    const privacyHandler = (event) => {
        setPatientPrivacy(event.target.value);
        const userId = localStorage.getItem("userID");

        fetch('https://mentcare-backend.onrender.com/settingsUpdPrivacy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId: userId, patientPrivacy: event.target.value }),
        })
            .then(res => res.json())
            .then(data => {
            })
            .catch(err => console.error('Error fetching data:', err));
    }

    const accountChangeHandler = async (words) => {
        const userId = localStorage.getItem("userID");
        const userType = localStorage.getItem("userType");

        const response = await fetch('https://mentcare-backend.onrender.com/settingsRemoveAccount', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId: userId, userType: userType }),
        });
        if (response.ok) {
            const data = await response.json()
            if (userType === 'Therapist' && words === 'Deactivate') {
                localStorage.setItem("isActive", data.isActive);
                navigate('/deactivated');
                return;
            }
            else if (userType === 'Therapist' && words === 'Activate') {
                localStorage.setItem("isActive", data.isActive);
                setAccActionClass("settings-acc-action-btn settings-red-btn");
                setWords("DEACTIVATE");
                navigate("/settings");
                return;
            }
            localStorage.setItem("userID", 0);
            navigate('/')
        } else {
            const data = await response.json()
            if (data.deletion === 'Unpaid invoices') {
                clearWaitingQueue();
                toast.error("You are unable to delete your account due to unpaid invoices.");
            }
            else {
                clearWaitingQueue();
                toast.error("There was a problem deleting your account. Try again later!");
            }
        }
    }

    function resetInput(e, field) {
        switch (field) {
            case 'name':
                setUserNameUpd(userName);
                e.target.parentElement.parentElement.children[0].value = userName;
                break;
            case 'email':
                setEmailUpd(email);
                e.target.parentElement.parentElement.children[0].value = email;
                break;
            case 'insComp':
                setInsCompUpd(insComp);
                e.target.parentElement.parentElement.children[0].value = insComp;
                break;
            case 'insID':
                setInsIDUpd(insID);
                e.target.parentElement.parentElement.children[0].value = insID;
                break;
            case 'insTier':
                setInsTierUpd(insTier);
                e.target.parentElement.parentElement.children[0].value = insTier;
                break
            default:
                console.log("Something went wrong when resetting insurance details!)");
                break;
        }
    }

    function handleImageFileChange(e) {
        e.preventDefault();
        const file = e.target.files[0]; // Get the first file
        if (file) {
            const fileURL = URL.createObjectURL(file);
            setPfpUpd(fileURL);
            setPfpFile(file);
            // setPfp(fileURL);
        }
    }

    const clearWaitingQueue = () => {
        toast.clearWaitingQueue();
    }

    return (
        <div data-aos="fade-up" className='flex-col flex-centered' style={{ gap: '40px', justifyContent: 'space-around', marginBottom: '40px' }}>
            <ToastContainer
                limit={1}
                position="bottom-left"
                closeButton={false}
                hideProgressBar={true}
                pauseOnHover={false}
                autoClose={3000}
            />
            <div className='settings-main-container'>
                <div className="flex-col flex-centered">
                    <div className='flex-col flex-centered'>
                        <h1>Account Details</h1>
                        <div className='flex-row flex-centered' style={{ gap: "20px" }}>
                            {pfp ? (
                                <div className="centered settings-img-circle-mask">
                                    <img src={pfp} alt="Profile" className="settings-profile-pic" />
                                </div>
                            ) : (
                                <div className="centered settings-img-circle-mask">
                                    <img src={'/assets/images/default-profile-pic.jpg'} alt="Profile" className="settings-profile-pic" />
                                </div>
                            )}
                            <div className='flex-row' style={{ textAlign: "right", gap: "10px" }}>
                                <div className='flex-col'>
                                    <p>Name:</p>
                                    <p>Email:</p>
                                </div>
                                <div className='flex-col' style={{ textAlign: "left" }}>
                                    <p>{userName}</p>
                                    <p>{email}</p>
                                </div>
                            </div>
                        </div>

                        <button className='settings-btn' type="button" onClick={() => editAccDetails()}>Edit Details</button>
                    </div>
                    <div ref={patientRef} className="hidden settings-popUp-background" style={{ width: '100%' }}>

                        <hr style={{ "width": "100%", "height": "2px", "border": "none", "marginTop": "25px", "marginBottom": "-10px", "backgroundColor": "black" }} />
                        <h1>Insurance Details</h1>
                        <div className='flex-row flex-centered' style={{ gap: "10px" }}>
                            <div className='flex-col flex-centered' style={{ textAlign: "right" }}>
                                <p>Insurance Company:</p>
                                <p>Insurance ID:</p>
                                <p>Insurance Tier:</p>
                            </div>
                            <div className='flex-col' style={{ textAlign: "left" }}>
                                <p>{insComp}</p>
                                <p>{insID}</p>
                                <p>{insTier}</p>
                            </div>
                        </div>
                        <button className='settings-btn' type="button" onClick={() => editInsDetails()}>Edit Details</button>
                    </div>
                    <hr style={{ "width": "100%", "height": "2px", "border": "none", "marginTop": "25px", "marginBottom": "-10px", "backgroundColor": "black" }} />
                    {/* <h1>Appearance</h1>
                    <label htmlFor="theme">Choose a theme:</label><br />
                    <select name="theme" id="theme">
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                    </select>
                    <br /><br /> */}
                    <div className={localStorage.getItem('userType') === 'Patient' ? '' : 'hidden'} style={{ width: '100%' }}>
                        <h1>Privacy Details</h1>
                        <label htmlFor="theme">Allow therapists to see old records?</label><br />
                        <select name="theme" id="theme" value={patientPrivacy === "True" ? "True" : "False"} onChange={(event) => privacyHandler(event)}>
                            <option value="False">No</option>
                            <option value="True">Yes</option>
                        </select>
                        <hr style={{ "width": "100%", "height": "2px", "border": "none", "marginTop": "25px", "marginBottom": "-10px", "backgroundColor": "black" }} />
                    </div>

                    <button className={accActionClass} type="button" onClick={() => accountChangeHandler(words)}>{words} Account</button>
                </div>
            </div >
            <div ref={accDeetsPopupRef} className="hidden settings-popUp-background">
                <div className="settings-popUp flex-row flex-centered">
                    <h1>EDITING DETAILS</h1>
                    <form onSubmit={(e) => saveAccDetails(e)} className='flex-col settings-upd-details-container' style={{ gap: "40px" }}>
                        <div className='flex-row' style={{ gap: "40px" }}>
                            <div className='settings-profile-pic-container flex-col flex-centered'>
                                <div className="settings-img-circle-mask">
                                    <img src={pfpUpd} alt='PROFILE PIC' height={100} width={100} className="settings-profile-pic" />
                                </div>
                                {/* <div>Upload Profile Picture</div>
                                <input type="file" style={{ width: "180px" }} onChange={(e) => handleImageFileChange(e)} /> */}
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
                                        onChange={(e) => handleImageFileChange(e)}
                                    />
                                </Button>
                            </div>
                            <div className='flex-col flex-centered' style={{ gap: "20px" }}>
                                <div className='flex-col' style={{ gap: "5px" }}>
                                    <label>New Name:</label>
                                    <div className='flex-row flex-centered' style={{ height: "30px", gap: "10px" }}>
                                        <input className='settings-text-input' type="text" id="nameBox" name="nameBox" placeholder="Name" maxLength="50" value={userNameUpd} onChange={(event) => event.target.value !== '' ? setUserNameUpd(event.target.value) : setUserNameUpd('')} />
                                        <div className='settings-undo-btn-container'>
                                            <img src={'/assets/images/undo-btn.png'} alt='undo-btn' onClick={(e) => resetInput(e, 'name')} style={{ height: "100%", width: "auto" }} ></img>
                                        </div>
                                    </div>
                                </div>
                                <div className='flex-col' style={{ gap: "5px" }}>
                                    <label>New Email:</label>
                                    <div className='flex-row' style={{ height: "30px", gap: "10px" }}>
                                        <input className='settings-text-input' type="text" id="emailBox" name="emailBox" placeholder="Email" maxLength="320" value={emailUpd} onChange={(event) => event.target.value !== '' ? setEmailUpd(event.target.value) : setEmailUpd('')} />
                                        <div className='settings-undo-btn-container'>
                                            <img src={'/assets/images/undo-btn.png'} alt='undo-btn' onClick={(e) => resetInput(e, 'email')} style={{ height: "100%", width: "auto" }} ></img>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {/* <input type="text" id="pfpBox" name="pfpBox" placeholder="PFP URL" defaultValue={pfp} onChange={(event) => event.target.value !== '' ? setPfpUpd(event.target.value) : setPfpUpd('')} /> */}
                        <div className="flex-row flex-centered" style={{ gap: "10px" }}>
                            <button className='settings-btn' type="submit">Save Details</button>
                            <button className='settings-btn' type="button" onClick={() => cancelEditAccDetails()}>Cancel Details</button>
                        </div>
                    </form>
                </div>
            </div>

            <div ref={insInfoPopupRef} className="hidden settings-popUp-background">
                <div className="settings-popUp flex-row flex-centered">
                    <h1>EDITING DETAILS</h1>
                    <form onSubmit={(event) => saveInsDetails(event)} className='flex-col settings-upd-details-container' style={{ gap: "40px" }}>
                        <div className='flex-col' style={{ gap: "20px" }}>
                            <div className='flex-col' style={{ gap: "5px" }}>
                                <label>New Insurance Company:</label>
                                <div className='flex-row' style={{ height: "30px", gap: "10px" }}>
                                    <input className='settings-text-input' type="text" id="insCompBox" name="insCompBox" placeholder="Insurance Company" value={insCompUpd} onChange={(event) => event.target.value !== '' ? setInsCompUpd(event.target.value) : setInsCompUpd('')} /><br />
                                    <div className='settings-undo-btn-container'>
                                        <img src={'/assets/images/undo-btn.png'} alt='undo-btn' onClick={(e) => resetInput(e, 'insComp')} style={{ height: "100%", width: "auto" }} ></img>
                                    </div>
                                </div>
                            </div>
                            <div className='flex-col' style={{ gap: "5px" }}>
                                <label>New Insurance ID:</label>
                                <div className='flex-row' style={{ height: "30px", gap: "10px" }}>
                                    <input className='settings-text-input' type="text" id="insIDBox" name="insIDBox" placeholder="Insurance ID" value={insIDUpd} onChange={(event) => event.target.value !== '' ? setInsIDUpd(event.target.value) : setInsIDUpd('')} /><br />
                                    <div className='settings-undo-btn-container'>
                                        <img src={'/assets/images/undo-btn.png'} alt='undo-btn' onClick={(e) => resetInput(e, 'insID')} style={{ height: "100%", width: "auto" }} ></img>
                                    </div>
                                </div>
                            </div>
                            <div className='flex-col' style={{ gap: "5px" }}>
                                <label>New Insurance Tier:</label>
                                <div className='flex-row' style={{ height: "30px", gap: "10px" }}>
                                    <input className='settings-text-input' type="text" id="insTierBox" name="insTierBox" placeholder="Insurance Tier" value={insTierUpd} onChange={(event) => event.target.value !== '' ? setInsTierUpd(event.target.value) : setInsTierUpd('')} /><br />
                                    <div className='settings-undo-btn-container'>
                                        <img src={'/assets/images/undo-btn.png'} alt='undo-btn' onClick={(e) => resetInput(e, 'insTier')} style={{ height: "100%", width: "auto" }} ></img>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="flex-row flex-centered" style={{ gap: "10px" }}>
                            <input className='settings-btn' type="button" onClick={(e) => saveInsDetails(e)} value="Save Details" />
                            <button className='settings-btn' type="button" onClick={() => cancelEditInsDetails()}>Cancel Details</button>
                        </div>
                    </form>
                </div>
            </div >
        </div>
    );
}

export default SettingsPage;