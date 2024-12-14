import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import io from 'socket.io-client';
import { DashboardCard } from '../components/DashboardCards.js';
import Pagination from '../components/Pagination.js';
import { ToastContainer, toast } from 'react-toastify';
import AOS from 'aos';
import 'aos/dist/aos.css';
import 'react-toastify/dist/ReactToastify.css';
import './styles/PatientDashboard.css';
import '../components/Pagination.css';

function PatientDashboard() {
    const [callCount, setCallCount] = useState(0);
    const [journals, setJournals] = useState([]);
    const [feedback, setFeedback] = useState([]);
    const [dailySurveys, setDailySurveys] = useState([]);
    const [incompleteTherapistSurveys, setIncompleteTherapistSurveys] = useState([]);
    const [completeTherapistSurveys, setCompleteTherapistSurveys] = useState([]);
    const [invoices, setInvoices] = useState([]);

    const [currentPage, setCurrentPage] = useState(1);
    const PageSize = 4;

    //  ---------------------- USED FOR POP UP DAILY SURVEYS ----------------------
    const [clickedDailySurveys, setClickedDailySurveys] = useState(null);
    const [dailySurveyAnswers, setDailySurveyAnswers] = useState({});
    const { paginatedDailySurvey, tableLength } = useMemo(() => {
        if (dailySurveys.length === 0) {
            return { paginatedDailySurvey: [], tableLength: 0 }; // Return default values if it's null or undefined
        }

        const firstPageIndex = (currentPage - 1) * PageSize;
        const lastPageIndex = firstPageIndex + PageSize;
        // let newDailySurveys = dailySurveys.slice();

        const questions = ['weight', 'height', 'calories', 'water', 'exercise', 'sleep', 'energy', 'stress'];
        const transformDailySurveysToQuestions = (dailySurveys) => {
            return dailySurveys.slice().reverse().map(survey => {
                return questions.map((question, index) => ({
                    [`question${index + 1}`]: survey[question]  // Dynamically assigning the question number (question1, question2, etc.)
                }));
            });
        };

        const transformedSurveys = transformDailySurveysToQuestions(dailySurveys);
        // console.log("Every survey: ", transformedSurveys);
        // console.log(dailySurveys.slice());
        // console.log(newDailySurveys.slice(firstPageIndex, lastPageIndex));
        let index;
        if (clickedDailySurveys !== null) {
            index = parseInt(clickedDailySurveys);
            // console.log("Content on Current page: ", transformedSurveys[index].slice(firstPageIndex, lastPageIndex));
        }
        else {
            return false;
        }

        return {
            paginatedDailySurvey: transformedSurveys[index].slice(firstPageIndex, lastPageIndex),
            tableLength: transformedSurveys[index].length,
        };
    }, [currentPage, clickedDailySurveys, dailySurveys]);
    //  ---------------------------------------------------------------------

    //  ---------------------- USED FOR POP UP INCOMPLETE THERAPIST SURVEYS ----------------------
    const [clickedTherapistSurveys, setClickedTherapistSurveys] = useState(null);
    const [therapistSurveyQuestions, setTherapistSurveyQuestions] = useState([]);
    const [therapistSurveyAnswers, setTherapistSurveyAnswers] = useState([]);
    const { paginatedTherapistSurvey, tableLength2 } = useMemo(() => {
        // console.log(clickedTherapistSurveys);
        if (incompleteTherapistSurveys.length === 0) {
            return { paginatedTherapistSurvey: [], tableLength2: 0 }; // Return default values if it's null or undefined
        }

        const firstPageIndex = (currentPage - 1) * PageSize;
        const lastPageIndex = firstPageIndex + PageSize;
        const transformSurveysToQuestions = (incompleteTherapistSurveys) => {
            // const survey = incompleteTherapistSurveys['survey'];
            return incompleteTherapistSurveys.map(survey => {
                const questions = JSON.parse(survey.survey);
                return questions.map((question, index) => ({
                    [`question${index + 1}`]: question.question  // Dynamically assigning the question number (question1, question2, etc.)
                }));
            });
        };

        const transformedSurveys = transformSurveysToQuestions(incompleteTherapistSurveys);
        let index;
        if (clickedTherapistSurveys) {
            index = parseInt(clickedTherapistSurveys) - 1;
        }
        else {
            return false;
        }
        return {
            paginatedTherapistSurvey: transformedSurveys[index].slice(firstPageIndex, lastPageIndex),
            tableLength2: transformedSurveys[index].length,
        };
    }, [currentPage, clickedTherapistSurveys, incompleteTherapistSurveys]);
    //  ---------------------------------------------------------------------

    //  ---------------------- USED FOR POP UP COMPLETE THERAPIST SURVEYS ----------------------
    const [clickedCompTherapistSurveys, setClickedCompTherapistSurveys] = useState(null);
    const { paginatedCompletedTherapistSurvey, tableLength3 } = useMemo(() => {
        if (completeTherapistSurveys.length === 0) {
            return { paginatedCompletedTherapistSurvey: [], tableLength3: 0 }; // Return default values if it's null or undefined
        }

        const firstPageIndex = (currentPage - 1) * PageSize;
        const lastPageIndex = firstPageIndex + PageSize;
        const transformSurveysToQuestions = (completeTherapistSurveys) => {
            // const survey = incompleteTherapistSurveys['survey'];
            //console.log(completeTherapistSurveys);
            return completeTherapistSurveys.map(survey => {
                const questions = JSON.parse(survey.questions);
                const answers = JSON.parse(survey.answers);
                //console.log(completeTherapistSurveys);
                return questions.map((question, index) => ({
                    [`question${index + 1}`]: {
                        question: question.question,
                        answer: answers[index][`q${index + 1}`]
                    }
                }));
            });
        };

        const transformedSurveys = transformSurveysToQuestions(completeTherapistSurveys);
        // console.log(transformedSurveys);
        let index;
        if (clickedCompTherapistSurveys) {
            index = parseInt(clickedCompTherapistSurveys) - 1;
            //console.log("Inside transform complete survey, clickedCompTherap... = ", index);
        }
        else {
            return false;
        }
        return {
            paginatedCompletedTherapistSurvey: transformedSurveys[index].slice(firstPageIndex, lastPageIndex),
            tableLength3: transformedSurveys[index].length,
        };
    }, [currentPage, clickedCompTherapistSurveys, completeTherapistSurveys]);
    //  ---------------------------------------------------------------------



    const navigate = useNavigate();

    const dailySurveyRefs = useRef({
        weight: null,
        height: null,
        calories: null,
        water: null,
        exercise: null,
        sleep: null,
        energy: null,
        stress: null
    });

    useEffect(() => {
        AOS.init({ duration: 1500 });
    }, [])

    useEffect(() => {
        const socket = io('http://localhost:5000');

        const patientID = localStorage.getItem("userID");

        // fetch('http://localhost:5000/patientDashboardData', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({ patientId }), // Send patientId in the body
        // })
        //     .then(res => res.json())
        //     .then(data => {
        //         //console.log(data[0]);
        //         //console.log(data[1]);
        //         //console.log(data[2]);
        //         //console.log(data[3]);
        //         //console.log(data[4]);
        //         //console.log(data[5]);
        //         if (data[0] !== "Nothing") {
        //             setJournals(data[0]);
        //         }
        //         else {
        //             setJournals([]);
        //         }
        //         if (data[1] !== "Nothing") {
        //             setFeedback(data[1]);
        //         }
        //         else {
        //             setFeedback([]);
        //         }
        //         if (data[2] !== "Nothing") {
        //             setDailySurveys(data[2]);
        //         }
        //         else {
        //             setDailySurveys([]);
        //         }
        //         if (data[3] !== "Nothing") {
        //             //console.log("IM HERE")
        //             setIncompleteTherapistSurveys(data[3]);
        //             setTherapistSurveyQuestions(JSON.parse(data[3][0].survey));
        //             //console.log(JSON.parse(data[3][0].survey));
        //         }
        //         else {
        //             setIncompleteTherapistSurveys([]);
        //             setTherapistSurveyQuestions([]);
        //         }
        //         if (data[4] !== "Nothing") {
        //             setCompleteTherapistSurveys(data[4]);
        //             // console.log(data[4]);
        //         }
        //         else {
        //             setCompleteTherapistSurveys([]);
        //         }
        //         if (data[5] !== "Nothing") {
        //             setInvoices(data[5]);
        //         }
        //         else {
        //             setInvoices([]);
        //         }
        //     })
        //     .catch(err => console.error('Error fetching data:', err));

        fetch('http://localhost:5000/getJournals', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({ patientID }), // Send patientId in the body
        })
            .then(res => res.json())
            .then(data => {
                if (data) {
                    setJournals(data);
                }
            })
            .catch(err => console.error('Error fetching data:', err));

        fetch('http://localhost:5000/getFeedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({ patientID }), // Send patientId in the body
        })
            .then(res => res.json())
            .then(data => {
                if (data) {
                    setFeedback(data);
                }
            })
            .catch(err => console.error('Error fetching data:', err));

        fetch('http://localhost:5000/getDailySurveys', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({ patientID }), // Send patientId in the body
        })
            .then(res => res.json())
            .then(data => {
                if (data) {
                    setDailySurveys(data);
                }
            })
            .catch(err => console.error('Error fetching data:', err));

        fetch('http://localhost:5000/getIncompleteTherapistSurveys', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({ patientID }), // Send patientId in the body
        })
            .then(res => res.json())
            .then(data => {
                if (data) {
                    setIncompleteTherapistSurveys(data);
                    setTherapistSurveyQuestions(data.survey);
                }
            })
            .catch(err => console.error('Error fetching data:', err));

        fetch('http://localhost:5000/getCompleteTherapistSurveys', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({ patientID }), // Send patientId in the body
        })
            .then(res => res.json())
            .then(data => {
                if (data) {
                    setCompleteTherapistSurveys(data);
                }
            })
            .catch(err => console.error('Error fetching data:', err));

        fetch('http://localhost:5000/getInvoices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({ patientID }), // Send patientId in the body
        })
            .then(res => res.json())
            .then(data => {
                if (data) {
                    setInvoices(data);
                }
            })
            .catch(err => console.error('Error fetching data:', err));

        //  Connection
        socket.on('connect', () => {
            console.log(`Connected to Patient Dashboard server (userID = ${patientID}`);
            // console.log(patientId)
            socket.emit("init-socket-comm", { "userID": patientID });
        });
        //  Disconnect
        socket.on('disconnect', () => {
            console.log(`Disconnected from Patient Dashboard server (userID = ${patientID}`);
        });

        // Update daily surveys list
        socket.on('submit-daily-survey', () => {
            console.log('DAILY SURVEY SUCCESSFULLY SUBMITTED');
        })

        // Update therapist surveys list
        socket.on('submit-therapist-survey', () => {
            //setIncompleteTherapistSurveys([]);
            console.log('THERAPIST SURVEY SUCCESSFULLY SUBMITTED');
        })

        // Listen for new feedback from therapist
        socket.on('new-feedback', (data) => {
            setFeedback((prevFeedback) => [...prevFeedback, data.feedback]);
        });

        // Listen for new surveys from therapist
        socket.on('new-survey', (newSurvey) => {
            setIncompleteTherapistSurveys((prevSurveys) => [...prevSurveys, newSurvey]);
        });

        // Cleanup on component unmount
        return () => {
            socket.emit("rem-socket-comm", { "userID": patientID });
            socket.off('new-feedback');
            socket.off('new-survey');
            socket.disconnect();
        };
    }, [callCount]);

    function systemSleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function displayPopUp(e, x, surveyID, type) {
        if (type === 'Daily') {
            setClickedDailySurveys(surveyID);
        }
        else if (type === 'Incomplete') {
            setClickedTherapistSurveys(surveyID + 1);
        }
        else if (type === 'Complete') {
            setClickedCompTherapistSurveys(surveyID + 1);
        }

        // if (dailySurveyID) {
        //     setClickedDailySurveys(dailySurveyID);
        // }
        // if (therapistSurveyID) {
        //     setClickedTherapistSurveys(therapistSurveyID);
        // }

        if (x === 2) {
            await systemSleep(100);
        }
        const divParent = x === 1 ? e.target.parentElement.children[1] : e.target.parentElement.children[0].children[1].children[0].children[1];
        divParent.className = 'visible popUp-background';
    }

    function hidePopUp(e, x) {
        setCurrentPage(1);
        if (x === 1) {
            //setCallCount(callCount + 1);
            const divParent = e.target.parentElement.parentElement.parentElement;
            // console.log(divParent);
            divParent.className = 'hidden popUp-background';
        }
        else if (x === 2) {
            //setCallCount(callCount + 1);
            const divParent = e.target.parentElement.parentElement;
            // console.log(divParent);
            divParent.className = 'hidden popUp-background';
        }
        else if (x === 3) {
            //setCallCount(callCount + 1);
            const divParent = e.target;
            // console.log(divParent);
            divParent.className = 'hidden popUp-background';
        }
        setCallCount(callCount + 1);
    }

    const clearWaitingQueue = () => {
        // Easy, right 😎
        toast.clearWaitingQueue();
    }

    function saveJournal(e) {
        const newEntry = e.target.parentElement.parentElement.children[2];
        const patientId = localStorage.getItem("userID");
        const journalId = e.target.getAttribute('journalid');
        // console.log("JOURNAL ID: ", journalId);

        fetch('http://localhost:5000/saveJournal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({ "journalEntry": newEntry.value, patientId, journalId }),
        })
            .then(res => res.json())
            .then(data => {
                clearWaitingQueue();
                toast.success('Saved Journal!');
            })
            .catch(err => console.error('Error fetching data:', err));
    }

    function createJournal(e) {
        const newJournal = { journalID: null, journalEntry: '', timeDone: new Date().toISOString() };
        // setJournals([...journals, newJournal]);
        //console.log("setJ", journals);
        if (journals) {
            setJournals([...journals, newJournal]);
        }
        else {
            setJournals([newJournal]);
        }
        displayPopUp(e, 2);
    }

    async function submitDailySurvey(e, x) {
        e.preventDefault();

        const patientId = localStorage.getItem("userID");
        const userID = localStorage.getItem("realUserID");
        const dailySurveyID = e.target.getAttribute('dailysurveyid');
        // console.log('Survey Answers:', dailySurveyAnswers);

        const weight = dailySurveyAnswers['0'] ? dailySurveyAnswers['0'] : "";
        const height = dailySurveyAnswers['1'] ? dailySurveyAnswers['1'] : "";
        const calories = dailySurveyAnswers['2'] ? dailySurveyAnswers['2'] : "";
        const water = dailySurveyAnswers['3'] ? dailySurveyAnswers['3'] : "";
        const exercise = dailySurveyAnswers['4'] ? dailySurveyAnswers['4'] : "";
        const sleep = dailySurveyAnswers['5'] ? dailySurveyAnswers['5'] : "";
        const energy = dailySurveyAnswers['6'] ? dailySurveyAnswers['6'] : "";
        const stress = dailySurveyAnswers['7'] ? dailySurveyAnswers['7'] : "";

        //console.log("DAILY SURVEY ID: ", dailySurveyID);

        fetch('http://localhost:5000/completeDailySurvey', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({
                "userID": userID, "patientID": patientId, "dailySurveyID": dailySurveyID,
                weight, height, calories, water, exercise, sleep, energy, stress
            }),
        })
            .then(res => res.json())
            .then(data => {
                clearWaitingQueue();
                toast.success('Successfully submitted survey!');
                //console.log("Successfully saved the journal");
            })
            .catch(err => console.error('Error fetching data:', err));
        await systemSleep(100)
        setCallCount(callCount + 1);
        hidePopUp(e, x);
    }

    async function submitTherapistSurvey(e, x) {
        e.preventDefault();
        const patientId = localStorage.getItem("userID");
        const userID = localStorage.getItem("realUserID");
        const surveyID = e.target.getAttribute('incomptherapistsurveyid');
        // console.log(therapistSurveyQuestions);
        // console.log(therapistSurveyAnswers);


        fetch('http://localhost:5000/completeTherapistSurvey', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "http://localhost:5000",
            },
            body: JSON.stringify({
                "userID": userID, "patientID": patientId, "surveyID": surveyID,
                "questions": therapistSurveyQuestions, "answers": therapistSurveyAnswers
            }),
        })
            .then(res => res.json())
            .then(data => {
                clearWaitingQueue();
                toast.success('Successfully submitted survey!');
                //console.log("Successfully saved the journal");
            })
            .catch(err => console.error('Error fetching data:', err));

        await systemSleep(100)
        setCallCount(callCount + 1);
        hidePopUp(e, x);
    }

    function payInvoice(invoiceID, amountDue, therapistName) {
        //console.log(e.target.getAttribute('invoiceid'));
        navigate('/payment', { state: { invoiceID: invoiceID, amountDue: amountDue, therapistName: therapistName } })
    }

    const handleInputChange = (questionIndex, value, type) => {
        if (type === 'Daily') {
            setDailySurveyAnswers(prevState => ({
                ...prevState,
                [questionIndex]: value,
            }));
        }
        else {
            if (parseInt(questionIndex) + 1 > therapistSurveyAnswers.length) {
                const answer = { [`q${questionIndex + 1}`]: value };
                let answers = therapistSurveyAnswers;
                answers.push(answer);
                setTherapistSurveyAnswers(answers);
            }
            else {
                let answers = therapistSurveyAnswers;
                answers[`q${questionIndex + 1}`] = value;
                setTherapistSurveyAnswers(answers);
            }
        }
    };

    return (
        <div data-aos="fade-up" className='patient-dashboard-container'>
            <ToastContainer
                limit={1}
                position="bottom-left"
                closeButton={false}
                hideProgressBar={true}
                pauseOnHover={false}
                autoClose={3000}
            />
            <h1
                style={{
                    textAlign: "center",
                    color: "#34c4a9",
                    fontSize: "38px",
                    fontWeight: "bold",
                    margin: 0,
                    padding: "20px 0",
                    boxSizing: "border-box",
                    textShadow: "0px 0px 2px #1a7867, 0px 0px 2px #1a7867, 0px 0px 2px #1a7867, 0px 0px 2px #1a7867, 0px 0px 2px #1a7867, 0px 0px 2px #1a7867"
                }}
            >
                Welcome to Your Patient Dashboard
            </h1>
            {/* Display patient-specific content */}

            <div className="cards-container">
                <div className='flex-col flex-centered' style={{ gap: '10px' }}>
                    <DashboardCard title="JOURNALS" extraClasses="patient-card">
                        {journals.length > 0 && journals.slice().reverse().map((row, index) => {
                            const originalIndex = journals.length - 1 - index;
                            return (
                                <div key={`journal-${originalIndex}`} style={{ width: "100%" }}>
                                    <input className='card-buttons' type='button' value={`Journal #${originalIndex + 1} - ${new Intl.DateTimeFormat('en-US').format(new Date(row.timeDone))}`} onClick={(e) => displayPopUp(e, 1)}></input>
                                    <div className='hidden popUp-background'>
                                        <div className='pd-popUp'>
                                            <h2>Journal Entry #{originalIndex + 1}</h2>
                                            <h3>Date Created: {new Intl.DateTimeFormat('en-US').format(new Date(row.timeDone))}</h3>
                                            <textarea defaultValue={row.journalEntry} placeholder='Type here...'></textarea>
                                            <div className="flex-row" style={{ gap: "10px" }}>
                                                <input className='pd-action-btn' type='button' value={'CLOSE'} onClick={(e) => hidePopUp(e, 1)}></input>
                                                <input className='pd-action-btn' type='button' journalid={row.journalID} value={'SAVE'} onClick={(e) => saveJournal(e)}></input>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </DashboardCard>
                    <input className='card-buttons' type='button' value={'CREATE NEW JOURNAL'} onClick={(e) => createJournal(e)}></input>
                </div>

                <DashboardCard title="FEEDBACK" extraClasses="patient-card">
                    {feedback.length > 0 && feedback.map((row, index) => {
                        return (
                            <div key={`feedback-${index}`} style={{ width: "100%" }}>
                                <input className='card-buttons' type='button' value={row.feedback} onClick={(e) => displayPopUp(e, 1)}></input>
                                <div className='hidden popUp-background'>
                                    <div className='pd-popUp'>
                                        <h2>Feedback #{index + 1}</h2>
                                        <div className='flex-col' style={{ gap: '10px' }}>
                                            <h3>Date Sent: {new Intl.DateTimeFormat('en-US').format(new Date(row.feedbackDate))}</h3>
                                            <h3>Sent By: {row.userName}</h3>
                                        </div>
                                        <p>{row.feedback}</p>
                                        <div>
                                            <input className='pd-action-btn' type='button' value={'CLOSE'} onClick={(e) => hidePopUp(e, 1)}></input>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </DashboardCard>

                <DashboardCard title="DAILY SURVEYS" extraClasses="patient-card">
                    {dailySurveys.length > 0 && dailySurveys.slice().reverse().map((row, index) => {
                        const dailySurveyDate = new Intl.DateTimeFormat('en-US', { timeZone: 'UTC' }).format(new Date(row.dateCreated));
                        const currentDate = Intl.DateTimeFormat('en-US', { timeZone: 'EST' }).format(new Date());
                        const isSameDate = (
                            dailySurveyDate.split('/')[0] === currentDate.split('/')[0] &&
                            dailySurveyDate.split('/')[1] === currentDate.split('/')[1] &&
                            dailySurveyDate.split('/')[2] === currentDate.split('/')[2]
                        );
                        return (
                            <div key={`daily-survey-${index}`} style={{ width: "100%" }}>
                                <input
                                    type='button'
                                    className='card-buttons'
                                    dailysurveyid={row.dailySurveyID}
                                    value={
                                        isSameDate
                                            ? (row.weight === null
                                                ? `(NEW) Daily Survey ${new Intl.DateTimeFormat('en-US', { timeZone: 'UTC' }).format(new Date(row.dateCreated))}`
                                                : `COMPLETED Daily Survey ${new Intl.DateTimeFormat('en-US', { timeZone: 'UTC' }).format(new Date(row.dateCreated))}`)
                                            : (row.weight !== null
                                                ? `COMPLETED Daily Survey ${new Intl.DateTimeFormat('en-US', { timeZone: 'UTC' }).format(new Date(row.dateCreated))}`
                                                : `(NEW) Daily Survey ${new Intl.DateTimeFormat('en-US', { timeZone: 'UTC' }).format(new Date(row.dateCreated))}`)
                                    }
                                    onClick={(e) => displayPopUp(e, 1, index, 'Daily')}
                                />
                                <form className='hidden popUp-background' dailysurveyid={row.dailySurveyID} onSubmit={(e) => submitDailySurvey(e, 3)}>
                                    <div className='pd-popUp pd-questions-container' style={{ width: "400px" }}>
                                        <h2>Daily Survey #{dailySurveys.length - index}</h2>
                                        <h3>Date: {new Intl.DateTimeFormat('en-US', { timeZone: 'UTC' }).format(new Date(row.dateCreated))}</h3>
                                        {paginatedDailySurvey && paginatedDailySurvey.length > 0 ? (
                                            paginatedDailySurvey.map((newRow, newIndex) => {
                                                const rowProperties = ['weight', 'height', 'calories', 'water', 'exercise', 'sleep', 'energy', 'stress'];
                                                const propertyToShow = rowProperties[newIndex % rowProperties.length];
                                                return (
                                                    row.weight !== null ? (
                                                        <div className='flex-col pd-question-container' key={`question-${row.dailySurveyID}-${newIndex}`} style={{ width: "100%" }}>
                                                            {
                                                                (newIndex + 1) + (4 * (currentPage - 1)) === 1 ? (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How much do you weigh?</label>
                                                                ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 2) ? (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How tall are you?</label>
                                                                ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 3) ? (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How many calories have you consumed today?</label>
                                                                ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 4) ? (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How much water have you drank today?</label>
                                                                ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 5) ? (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How much exercise have you had today?</label>
                                                                ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 6) ? (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How much sleep have you had?</label>
                                                                ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 7) ? (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: On a scale 1-10, how much energy do you have?</label>
                                                                ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 8) ? (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: On a scale 1-10, how much stressed are you?</label>
                                                                ) : (
                                                                    <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: </label>
                                                                )
                                                            }

                                                            {/* <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: </label> */}
                                                            <textarea
                                                                className='pd-textarea'
                                                                disabled
                                                                value={newRow[`question${(newIndex + 1) + (4 * (currentPage - 1))}`] ? newRow[`question${(newIndex + 1) + (4 * (currentPage - 1))}`] : ""}
                                                            >
                                                            </textarea>
                                                        </div>
                                                    ) : (
                                                        <div className='questions-container' key={`questions-${row.dailySurveyID}-${newIndex}`} style={{ width: "100%" }}>
                                                            <div className='flex-col pd-question-container' style={{ width: "100%" }}>
                                                                {
                                                                    (newIndex + 1) + (4 * (currentPage - 1)) === 1 ? (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How much do you weigh?</label>
                                                                    ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 2) ? (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How tall are you?</label>
                                                                    ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 3) ? (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How many calories have you consumed today?</label>
                                                                    ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 4) ? (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How much water have you drank today?</label>
                                                                    ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 5) ? (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How much exercise have you had today?</label>
                                                                    ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 6) ? (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: How much sleep have you had?</label>
                                                                    ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 7) ? (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: On a scale 1-10, how much energy do you have?</label>
                                                                    ) : ((newIndex + 1) + (4 * (currentPage - 1)) === 8) ? (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: On a scale 1-10, how much stressed are you?</label>
                                                                    ) : (
                                                                        <label>QUESTION #{(newIndex + 1) + (4 * (currentPage - 1))}: </label>
                                                                    )
                                                                }
                                                                <textarea
                                                                    className='pd-textarea'
                                                                    required
                                                                    placeholder='Answer here...'
                                                                    //ref={el => (dailySurveyRefs.current[`${newRow[propertyToShow]}`] = el)}
                                                                    value={dailySurveyAnswers[(newIndex) + (4 * (currentPage - 1))] || ''}
                                                                    onChange={(e) => handleInputChange((newIndex) + (4 * (currentPage - 1)), e.target.value, 'Daily')}
                                                                >
                                                                </textarea>
                                                            </div>
                                                        </div>
                                                    )
                                                );
                                            })

                                        ) : (
                                            <></>
                                        )}
                                        <div className='flex-row' style={{ gap: "10px" }}>
                                            <input className='pd-action-btn' type='button' value={'CLOSE'} onClick={(e) => hidePopUp(e, 1)}></input>
                                            <Pagination
                                                currentPage={currentPage}
                                                totalCount={tableLength}
                                                pageSize={PageSize}
                                                onPageChange={page => setCurrentPage(page)}
                                                className={'pd-action-btn'}
                                            />
                                            {row.weight === null && currentPage === 2 && (
                                                <input className='pd-action-btn' type='submit' value={'SUBMIT'} />
                                            )}
                                        </div>
                                    </div>
                                </form>
                            </div>
                        );
                    })}
                </DashboardCard>

                <DashboardCard title="INVOICES" extraClasses="patient-card">
                    {invoices.length > 0 && invoices.map((row, index) => {
                        return (
                            <input
                                className='card-buttons'
                                key={`invoice-${index}`}
                                invoiceid={row.invoiceID}
                                type='button'
                                value={`$${row.amountDue} Invoice to ${row.userName}`}
                                onClick={() => payInvoice(row.invoiceID, row.amountDue, row.userName)}
                            >
                            </input>
                        );
                    })}
                </DashboardCard>

                <DashboardCard title="THERAPIST SURVEYS" extraClasses="patient-card">
                    {incompleteTherapistSurveys.length > 0 && incompleteTherapistSurveys.map((row, index) => {
                        // Parse the 'survey' JSON string into an array of questions
                        const questions = JSON.parse(row.survey);

                        return (
                            <div key={`incompleted-survey-${index}`} style={{ width: "100%" }}>
                                <input
                                    type='button'
                                    className='card-buttons'
                                    incomptherapistsurveyid={row.surveyID}
                                    value={`(NEW) Survey ${new Intl.DateTimeFormat('en-US').format(new Date(row.dateCreated))}`}
                                    onClick={(e) => displayPopUp(e, 1, index, 'Incomplete')}
                                />
                                <form className='hidden popUp-background' incomptherapistsurveyid={row.surveyID} onSubmit={(e) => submitTherapistSurvey(e, 3)}>
                                    <div className='pd-popUp pd-questions-container' style={{ width: "400px" }}>
                                        <h2>{row.userName}'s Survey</h2>
                                        {/* <h3>Date: {new Date(row.dateCreated).toDateString()}</h3> */}
                                        {paginatedTherapistSurvey && paginatedTherapistSurvey.length > 0 ? (
                                            paginatedTherapistSurvey.map((newRow, newIndex) => {
                                                return (
                                                    <div className='questions-container' key={`therapist-questions-${row.surveyID}-${newIndex}`} style={{ width: "100%" }}>
                                                        <div className='flex-col pd-question-container' style={{ width: "100%" }}>
                                                            <label>{newRow[`question${(newIndex + 1) + (4 * (currentPage - 1))}`]}</label>
                                                            <textarea
                                                                className='pd-textarea'
                                                                required
                                                                placeholder='Answer here...'
                                                                value={therapistSurveyAnswers[`q${(newIndex) + (4 * (currentPage - 1))}`]}
                                                                onChange={(e) => handleInputChange((newIndex) + (4 * (currentPage - 1)), e.target.value, 'Therapist')}
                                                            >
                                                            </textarea>
                                                        </div>
                                                    </div>
                                                );
                                            })

                                        ) : (
                                            <></>
                                        )}
                                        <div className='flex-row' style={{ gap: "10px" }}>
                                            <input className='pd-action-btn' type='button' value={'CLOSE'} onClick={(e) => hidePopUp(e, 1)}></input>
                                            <Pagination
                                                currentPage={currentPage}
                                                totalCount={tableLength2}
                                                pageSize={PageSize}
                                                onPageChange={page => setCurrentPage(page)}
                                                className={'card-buttons'}
                                            />
                                            {currentPage === Math.ceil(tableLength2 / PageSize) && (
                                                <input className='pd-action-btn' type='submit' value={'SUBMIT'} />
                                            )}
                                        </div>
                                    </div>
                                </form>
                            </div>
                        );
                    })}
                    {completeTherapistSurveys.length > 0 && completeTherapistSurveys.map((row, index) => {
                        return (
                            <div key={`completed-survey-${index}`} style={{ width: "100%" }}>
                                <input
                                    type='button'
                                    className='card-buttons'
                                    incomptherapistsurveyid={row.completionID}
                                    value={`COMPLETED Survey (Done: ${new Intl.DateTimeFormat('en-US').format(new Date(row.dateDone))})`}
                                    onClick={(e) => displayPopUp(e, 1, index, 'Complete')}
                                />
                                <div className='hidden popUp-background' comptherapistsurveyid={row.completionID}>
                                    <div className='pd-popUp pd-questions-container' style={{ width: "400px" }}>
                                        <h2>{row.userName}'s Survey</h2>
                                        {/* <h3>Date: {new Date(row.dateCreated).toDateString()}</h3> */}
                                        {paginatedCompletedTherapistSurvey && paginatedCompletedTherapistSurvey.length > 0 ? (
                                            paginatedCompletedTherapistSurvey.map((newRow, newIndex) => {
                                                return (
                                                    <div className='questions-container' key={`therapist-questions-${row.completionID}-${newIndex}`} style={{ width: "100%" }}>
                                                        <div className='flex-col pd-question-container' style={{ width: "100%" }}>
                                                            <label>{newRow[`question${(newIndex + 1) + (4 * (currentPage - 1))}`][`question`]}</label>
                                                            <textarea
                                                                className='pd-textarea'
                                                                disabled
                                                                value={newRow[`question${(newIndex + 1) + (4 * (currentPage - 1))}`][`answer`]}
                                                            >
                                                            </textarea>
                                                        </div>
                                                    </div>
                                                );
                                            })

                                        ) : (
                                            <></>
                                        )}
                                        <div className='flex-row' style={{ gap: "10px" }}>
                                            <input className='pd-action-btn' type='button' value={'CLOSE'} onClick={(e) => hidePopUp(e, 1)}></input>
                                            <Pagination
                                                currentPage={currentPage}
                                                totalCount={tableLength3}
                                                pageSize={PageSize}
                                                onPageChange={page => setCurrentPage(page)}
                                                className={'card-buttons'}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                    {/* {completeTherapistSurveys && completeTherapistSurveys.map((row, index) => {
                        const questions = JSON.parse(row.questions);
                        const answers = JSON.parse(row.answers);

                        return (
                            <div key={`completed-survey-${index}`}>
                                <input className='card-buttons' type='button' value={`COMPLETED Survey ${new Intl.DateTimeFormat('en-US').format(new Date(row.dateDone))}`} onClick={(e) => displayPopUp(e, 1)}></input>
                                <div className='hidden popUp-background'>
                                    <div className='popUp'>
                                        <h2>{row.userName}'s Survey</h2>
                                        {questions && questions.map((question, questionIndex) => (
                                            <div key={questionIndex} className='flex-col'>
                                                <label>{question.question}</label>
                                                <input type='text' disabled value={answers[0][`q${questionIndex + 1}`] || ''}></input>
                                            </div>
                                        ))}
                                        <div>
                                            <input className='card-buttons' type='button' value={'CLOSE'} onClick={(e) => hidePopUp(e, 1)}></input>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })} */}
                </DashboardCard>
            </div >
        </div >
    );
}

export default PatientDashboard;