import React, { useState, useEffect, useRef } from "react";
import "./styles/Chat.css";
import BasicModalInvoice from "../components/InvoiceModal";
import { io } from 'socket.io-client';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AOS from 'aos';
import 'aos/dist/aos.css';

function Chat() {
    const userType = localStorage.getItem('userType');
    const chooseId = localStorage.getItem('userID');
    const realUserID = localStorage.getItem('realUserID');

    const [therapists, setTherapists] = useState([]);
    const [selectedTherapist, setSelectedTherapist] = useState(null);
    const [chatHistory, setChatHistory] = useState([]);
    const [input, setInput] = useState("");
    const chatBoxRef = useRef(null);

    const socketRef = useRef(null);

    useEffect(() => {
        AOS.init({ duration: 1500 });
    }, [])

    useEffect(() => {
        if (socketRef.current) {
            socketRef.current.disconnect();
            socketRef.current = null;
        }
        const socket = io('https://mentcare-backend.onrender.com', {withCredentials:true, transports:['websocket', 'polling']})
        socketRef.current = socket;

        const fetchChats = async () => {
            const response = await fetch("https://mentcare-backend.onrender.com/userChats", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ chooseId, userType }),
            });
            const data = await response.json();
            console.log(data);
            setTherapists(data);
        };

        fetchChats();

        //  Connection
        socket.on('connect', () => {
            console.log(`Connected to Chats server (userID = ${realUserID})`);
            console.log("CHOOSE ID: ", chooseId);
            socket.emit("init-socket-comm", { "userID": realUserID });
        });
        //  Disconnect
        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        socket.on('start-chat-for-patient', async (data) => {
            console.log("Your therapist has started a chat! ");
            setSelectedTherapist({
                therapistID: chooseId,
                patientID: parseInt(data.therapistID),
                chatStatus: 'Active',
                requestStatus: 'Inactive'
            });
            const updatedUsers = await updateUsers();
            setTherapists(updatedUsers);
            const therapist = updatedUsers.filter(therap => therap.therapistID === parseInt(data.therapistID));
            // console.log(therapist[0]);
            // setChatHistory(JSON.parse(therapist[0].content).chats);
            const updatedTherapist = { ...therapist[0], requestStatus: 'Inactive' };
            handleTherapistSelect(updatedTherapist);

            // setSelectedTherapist((prevSelected) =>
            //     prevSelected ? { ...prevSelected, chatStatus: "Active" } : null
            // );
            // setSelectedTherapist((prevSelected) =>
            //     prevSelected ? { ...prevSelected, chatStatus: "Active" } : null
            // );
        });

        socket.on('end-chat-for-patient', async () => {
            console.log("Your therapist has ended the chat! ");

            setSelectedTherapist({
                therapistID: chooseId,
                patientID: selectedTherapist?.therapistID,
                chatStatus: 'Inactive',
                requestStatus: 'Inactive',
            });
            const updatedUsers = await updateUsers();
            console.log(updatedUsers);
            setTherapists(updatedUsers);
            const therapist = updatedUsers.filter(therap => therap.patientID === selectedTherapist?.patientID);
            handleTherapistSelect(therapist[0]);
        });

        socket.on('request-chat', async (data) => {
            console.log("Patient has sent a chat request!");
            console.log(data.patientID);

            setSelectedTherapist({
                therapistID: parseInt(data.patientID),
                patientID: chooseId,
                chatStatus: 'Inactive',
                requestStatus: 'Active',
            });
            const updatedUsers = await updateUsers();
            console.log(updateUsers);
            setTherapists(updatedUsers);
            const therapist = updatedUsers.filter(therap => therap.patientID === parseInt(data.patientID));
            handleTherapistSelect(therapist[0]);
        });

        socket.on('new-message', (data) => {
            console.log('got message');
            setChatHistory((prevChatHistory) => [
                ...prevChatHistory,
                { msg: data.message, sender: data.sender }
            ]);
            if (chatBoxRef.current) {
                chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
            }
        });

        return () => {
            socket.emit("rem-socket-comm", { "userID": realUserID });
            socket.off('start-chat-for-patient');
            socket.off('new-message');
            socket.off('end-chat-for-patient');
            socket.off('request-chat');
            // socket.off('chat-start');
            // socket.off('chat-end');
            socket.disconnect();
        };
    }, [chooseId, userType]);

    const handleTherapistSelect = (therapist) => {
        setSelectedTherapist({
            therapistID: therapist.therapistID || therapist.patientID,
            therapistName: therapist.therapistName || therapist.patientName,
            content: therapist.content,
            chatStatus: therapist?.chatStatus,
            requestStatus: therapist.requestStatus,
            status: therapist?.status
        });
        setChatHistory(JSON.parse(therapist.content).chats);
    };

    const updateUsers = async () => {
        const response = await fetch("https://mentcare-backend.onrender.com/userChats", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ chooseId, userType }),
        });
        const data = await response.json();
        return data;
    };


    const handleSendMessage = async () => {
        if (input.trim() !== "" && selectedTherapist) {
            let sender;
            if (userType === "Therapist") {
                sender = "T";
            } else {
                sender = "P";
            }

            const newMessage = {
                sender: sender,
                msg: input,
            };
            setChatHistory([...chatHistory, newMessage]);
            setInput("");
            let patientId;
            let therapistId;

            if (userType === "Therapist") {
                patientId = selectedTherapist.therapistID;
            } else {
                patientId = chooseId;
            }

            if (userType === "Patient") {
                therapistId = selectedTherapist.therapistID;
            } else {
                therapistId = chooseId;
            }

            const response = await fetch("https://mentcare-backend.onrender.com/sendMessage", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    patientId: patientId,
                    therapistId: therapistId,
                    message: input,
                    sender: sender,
                }),
            });

            if (response.ok) {
                console.log("Message sent");
                setInput("");
            } else {
                console.error("err sendin");
            }
        }
    };

    const handleStatus = async (status, type) => {
        if (userType === "Therapist") {
            const patientId = selectedTherapist.therapistID;
            const response = await fetch("https://mentcare-backend.onrender.com/updateStatus", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    therapistId: chooseId,
                    patientId: patientId,
                    status: status,
                    type: type,
                }),
            });

            if (response.ok) {
                const updatedUsers = await updateUsers();
                setTherapists(updatedUsers);
                setSelectedTherapist((prevSelected) =>
                    prevSelected ? { ...prevSelected, chatStatus: status } : null
                );
            } else {
                console.error("Failed to update chatStatus");
            }
        }
        else if (userType === "Patient") {
            const therapistId = selectedTherapist.therapistID;
            const response = await fetch("https://mentcare-backend.onrender.com/updateStatus", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    therapistId: therapistId,
                    patientId: chooseId,
                    status: status,
                    type: type,
                }),
            });

            if (response.ok) {
                const updatedUsers = await updateUsers();
                console.log(updateUsers);
                setTherapists(updatedUsers);
                setSelectedTherapist((prevSelected) =>
                    prevSelected ? { ...prevSelected, requestStatus: status } : null
                );
            } else {
                console.error("Failed to update requestStatus");
            }
        }
    };

    const handleStartChat = () => {
        if (selectedTherapist) {
            const patientId = selectedTherapist.therapistID;
            const therapistID = chooseId;
            console.log(patientId);
            fetch('https://mentcare-backend.onrender.com/startChat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ patientId, therapistId: chooseId }),
            })
                .then(res => res.json())
                .then(data => {
                    //console.log("Successfully saved the journal");
                })
                .catch(err => console.error('Error fetching data:', err));
            // socket.emit('chat-start', {
            //     therapistId: chooseId,
            //     patientId: selectedTherapist?.therapistID,
            // });
            // console.log("started chat");
            handleStatus('Active', 'chat')
        }
    }

    const handleEndChat = () => {
        if (selectedTherapist) {
            const patientId = selectedTherapist.therapistID;
            console.log(patientId);
            fetch('https://mentcare-backend.onrender.com/endChat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ patientId }),
            })
                .then(res => res.json())
                .then(data => {
                    //console.log("Successfully saved the journal");
                })
                .catch(err => console.error('Error fetching data:', err));
            console.log("Ended  cat");
            handleStatus('Inactive', 'chat');
            setSelectedTherapist({
                therapistID: selectedTherapist?.therapistID,
                patientID: chooseId,
                therapistName: selectedTherapist.therapistName,
                chatStatus: 'Inactive',
                requestStatus: 'Inactive',
            });
        }
    }

    const handleRequestChat = () => {
        if (selectedTherapist) {
            const therapistId = selectedTherapist?.therapistID;
            const patientId = chooseId;
            console.log(chooseId);
            console.log(therapistId);
            fetch('https://mentcare-backend.onrender.com/requestChat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ therapistId, patientId }),
            })
                .then(res => res.json())
                .then(data => {
                    //console.log("Successfully saved the journal");
                })
                .catch(err => console.error('Error fetching data:', err));
            console.log("Ended  cat");
            handleStatus('Active', 'request');
        }
    }

    const handleKeyDown = (event) => {
        if (event.key === "Enter") {
            handleSendMessage();
        }
    };

    useEffect(() => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [chatHistory]);

    return (
        <div className="chat-page">
            <ToastContainer
                limit={1}
                position="bottom-left"
                closeButton={false}
                hideProgressBar={true}
                pauseOnHover={false}
                autoClose={3000}
            />
            <div data-aos='fade-up' className="main-container">
                <div className="sidebar">
                    <div className="chat-list">
                        {therapists.map((therapist) => {
                            const isCurrent = selectedTherapist?.therapistID === (therapist.therapistID || therapist.patientID);
                            return (
                                <button key={therapist.therapistID || therapist.patientID}
                                    className={therapist.chatStatus === 'Active' ? `chat-item ${isCurrent ? "current" : ""}` : `chat-item ${isCurrent ? "inactivechosen" : "inactive"}`}
                                    onClick={() => handleTherapistSelect(therapist)}>
                                    {therapist.therapistName || therapist.patientName}
                                </button>
                            );
                        })}
                    </div>
                    <div className="bottom-list">
                        {(userType === 'Therapist' && selectedTherapist?.chatStatus === 'Inactive' && selectedTherapist?.requestStatus === 'Active') ?
                            <div className="request-chat-button not" style={{ textAlign: "center" }}>Patient has requested to chat!</div> : ''}
                        {(userType === 'Therapist' && selectedTherapist?.chatStatus === 'Active') || (userType === 'Therapist' && selectedTherapist?.status === 'Inactive') ?
                            <button className="request-chat-button inactive">Start Chat</button> :
                            userType === 'Therapist' && selectedTherapist ?
                                <button className="request-chat-button" onClick={() => handleStartChat('Active', 'chat')}>Start Chat</button> :
                                (userType === 'Patient' && selectedTherapist?.chatStatus === 'Inactive' && selectedTherapist?.requestStatus === 'Inactive' && selectedTherapist?.status === 'Active') ?
                                    <button className="request-chat-button" onClick={() => handleRequestChat('Active', 'request')}>Request to chat</button> :
                                    (userType === 'Patient') ?
                                        <button className="request-chat-button inactive">Request to Chat</button> :
                                        <button className="request-chat-button inactive">Start Chat</button>}
                    </div>
                </div>
                <div className="chat-box-container">
                    <div className="chat-box-header">
                        {selectedTherapist ? selectedTherapist.therapistName || selectedTherapist.patientName : "Select a Chat"}
                    </div>
                    <div className="chat-box" ref={chatBoxRef}>
                        {chatHistory.map((message, index) => {
                            const isUserMessage =
                                (userType === "Patient" && message.sender === "P") ||
                                (userType === "Therapist" && message.sender === "T");
                            return (
                                <div
                                    key={index}
                                    className={`chat-bubble ${isUserMessage ? "user" : "therapist"}`}>
                                    {message.msg}
                                </div>
                            );
                        })}
                    </div>
                    {selectedTherapist && (
                        <div className="chat-input-container">
                            {selectedTherapist?.chatStatus === 'Active' ? <input
                                type="text"
                                className="chat-input"
                                placeholder="Type a message..."
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                            /> : <div className="chat-input inactive">This chat is inactive</div>}
                            {(selectedTherapist?.chatStatus === 'Active') ? <button className="send-button" onClick={() => handleSendMessage()}>Send</button> :
                                <button className="send-button inactive">Send</button>}
                        </div>
                    )}
                </div>
                {(selectedTherapist?.chatStatus === 'Active' && userType === 'Therapist') ? <div className="invoice-container">
                    <button className="invoice-button" onClick={() => handleEndChat('Inactive', 'chat')}>End Chat</button>
                    {/* <button className="invoice-button" onClick={BasicModalInvoice}>Send Invoice</button> */}
                    <BasicModalInvoice patientId={selectedTherapist?.therapistID} therapistId={chooseId} />
                </div> : ((selectedTherapist?.chatStatus === 'Inactive' && userType === 'Therapist') ?
                    <div className="invoice-container">
                        <button className="invoice-button inactive">End Chat</button>
                        <button className="invoice-button inactive">Send Invoice</button></div> :
                    ((userType === 'Therapist') ? <div className="invoice-container"></div> : ''))}
            </div> {/* Container end (kill me)*/}
        </div>
    );
}

export default Chat;
