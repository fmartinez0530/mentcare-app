import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import './styles/TherapistProfile.css';
import '../presets.css';
import { Rating, Slider, Pagination, FormControl, FormHelperText } from '@mui/material';
import { ToastContainer, toast } from 'react-toastify';
import AOS from 'aos';
import 'aos/dist/aos.css';

function TherapistProfile() {
    const { userId } = useParams();
    const [therapistName, setTherapistName] = useState("");
    const [therapistPfp, setTherapistPfp] = useState("/assets/images/default-profile-pic.jpg");

    const [specializations, setSpecializations] = useState("");
    const [education, setEducation] = useState("");
    const [availability, setAvailability] = useState("");
    const [aboutMe, setAboutMe] = useState("");
    const [pricingTxt, setPricingTxt] = useState("");
    const [pricingNum, setPricingNum] = useState("");

    const [specializationsArr, setSpecializationsArr] = useState([]);
    const [educationUpd, setEducationUpd] = useState("");
    const [availabilityUpd, setAvailabilityUpd] = useState("");
    const [aboutMeUpd, setAboutMeUpd] = useState("");
    const [pricingUpdTxt, setPricingUpdTxt] = useState("");
    const [pricingUpdNum, setPricingUpdNum] = useState("");

    const [reviews, setReviews] = useState();
    const [reviewSummary, setReviewSummary] = useState({ "avgStars": 0, "individualReviews": [{ "fives": 5, "fours": 4, "threes": 3, "twos": 2, "ones": 1 }] });
    const [totalReviews, setTotalReviews] = useState(0);
    const [page, setPage] = useState(1);
    const [editing, setEditing] = useState(0);

    const [currentTherapist, setCurrentTherapist] = useState(0);
    const [ableToSwap, setAbleToSwap] = useState(0);
    const [accepting, setAccepting] = useState(0);

    const [userReviewText, setUserReviewText] = useState();
    const [userReviewStars, setUserReviewStars] = useState(0);
    const [ratingError, setRatingError] = useState(false);
    const popupRef = useRef(null);


    useEffect(() => {
        // editable info
        fetch(`https://mentcare-backend.onrender.com/therapistProfileInfo`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urlUserId: userId }),
        })
            .then(res => res.json())
            .then(data => {
                if (data.Therapist[6] !== null) {
                    setTherapistPfp(`/assets/profile-pics/${data.Therapist[6]}`)
                }
                else {
                    setTherapistPfp('/assets/images/default-profile-pic.jpg')
                }
                setTherapistName(data.Therapist[0]);
                setSpecializations(data.Therapist[5]);
                setSpecializationsArr(data.Therapist[5].split(','));
                setEducation(data.Therapist[2]);
                setEducationUpd(data.Therapist[2]);
                setAboutMe(data.Therapist[1]);
                setAboutMeUpd(data.Therapist[1]);
                setAvailability(data.Therapist[3]);
                setAvailabilityUpd(data.Therapist[3]);
                setPricingTxt(data.Therapist[4]);
                setPricingUpdTxt(data.Therapist[4]);
                setPricingNum(data.Therapist[8]);
                setPricingUpdNum(data.Therapist[8]);
                setAccepting(data.Therapist[7]);
                let totRevs = data.fives + data.fours + data.threes + data.twos + data.ones
                let avgStars = (5 * data.fives + 4 * data.fours + 3 * data.threes + 2 * data.twos + data.ones) / totRevs
                setReviewSummary({ "avgStars": avgStars, "individualReviews": [{ "fives": data.fives, "fours": data.fours, "threes": data.threes, "twos": data.twos, "ones": data.ones }] });
                setTotalReviews(totRevs);
            })
            .catch(err => console.error('Error fetching data:', err));

        // reviews
        fetch(`https://mentcare-backend.onrender.com/therapistReviewInfo`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urlUserId: userId, page: page }),
        })
            .then(res => res.json())
            .then(data => {
                setReviews(data.reviews);
            })
            .catch(err => console.error('Error fetching data:', err));

        // add rem therapist stuff
        const nonParamUserId = localStorage.getItem("userID");
        const userType = localStorage.getItem("userType");

        fetch(`https://mentcare-backend.onrender.com/isCurrentTherapist`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId: nonParamUserId, userType: userType, urlUserId: userId }),
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);
                setCurrentTherapist(data.isCurrentTherapist);
                setAbleToSwap(data.swapable);
            })
            .catch(err => console.error('Error fetching data:', err));
    }, []);

    // reviews
    useEffect(() => {
        fetch(`https://mentcare-backend.onrender.com/therapistReviewInfo`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urlUserId: userId, page: page }),
        })
            .then(res => res.json())
            .then(data => {
                setReviews(data.reviews);
            })
            .catch(err => console.error('Error fetching data:', err));
    }, [page]);

    useEffect(() => {
        AOS.init({ duration: 1500 });
    }, [])

    const paginationFunc = (event, value) => {
        setPage(value);
    }

    // editing data functions
    const startEditing = (event) => {
        event.preventDefault();
        setSpecializationsArr(specializations.split(','));
        setEducationUpd(education);
        setAboutMeUpd(aboutMe);
        setAvailabilityUpd(availability);
        setPricingUpdTxt(pricingTxt);
        setPricingUpdNum(pricingNum.toFixed(0));
        setEditing(1);
    }

    const cancelEditing = (event) => {
        event.preventDefault();
        setSpecializationsArr(specializations.split(','));
        setEditing(0);
    }

    const updText = (event, setFunc) => {
        event.preventDefault();
        if (setFunc === setPricingUpdNum) {
            if (/^[0-9]+$/.test(event.target.value)) {
                let priceNum = parseInt(event.target.value).toFixed(0);
                setFunc(priceNum);
            }
            else {
                setFunc(0);
            }
        }
        else {
            setFunc(event.target.value);
        }
    }

    function selectedSpecialization(e) {
        if (e.target.className === 'grid-spec') {
            e.target.className = 'grid-spec selected-spec';
        }
        else {
            e.target.className = 'grid-spec';
        }

        if (specializationsArr.includes(e.target.value)) {
            setSpecializationsArr(specializationsArr.filter(item => item !== e.target.value));
        }
        else {
            let otherArray = specializationsArr;
            otherArray.push(e.target.value);
            setSpecializationsArr(otherArray);
        }
    }

    const saveEditing = (event) => {
        event.preventDefault();
        fetch(`https://mentcare-backend.onrender.com/therapistUpdateInfo`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                urlUserId: userId,
                specializationsArr: specializationsArr.join(','),
                educationUpd: educationUpd,
                aboutMeUpd: aboutMeUpd,
                availabilityUpd: availabilityUpd,
                pricingUpd: pricingUpdTxt,
                pricingUpdNum: pricingUpdNum
            }),
        })
            .then(res => res.json())
            .then(data => {
                setSpecializations(String(data.specializations));
                setSpecializationsArr(String(data.specializations).split(','));
                setEducation(data.education);
                setAboutMe(data.aboutMe);
                setAvailability(data.availability);
                setPricingTxt(data.pricing);
                setPricingNum(data.pricingNum);
            })
            .catch(err => console.error('Error fetching data:', err));
        setEditing(0);
    }

    // add rem therapist
    const addRemTherapist = (event) => {
        event.preventDefault();
        const nonParamUserId = localStorage.getItem("userID");
        const userType = localStorage.getItem("userType");

        fetch(`https://mentcare-backend.onrender.com/addRemTherapist`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId: nonParamUserId, urlUserId: userId, currentlyTherapist: currentTherapist }),
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);
                setCurrentTherapist(data.nowHasTherapist);
            })
            .catch(err => console.error('Error fetching data:', err));
    }

    // leave review
    const startReview = () => {
        setUserReviewStars();
        setUserReviewText("");
        setRatingError(false);
        popupRef.current.className = 'popUp-background';
    }

    const cancelReview = () => {
        popupRef.current.className = 'hidden popUp-background';
    }

    const saveReview = (event) => {
        event.preventDefault();
        const nonParamUserId = localStorage.getItem("userID");
        if (userReviewStars !== 0 && userReviewStars !== undefined && userReviewText !== "") {
            fetch(`https://mentcare-backend.onrender.com/leaveReview`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: nonParamUserId,
                    urlUserId: userId,
                    review: userReviewText,
                    stars: userReviewStars,
                }),
            })
                .then(res => res.json())
                .then(data => {
                    if (data.reviewSent === 1) {
                        clearWaitingQueue();
                        toast.success('Review sent!');
                    }
                    else {
                        clearWaitingQueue();
                        toast.error('Review not sent.');
                    }
                })
                .catch(err => console.error('Error fetching data:', err));
            popupRef.current.className = 'hidden popUp-background';
        } else {
            setRatingError(true);
        }
    }

    const clearWaitingQueue = () => {
        toast.clearWaitingQueue();
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    };

    return (
        <div data-aos="fade-up">
            <ToastContainer
                limit={1}
                position="bottom-left"
                closeButton={false}
                hideProgressBar={true}
                pauseOnHover={false}
                autoClose={3000}
            />
            <form onSubmit={(event) => saveEditing(event)}>
                <div className="flex-col flex-centered" style={{ gap: '20px', paddingTop: '40px', fontSize: '14pt' }}>
                    <div className="flex-row" style={{ gap: '20px' }}>
                        <div className="card flex-col flex-centered thera-prof-top-left">
                            <div className='profile-pic-container'>
                                <div className="img-circle-mask">
                                    <img src={therapistPfp} alt='PROFILE PIC' className="profile-pic" />
                                </div>
                            </div>
                            <p>{therapistName}</p>
                            <Rating name="stars-overview" value={reviewSummary.avgStars} precision={0.1} size='large' readOnly />
                        </div>

                        <div className="card flex-col flex-centered thera-prof-top-right">
                            <h1>ABOUT ME</h1>
                            <div className={editing ? "hidden" : "flex-col"} style={{ maxWidth: '600px' }}>
                                <p>{aboutMe}</p>
                                <p><strong>Specializations: </strong>{specializations.replace(/,/g, ", ")}</p>
                                <p><strong>Education: </strong>{education}</p>
                            </div>
                            <div className={editing ? "flex-col" : "hidden"} style={{ gap: '20px' }}>
                                <div className='flex-col'>
                                    <label>Edit About Me</label>
                                    <textarea className='ther-profile-textarea' maxLength="255" value={aboutMeUpd} onChange={(event) => updText(event, setAboutMeUpd)} />
                                </div>
                                <div className='flex-col'>
                                    <label>Edit Specializations</label>
                                    <div className='grid-specs-container'>
                                        <input type='button' value={'Relationship'} className={specializations.includes("Relationship") ? 'grid-spec selected-spec' : 'grid-spec'} onClick={(e) => selectedSpecialization(e)} />
                                        <input type='button' value={'Depression'} className={specializations.includes("Depression") ? 'grid-spec selected-spec' : 'grid-spec'} onClick={(e) => selectedSpecialization(e)} />
                                        <input type='button' value={'Addiction'} className={specializations.includes("Addiction") ? 'grid-spec selected-spec' : 'grid-spec'} onClick={(e) => selectedSpecialization(e)} />
                                        <input type='button' value={'Anxiety'} className={specializations.includes("Anxiety") ? 'grid-spec selected-spec' : 'grid-spec'} onClick={(e) => selectedSpecialization(e)} />
                                        <input type='button' value={'PTSD'} className={specializations.includes("PTSD") ? 'grid-spec selected-spec' : 'grid-spec'} onClick={(e) => selectedSpecialization(e)} />
                                        <input type='button' value={'Family Therapy'} className={specializations.includes("Family Therapy") ? 'grid-spec selected-spec' : 'grid-spec'} onClick={(e) => selectedSpecialization(e)} />
                                        <input type='button' value={'Anger Mgmt.'} className={specializations.includes("Anger Mgmt.") ? 'grid-spec selected-spec' : 'grid-spec'} onClick={(e) => selectedSpecialization(e)} />
                                        <input type='button' value={'Confidence'} className={specializations.includes("Confidence") ? 'grid-spec selected-spec' : 'grid-spec'} onClick={(e) => selectedSpecialization(e)} />
                                    </div>
                                </div>
                                <div className='flex-col'>
                                    <label>Edit Education</label>
                                    <textarea className='ther-profile-textarea' maxLength="255" value={educationUpd} onChange={(event) => updText(event, setEducationUpd)} />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="flex-col flex-centered thera-prof-mid" style={{ gap: '20px' }}>
                        <div className='flex-row flex-centered' style={{ gap: '20px', 'alignItems': 'stretch', marginBottom: '40px' }}>
                            <div className='card flex-col'>
                                <h1>AVAILABILITY</h1>
                                <div className={editing ? "hidden" : "flex-col flex-centered"}>
                                    <div>{availability}</div>
                                </div>
                                <div className={editing ? "flex-col" : "hidden"}>
                                    <label>Edit Availability</label>
                                    <textarea className='ther-profile-textarea' maxLength="255" value={availabilityUpd} onChange={(event) => updText(event, setAvailabilityUpd)} />
                                </div>
                            </div>

                            <div className='card flex-col'>
                                <h1>PRICING</h1>
                                <div className={editing ? "hidden" : "flex-col flex-centered"} style={{ maxWidth: '500px' }}>
                                    <div>{pricingTxt}<br /><strong>Price:</strong> ${pricingNum}</div>
                                </div>
                                <div className={editing ? "flex-col flex-centered" : "hidden"}>
                                    <label>Edit Pricing Info</label>
                                    <textarea className='ther-profile-textarea' maxLength="255" value={pricingUpdTxt} onChange={(event) => updText(event, setPricingUpdTxt)} />
                                    <label>Edit Pricing Number</label>
                                    <input type="text" className='ther-profile-textarea' min="0" value={pricingUpdNum} style={{ height: "20px", width: "200px" }} onChange={(event) => updText(event, setPricingUpdNum)} onKeyPress={handleKeyPress} />
                                </div>
                            </div>
                        </div>

                        <button className={(localStorage.getItem("userType") === "Therapist" && editing === 0 && localStorage.getItem("realUserID") === userId) ? "td-btn" : "hidden"} onClick={(event) => startEditing(event)}>Edit Details</button>
                        <div className='flex-row flex-centered' style={{ gap: '20px' }}>
                            <input type="submit" className={(localStorage.getItem("userType") === "Therapist" && editing === 1) ? "td-btn" : "hidden"} value="Save Details" /><br />
                            <button className={(localStorage.getItem("userType") === "Therapist" && editing === 1) ? "td-btn" : "hidden"} onClick={(event) => cancelEditing(event)}>Cancel Editing</button>
                        </div>

                        <button className={((localStorage.getItem("userType") === "Patient") && (accepting && ableToSwap)) ? "td-btn" : "hidden"} onClick={(event) => addRemTherapist(event)}>{(currentTherapist) ? "Remove" : "Add"} Therapist</button>
                        <p className={((localStorage.getItem("userType") === "Patient") && !accepting && !currentTherapist) ? "td-btn-no-hover flex-centered" : "hidden"}>Therapist is not accepting patients</p>

                        <div className='flex-col flex-centered' style={{ gap: '60px' }}>
                            <div className="flex-centered flex-col" style={{ gap: '20px' }}>
                                <h1>Reviews</h1>
                                <div className="flex-centered flex-row">
                                    5<Rating name="5Stars" value={1} max={1} size='large' readOnly />
                                    <Slider
                                        value={reviewSummary.individualReviews[0].fives}
                                        max={totalReviews}
                                        sx={{ width: "500px", '& .MuiSlider-thumb': { display: 'none' } }}
                                        disabled />
                                </div>
                                <div className="flex-centered flex-row">
                                    4<Rating name="4Stars" value={1} max={1} size='large' readOnly />
                                    <Slider
                                        value={reviewSummary.individualReviews[0].fours}
                                        max={totalReviews}
                                        sx={{ width: "500px", '& .MuiSlider-thumb': { display: 'none' } }}
                                        disabled />
                                </div>
                                <div className="flex-centered flex-row">
                                    3<Rating name="3Stars" value={1} max={1} size='large' readOnly />
                                    <Slider
                                        value={reviewSummary.individualReviews[0].threes}
                                        max={totalReviews}
                                        sx={{ width: "500px", '& .MuiSlider-thumb': { display: 'none' } }}
                                        disabled />
                                </div>
                                <div className="flex-centered flex-row">
                                    2<Rating name="2Stars" value={1} max={1} size='large' readOnly />
                                    <Slider
                                        value={reviewSummary.individualReviews[0].twos}
                                        max={totalReviews}
                                        sx={{ width: "500px", '& .MuiSlider-thumb': { display: 'none' } }}
                                        disabled />
                                </div>
                                <div className="flex-centered flex-row">
                                    1<Rating name="1Stars" value={1} max={1} size='large' readOnly />
                                    <Slider
                                        value={reviewSummary.individualReviews[0].ones}
                                        max={totalReviews}
                                        sx={{ width: "500px", '& .MuiSlider-thumb': { display: 'none' } }}
                                        disabled />
                                </div>
                            </div>
                            <div className="flex-row">
                                {reviews && reviews.map((item, index) => (
                                    <div className="card flex-centered flex-col" style={{ marginLeft: "25px", marginRight: "25px", marginBottom: "10px", width: "175px" }}>
                                        <div className="flex-centered flex-col">
                                            <div className='reviews-profile-pic-container'>
                                                <div className="img-circle-mask" style={{ width: '100px', height: '100px' }}>
                                                    <img src={item[4] !== null ? `/assets/profile-pics/${item[4]}` : '/assets/images/default-profile-pic.jpg'} alt='PROFILE PIC' className="profile-pic" />
                                                </div>
                                            </div>
                                            <p>{item[3]}<br />{item[2].slice(0, -13)}</p><Rating name="1Stars" value={item[1]} max={5} readOnly />
                                        </div>
                                        <div style={{ width: "175px", maxHeight: "150px", overflowY: "auto", overflowX: "hidden" }}>
                                            <p>{item[0]}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <Pagination variant="text" shape="rounded" count={Math.ceil(totalReviews / 4)} onChange={paginationFunc} /> <br />
                        <button className={(localStorage.getItem("userType") === "Patient" && currentTherapist) ? "td-btn" : "hidden"} onClick={() => startReview()}>Add Review</button>
                    </div>
                </div>
            </form>

            <div ref={popupRef} className="hidden popUp-background">
                <div className='popUp'>
                    <form className="flex-col flex-centered main-container" onSubmit={(event) => saveReview(event)}>
                        <FormControl className="flex-col flex-centered main-container">
                            <textarea className="ther-profile-textarea" maxLength="255" value={userReviewText} onChange={(event) => updText(event, setUserReviewText)} />
                            <Rating name="userReviewRating" value={userReviewStars} max={5} onChange={(event, newValue) => setUserReviewStars(newValue)} required />
                            {ratingError && <FormHelperText>Please fill out stars & text box</FormHelperText>}
                        </FormControl>
                        <div className="flex-row flex-centered main-container" style={{ gap: "10px" }}>
                            <input className='td-btn' type="submit" value="Send Review" />&nbsp;
                            <button className='td-btn' type="button" onClick={() => cancelReview()}>Cancel Review</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default TherapistProfile;