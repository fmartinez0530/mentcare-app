import './styles/LandingPage.css';
import React, { useState, useEffect } from "react";
import { Row, Col } from 'react-grid-system';
import Grid from '@mui/material/Grid2';
import VideoPlayer from '../components/VideoPlayer';
import { Link } from 'react-router-dom';
// import FadeInSection from '../components/FadeInSection';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { Box } from '@mui/material';
import { useLocation } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function LandingPage() {
    const [openQuestion, setOpenQuestion] = useState(null);
    const [testimonials, setTestimonials] = useState([]);
    const [review, setReview] = useState("");
    const userType = localStorage.getItem('userType');
    const realUserID = localStorage.getItem('realUserID');
    const location = useLocation(); // Get the location object
    console.log(userType);

    const toggleQuestion = (index) => {
        setOpenQuestion((openQuestion === index) ? null : index);
    };

    useEffect(() => {
        AOS.init({ duration: 2000 });
    }, [])

    useEffect(() => {
        const fetchTestimonials = async () => {
            try {
                const response = await fetch("https://mentcare-backend.onrender.com/getTestimonials");
                const data = await response.json();
                console.log("Fetched testimonials:", data);
                setTestimonials(data);
            } catch (error) {
                console.error("No testimonials", error);
            }
        };
        fetchTestimonials();
    }, []);

    console.log("Fetched testimonials:", testimonials);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!review.trim()) {
            alert("Please enter a review before submitting.");
            return;
        }

        const response = await fetch("https://mentcare-backend.onrender.com/sendTestimonial", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                userId: realUserID,
                content: review,
            }),
        });
        if (response.ok) {
            toast.clearWaitingQueue();
            toast.success('Your review has been sent. Thank you for using MentCare!')
            setReview("");
        } else {
            toast.clearWaitingQueue();
            toast.error('Unable to send review. Try again later!')
        }

        // await fetch("https://mentcare-backend.onrender.com/sendTestimonial", {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json" },
        //     body: JSON.stringify({
        //         userId: realUserID,
        //         content: review,
        //     }),
        // });
    };

    return (
        <div className="landing-page">
            <ToastContainer
                limit={1}
                position="bottom-left"
                closeButton={false}
                hideProgressBar={true}
                pauseOnHover={false}
                autoClose={3000}
            />
            <div className="video-section">
                <div className="video">{VideoPlayer()}</div>
                <div data-aos="fade-up" className='video-text animation'>
                    <h1 className='outlined-text' style={{ marginBottom: '0' }}>Welcome to <span style={{ color: 'white' }}>MentCare</span></h1>
                    <h1 className='outlined-text'>Your Journey to Wellness starts here!</h1>
                    <Link to="/register" style={{ paddingTop: 80 }}>
                        <button className="landing-register-now">Register Now</button>
                    </Link>
                </div>
            </div>
            <div className="content-container flex-col">
                {/* <Row className="row-spacing">
                        <Col>
                            <Link to="/register">
                                <button className="send-button">Register Now</button>
                            </Link>
                        </Col>
                    </Row> */}

                {/* <FadeInSection> */}
                <Row data-aos="fade-up" className="row-spacing" style={{ paddingTop: 40, alignItems: 'center' }}>
                    <Col md={6} className='about-us'>
                        <h1 className='landing-heading' style={{ textAlign: 'center' }}>ABOUT US</h1>
                        <p style={{ textAlign: 'left' }}>
                            At MentCare, our mission is to create a safe, supportive, and accessible online space where individuals can prioritize their mental well-being. By connecting patients with licensed therapists through secure and meaningful interactions, we aim to empower users to overcome challenges, develop resilience, and lead fulfilling lives.
                        </p>
                        <p style={{ textAlign: 'left' }}>
                            Through our platform, we provide a confidential environment where patients can openly communicate with therapists via chat, receive personalized advice, and gain tools to navigate their mental health journey. Our commitment is to make professional mental health support more accessible, fostering a community of care and understanding in a digital world.
                        </p>
                        <p style={{ textAlign: 'left' }}>
                            We believe that everyone deserves compassionate support and the opportunity to thrive.
                        </p>
                    </Col>
                    <Col md={6}>
                        <div><img src="/assets/images/Mentcare_Symbol_Sans_AI.png" alt="image" width={320} height={320} /></div>
                    </Col>
                </Row>
                {/* </FadeInSection> */}

                {/* <FadeInSection> */}
                <div data-aos="fade-up" className="testimonial-users-section flex-col" style={{ paddingTop: 40, gap: '20px' }}>
                    <h1 className='landing-heading'>HEAR OUR HAPPY USERS!</h1>
                    <div className="testimonial-users-container">
                        {testimonials && testimonials.map((testimonial, index) => (
                            <div className={`testimonial-user ${(index % 2 === 0) ? "left" : "right"}`} key={testimonial.id}>
                                <div><div className="landing-img-circle-mask">{(testimonial.img === null) ? <img src='/assets/images/default-profile-pic.jpg' className='landing-profile-picture'></img> : <img src={`/assets/profile-pics/${testimonial.img}`} className='landing-profile-picture'></img>}</div>
                                    <div className='username' style={{ fontSize: '16pt' }}>{testimonial.username}</div></div>
                                <div className="testimonial"><span style={{ fontSize: '30pt' }}>"</span>{testimonial.content}<span style={{ fontSize: '30pt' }}>"</span></div>
                            </div>
                        ))}
                    </div>
                </div>
                {/* </FadeInSection> */}

                {/* <FadeInSection> */}
                <div data-aos="fade-up" className="faq-section" style={{ paddingTop: 40 }}>
                    <h1 className='landing-heading'>FAQs</h1>
                    <div className="faq-container">
                        <div className={`faq-bubble ${(openQuestion === 0) ? "open" : ""}`} onClick={() => toggleQuestion(0)}>
                            <div className="faq-question">How does online therapy work?</div>
                            {(openQuestion === 0) && (
                                <div className="faq-answer">Patients create an account, browse licensed therapists, and schedule sessions.
                                    Sessions can take place via video call, chat, or voice, depending on the therapist's and patient's preferences.</div>
                            )}
                        </div>
                        <div className={`faq-bubble ${(openQuestion === 1) ? "open" : ""}`} onClick={() => toggleQuestion(1)}>
                            <div className="faq-question">Is online therapy as effective as in-person therapy?</div>
                            {(openQuestion === 1) && (
                                <div className="faq-answer">Yes, numerous studies have shown that online therapy can be as effective as in-person therapy for many individuals and conditions.
                                    It also offers the convenience of accessing therapy from the comfort of your home.</div>
                            )}
                        </div>
                        <div className={`faq-bubble ${(openQuestion === 2) ? "open" : ""}`} onClick={() => toggleQuestion(2)}>
                            <div className="faq-question">How do I choose the right therapist?</div>
                            {(openQuestion === 2) && (
                                <div className="faq-answer">You can browse therapist profiles, read their qualifications,
                                    specialties, and client reviews, and filter by language, availability, and type of therapy they offer.</div>
                            )}
                        </div>
                    </div>
                </div>
                {/* </FadeInSection> */}

                {/* <FadeInSection> */}
                <div data-aos="fade-up" style={{ paddingTop: 40 }}>
                    <h1 className='landing-heading' style={{ textAlign: 'center' }}>Contact Us</h1>
                    <Row className="row-spacing">
                        {(userType !== null) ?
                            <Col md={6}>
                                <Box component="form" onSubmit={handleSubmit}>
                                    <h1>Leave a review!</h1>
                                    <textarea required placeholder="Enter review..." className="review-box" value={review} onChange={(e) => setReview(e.target.value)}></textarea>
                                    <button className="send-button" type='submit'>Send</button>
                                </Box>
                            </Col>
                            : null}
                        <Col md={(userType !== null) ? 6 : { span: 6, offset: 3 }} className={userType === null ? 'text-center' : ''}>
                            <div>
                                <h1>Need Assistance?</h1>
                                <p style={{ fontSize: '16pt' }}>Call: 111-222-3333</p>
                                <p style={{ fontSize: '16pt' }}>Email: mentcare@gmail.com</p>
                            </div>
                        </Col>
                    </Row>
                </div>
                {/* </FadeInSection> */}
            </div>
        </div >
    );
};

export default LandingPage;
