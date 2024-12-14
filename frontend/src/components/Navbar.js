import React, { useState, useEffect, useRef } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import io from 'socket.io-client';
import "./Navbar.css";
import "../presets.css";

const Navbar = () => {
    const [userData, setUserData] = useState(null);
    const [notifications, setNotifications] = useState(null);
    const [bellImage, setBellImage] = useState('/assets/images/notification-bell.png');
    const [profileImgUrl, setProfileImgUrl] = useState(null);
    const [isActive, setIsActive] = useState(null);

    //  Routing makes window.location not update on tab clicks
    const location = useLocation();
    const navigate = useNavigate();
    const [selectedTab, setSelectedTab] = useState(location.pathname);

    const bellRef = useRef(null);

    let isLoggedIn;
    const fakeUserID = localStorage.getItem("userID");
    // const isActive = localStorage.getItem("isActive");

    // if (isActive) {
    //     setTherapistIsActive(isActive)
    // }

    if (fakeUserID && fakeUserID !== "0") {
        isLoggedIn = true;
    } else {
        isLoggedIn = false;
    }

    async function handleTabClick(path) {
        if (path === "/logout") {
            localStorage.removeItem('realUserID');
            localStorage.setItem("userID", 0);
            localStorage.removeItem("userType");
            setUserData();
            setSelectedTab("/dashboard");
            return;
        }
        setSelectedTab(path.toLowerCase());
        // if (path === '/settings') {
        //     await fetch("https://mentcare-backend.onrender.com/updateSocketsNavbar", {
        //         method: "POST",
        //         headers: {
        //             "Content-Type": "application/json",
        //         },
        //         body: JSON.stringify({ 'realUserID': localStorage.getItem('realUserID') }),
        //     })
        //         .then((res) => {
        //             if (!res.ok) {
        //                 throw new Error('Network response was not ok');
        //             }
        //             return res.json();
        //         })
        //         .then((data) => {
        //         })
        //         .catch((err) => console.error("Error fetching data:", err));
        // }
    }

    const socketRef = useRef(null);

    useEffect(() => {
        if (socketRef.current) {
            socketRef.current.disconnect();
            socketRef.current = null;
        }

        const socket = io('https://mentcare-backend.onrender.com', {withCredentials:true, transports:['websocket', 'polling']});
        socketRef.current = socket;

        const fakeUserID = localStorage.getItem("userID");
        const realUserID = localStorage.getItem("realUserID");
        const userType = localStorage.getItem("userType");

        //  Connection
        socket.on('connect', () => {
            if (realUserID !== null) {
                console.log(`Connected to NAVBAR socket (userID = ${realUserID})`);
                socket.emit("init-socket-navbar-comm", { "userID": realUserID });
            }
            else {
                console.log('Real User ID is null. Unable to connect navbar socket');
            }
        });
        //  Disconnect
        socket.on('disconnect', () => {
            console.log(`Disconnected from NAVBAR socket (userID = ${realUserID})`);
        });

        socket.on('update-navbar', () => {
            console.log('Updated navbar!')
            fetch("https://mentcare-backend.onrender.com/navbarData", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ fakeUserID, userType }),
            })
                .then((res) => {
                    if (!res.ok) {
                        setUserData(null);
                        setNotifications(null);
                        throw new Error('Network response was not ok');
                    }
                    return res.json();
                })
                .then((data) => {
                    setUserData(data[0][0]);
                    setNotifications(data[1]);
                    if (userType === 'Therapist') {
                        setIsActive(data[0][0]['isActive'])
                    }
                })
                .catch((err) => console.error("Error fetching data:", err));

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
                        setProfileImgUrl(`/assets/profile-pics/${data.profileImg}`);
                        imageExists = false;
                    }
                    else {
                        setProfileImgUrl(null);
                    }
                })
                .catch((error) => {
                    console.error("Error fetching image:", error);
                });
        });

        // Cleanup on component unmount
        return () => {
            // socket.emit("rem-socket-navbar-comm", { "userID": realUserID });
            socket.off('update-navbar');
            socket.disconnect();
        };
    }, [selectedTab]);

    useEffect(() => {
        const fakeUserID = localStorage.getItem("userID");
        const realUserID = localStorage.getItem("realUserID");
        const userType = localStorage.getItem("userType");

        if (localStorage.getItem("userID") !== "0") {
            fetch("https://mentcare-backend.onrender.com/navbarData", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ fakeUserID, userType }),
            })
                .then((res) => {
                    if (!res.ok) {
                        setUserData(null);
                        setNotifications(null);
                        handleTabClick('/');
                        throw new Error('Network response was not ok');
                    }
                    return res.json();
                })
                .then((data) => {
                    setUserData(data[0][0]);
                    setNotifications(data[1]);
                    if (userType === 'Therapist') {
                        setIsActive(data[0][0]['isActive'])
                    }
                    handleTabClick(location.pathname);
                })
                .catch((err) => console.error("Error fetching data:", err));

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
                        setProfileImgUrl(`/assets/profile-pics/${data.profileImg}`);
                        imageExists = false;
                    }
                    else {
                        setProfileImgUrl(null);
                    }
                })
                .catch((error) => {
                    console.error("Error fetching image:", error);
                });
        }
        else {
            setUserData(null);
            setNotifications(null);
            handleTabClick('/');
        }
    }, [localStorage.getItem("userID"), localStorage.getItem("isActive")]);

    //  Use to update notifications
    useEffect(() => {
        if (!notifications) {
            setBellImage('/assets/images/notification-bell.png');
        } else {
            setBellImage('/assets/images/notification-bell-active.png');
        }
    }, [notifications]);

    //  Use to update current tab clicked
    useEffect(() => {
        handleTabClick(`${location.pathname}`)
    }, [location.pathname])

    function toggleNotifications() {
        if (bellRef.current.className === "notifs-dropdown-items hidden") {
            bellRef.current.className = "notifs-dropdown-items";
        } else {
            bellRef.current.className = "notifs-dropdown-items hidden";
        }
    }

    function handleNotificationClick(redLocation, notificationID) {
        if (redLocation !== "null") {
            handleTabClick(redLocation);
            navigate(redLocation);
            handleRemoveNotification(notificationID);
        }
    }

    function handleRemoveNotification(notificationID) {
        const updatedNotifications = [...notifications].filter(
            (notification) => notification.notificationID !== parseInt(notificationID)
        );
        if (updatedNotifications.length === 0) {
            setNotifications(null);
        } else {
            setNotifications(updatedNotifications);
        }

        fetch("https://mentcare-backend.onrender.com/deleteNotification", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ notificationID }),
        }).catch((err) => console.error("Error fetching data:", err));
    }

    return (
        <nav className="navbar">
            <div className="left-section flex-row">
                <div className="navbar-img-circle-mask">
                    <img src={'/assets/images/Mentcare_Symbol_Sans_AI_NoLeaf.png'} alt="Logo" className="navbar-profile-pic" />
                </div>
                <Link to="/" onClick={() => handleTabClick(`/`)}>
                    <h2 className={`${selectedTab === "/" ? "active-tab" : "selectable-tab"}`}>MentCare</h2>
                </Link>
            </div>

            <div className="right-section">
                {!isLoggedIn || !userData ? (
                    <Link to={`/login`} onClick={() => handleTabClick(`/login`)}>
                        <h2 className={`${selectedTab === "/login" ? "active-tab" : "selectable-tab"}`}>Login</h2>
                    </Link>
                ) : (
                    <>
                        {userData && (
                            <div className="flex-row flex-centered" style={{ gap: '30px' }}>
                                {userData.userType === "Patient" && (
                                    <>
                                        <Link to={`/dashboard`} onClick={() => handleTabClick(`/dashboard`)}>
                                            <h2 className={`${selectedTab === "/dashboard" ? "active-tab" : "selectable-tab"}`}>
                                                Dashboard
                                            </h2>
                                        </Link>
                                        <Link to={`/therapistlist`} onClick={() => handleTabClick(`/therapistlist`)}>
                                            <h2 className={`${selectedTab === "/therapistlist" ? "active-tab" : "selectable-tab"}`}>
                                                Therapist List
                                            </h2>
                                        </Link>
                                        <Link to={`/chat`} onClick={() => handleTabClick(`/chat`)}>
                                            <h2 className={`${selectedTab === "/chat" ? "active-tab" : "selectable-tab"}`}>
                                                Chats
                                            </h2>
                                        </Link>
                                    </>
                                )}
                                {userData.userType === "Therapist" && isActive ? (
                                    <>
                                        <Link to={`/dashboard`} onClick={() => handleTabClick(`/dashboard`)}>
                                            <h2 className={`${selectedTab === "/dashboard" ? "active-tab" : "selectable-tab"}`}>
                                                Dashboard
                                            </h2>
                                        </Link>
                                        <Link to={`/therapistprofile/${localStorage.getItem('realUserID')}`} onClick={() => handleTabClick(`/therapistprofile/${localStorage.getItem('realUserID')}`)}>
                                            <h2 className={`${selectedTab === `/therapistprofile/${localStorage.getItem('realUserID')}` ? "active-tab" : "selectable-tab"}`}>
                                                Profile
                                            </h2>
                                        </Link>
                                        <Link to={`/chat`} onClick={() => handleTabClick(`/chat`)}>
                                            <h2 className={`${selectedTab === "/chat" ? "active-tab" : "selectable-tab"}`}>
                                                Chats
                                            </h2>
                                        </Link>
                                    </>
                                ) : (
                                    <></>
                                )}
                                {userData ? (
                                    <div className="flex-row user-bell-container">
                                        <div className="dropdown flex-col flex-centered" style={{ gap: "10px", height: "100%" }}>
                                            <div className="flex-row flex-centered" style={{ position: 'relative' }}>
                                                <h2 className={`${selectedTab === "/settings" ? "active-tab" : "selectable-tab"}`} style={{ cursor: 'default' }}>{userData.userName}</h2>
                                                <div className='navbar-profile-pic-container'>
                                                    {profileImgUrl ? (
                                                        <div className="navbar-img-circle-mask">
                                                            <img src={profileImgUrl} alt="Profile" className="navbar-profile-pic" />
                                                        </div>
                                                    ) : (
                                                        <div className="navbar-img-circle-mask">
                                                            <img src={'/assets/images/default-profile-pic.jpg'} alt="Profile" className="navbar-profile-pic" />
                                                        </div>
                                                    )}
                                                </div>
                                                <div className="dropdown-items">
                                                    <Link
                                                        to={`/settings`}
                                                        onClick={() => handleTabClick(`/settings`)}
                                                        className="hamburger-item"
                                                    >
                                                        Settings
                                                    </Link>
                                                    <Link
                                                        to={`/login`}
                                                        onClick={() => handleTabClick(`/logout`)}
                                                        className="hamburger-item"
                                                    >
                                                        Log Out
                                                    </Link>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="notifs-dropdown flex-col flex-centered">
                                            <div
                                                className="flex-col flex-centered"
                                                style={{ height: "100%", marginTop: '20px', marginBottom: '20px' }}
                                            >
                                                <img
                                                    src={bellImage}
                                                    alt="notif-bell"
                                                    width={"40px"}
                                                    height={"40px"}
                                                    onClick={() => toggleNotifications()}
                                                />
                                            </div>

                                            {notifications && userData.userType === "Therapist" && isActive ? (
                                                <div
                                                    className="notifs-dropdown-items hidden"
                                                    ref={bellRef}
                                                >
                                                    {notifications.map((row, index) => (
                                                        <div
                                                            key={`notif-${index}`}
                                                            onClick={() =>
                                                                handleNotificationClick(
                                                                    `${row.redirectLocation}`,
                                                                    `${row.notificationID}`
                                                                )
                                                            }
                                                            className={`flex-row hamburger-item ${row.redirectLocation
                                                                ? "hamburger-item-pointer"
                                                                : "hamburger-item-no-pointer"
                                                                }`}
                                                        >
                                                            <div className="flex-col flex-centered">
                                                                {row.message}
                                                            </div>
                                                            <input
                                                                type="button"
                                                                value={"X"}
                                                                className='notif-close-btn'
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                    handleRemoveNotification(
                                                                        `${row.notificationID}`
                                                                    );
                                                                }}
                                                            />
                                                        </div>
                                                    ))}
                                                </div>
                                            ) : notifications && userData.userType === "Patient" ? (
                                                <div
                                                    className="notifs-dropdown-items hidden"
                                                    ref={bellRef}
                                                >
                                                    {notifications.map((row, index) => (
                                                        <div
                                                            key={`notif-${index}`}
                                                            onClick={() =>
                                                                handleNotificationClick(
                                                                    `${row.redirectLocation}`,
                                                                    `${row.notificationID}`
                                                                )
                                                            }
                                                            className={`flex-row hamburger-item ${row.redirectLocation
                                                                ? "hamburger-item-pointer"
                                                                : "hamburger-item-no-pointer"
                                                                }`}
                                                        >
                                                            <div className="flex-col flex-centered">
                                                                {row.message}
                                                            </div>
                                                            <input
                                                                type="button"
                                                                value={"X"}
                                                                className='notif-close-btn'
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                    handleRemoveNotification(
                                                                        `${row.notificationID}`
                                                                    );
                                                                }}
                                                            />
                                                        </div>
                                                    ))}
                                                </div>
                                            ) : (
                                                <div className="notifs-dropdown-items">
                                                    <div className="hamburger-item hamburger-item-no-pointer">
                                                        No Notifications!
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ) : (
                                    <p>Loading...</p>
                                )}
                            </div>
                        )}
                    </>
                )}
            </div>
        </nav >
    );
};

export default Navbar;


