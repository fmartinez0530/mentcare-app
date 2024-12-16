import { Row, Col } from 'react-grid-system';
import { Box, Button, FormControlLabel, TextField } from '@mui/material';
import React, { useState, useEffect } from "react";
import { useLocation } from 'react-router-dom';
import Grid from '@mui/material/Grid2';
import "./styles/Payment.css";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Checkbox from '@mui/material/Checkbox';

function Payment() {
    const [save, setSave] = useState(false);
    const [alreadyIn, setAlreadyIn] = useState(false);
    const patientId = localStorage.getItem('userID');
    const location = useLocation(); // Get the location object
    const { invoiceID, amountDue, therapistName } = location.state || {}
    const notifySuccess = () => {
        toast.success('Payment Successful! Redirecting to dashboard.');
    };
    const notifyFail = () => {
        toast("Payment Failed!");
    }

    const [formInput, setFormInput] = useState({
        patientId: '',
        amount: '',
        cardNum: '',
        cvc: '',
        month: '',
        year: '',
        firstName: '',
        lastName: '',
        city: '',
        billingAddress: '',
        state: '',
        country: '',
        zip: '',
        phone: '',
    });

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                const response = await fetch("https://mentcare-backend.onrender.com/getDetails", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        patientId
                    }),
                });
                const data = await response.json();
                console.log("Fetched details:", data);

                if (data.length === 0) {
                    setFormInput({
                        patientId,
                        amount: amountDue,
                        cardNum: '',
                        cvc: '',
                        month: '',
                        year: '',
                        firstName: '',
                        lastName: '',
                        city: '',
                        billingAddress: '',
                        state: '',
                        country: '',
                        zip: '',
                        phone: '',
                    });
                } else {
                    setFormInput({
                        patientId,
                        amount: amountDue,
                        cardNum: data[0][2],
                        cvc: data[0][3],
                        month: new Date(data[0][4]).getMonth() + 1,
                        year: new Date(data[0][4]).getFullYear(),
                        firstName: data[0][5],
                        lastName: data[0][6],
                        city: data[0][7],
                        billingAddress: data[0][8],
                        state: data[0][9],
                        country: data[0][10],
                        zip: data[0][11],
                        phone: data[0][12],
                    });
                    setSave(true);
                    setAlreadyIn(true);
                }
            } catch (error) {
                console.error("No details", error);
            }
        };

        fetchDetails();
    }, [patientId, amountDue]);

    // console.log(invoiceID);
    // console.log(amountDue);
    // console.log(therapistName);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormInput((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    }

    const handleSubmit = async (e) => {
        e.preventDefault(); //

        console.log(formInput);
        let phone = formInput.phone || null;

        const date = new Date(formInput.year, formInput.month, 0);
        const formDate = date.toLocaleDateString('en-CA');

        try {
            const response = await fetch("https://mentcare-backend.onrender.com/submitPayment", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    patientId: patientId,
                    invoiceId: invoiceID,
                    amount: amountDue,
                    cardNum: formInput.cardNum,
                    cvc: formInput.cvc,
                    expDate: formDate,
                    firstName: formInput.firstName,
                    lastName: formInput.lastName,
                    city: formInput.city,
                    billingAddress: formInput.billingAddress,
                    state: formInput.state,
                    country: formInput.country,
                    zip: formInput.zip,
                    phone: phone,
                    check: save,
                    alreadyIn: alreadyIn,
                }),
            });

            if (response.ok) {
                notifySuccess();
                setTimeout(() => {
                    window.location.href = "https://mentcare-frontend.onrender.com/dashboard";
                }, 2000);
            } else {
                notifyFail();
            }
        } catch (error) {
            console.error("Error submitting payment:", error);
            notifyFail();
        }
    };


    const handleDetails = (e) => {
        setSave(e.target.checked);
    }

    return (
        <div className="payment-page">
            <ToastContainer
                limit={1}
                position="bottom-left"
                closeButton={false}
                hideProgressBar={true}
                pauseOnHover={false}
                autoClose={3000}
            />
            <div>
                <Box className="payment-main-container" component="form" onSubmit={handleSubmit}>
                    <Grid>
                        <Row className="row-spacing title">
                            <Col><h1 style={{ margin: 0 }}>Payment</h1></Col>
                        </Row>
                        <Row className="row-spacing title">
                            <Col><h2 style={{ color: 'black', margin: 0 }}>Invoice to: {therapistName}<br />Amount: {amountDue}$</h2></Col>
                        </Row>
                        <Row>
                            <Col><h2 style={{ color: 'black', margin: 0, marginTop: 15, marginBottom: 10 }}>Payment Method</h2></Col>
                        </Row>
                        <Row gutterWidth={30} style={{ gap: '20px' }}>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>Card Number:</div>
                                <TextField required size='small' style={{ width: 250 }} name='cardNum' value={formInput.cardNum} onChange={handleChange} variant='filled' label="Card" /></Col>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>Expiration Date:</div>
                                <div style={{ display: "flex", gap: "10px" }}>
                                    <TextField required name='month' style={{ width: 80 }} value={formInput.month} onChange={handleChange} variant='filled' label="Month" size='small' />
                                    <TextField required name='year' style={{ width: 80 }} value={formInput.year} onChange={handleChange} variant='filled' label="Year" size='small' />
                                </div>
                            </Col>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>Security Code:</div>
                                <TextField required name='cvc' style={{ width: 100 }} value={formInput.cvc} onChange={handleChange} variant='filled' size='small' label='Code' /></Col>
                        </Row>
                    </Grid>
                    <Grid className='flex-col' style={{ width: '100%', gap: '10px' }}>
                        <Row>
                            <Col><h2 style={{ color: 'black', margin: 0, marginTop: 10, marginBottom: 5 }}>Billing Information</h2></Col>
                        </Row>
                        {/* <Row gutterWidth={30} style={{ gap: '20px' }}>
                        <Col className='payment-label'>Card Number:<br /><TextField required size='small' style={{ width: 250 }} name='cardNum' value={formInput.cardNum} onChange={handleChange} variant='filled' label="Card" /></Col>
                        <Col className='payment-label'>Expiration Date:<br />
                            <div style={{ display: "flex", gap: "10px" }}>
                                <TextField required name='month' style={{ width: 80 }} value={formInput.month} onChange={handleChange} variant='filled' label="Month" size='small' />
                                <TextField required name='year' style={{ width: 80 }} value={formInput.year} onChange={handleChange} variant='filled' label="Year" size='small' />
                            </div>
                        </Col>
                        <Col className='payment-label'>Security Code:<br /><TextField required name='cvc' style={{ width: 100 }} value={formInput.cvc} onChange={handleChange} variant='filled' size='small' label='Code' /></Col>
                    </Row> */}
                        <Row gutterWidth={30} style={{ gap: '20px', width: 'max-content' }}>
                            <Col className='payment-label'>
                                <div style={{ display: "flex", gap: "10px", width: 'max-content' }}>
                                    <div className='flex-col' style={{ gap: '5px' }}>
                                        <div>First Name:</div>
                                        <TextField required size='small' style={{ width: 120 }} name='firstName' value={formInput.firstName} onChange={handleChange} variant='filled' label="First" />
                                    </div>
                                    <div className='flex-col' style={{ gap: '5px' }}>
                                        <div>Last Name:</div>
                                        <TextField required size='small' style={{ width: 120 }} name='lastName' value={formInput.lastName} onChange={handleChange} variant='filled' label="Last" />
                                    </div>
                                </div>
                            </Col>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>City:</div>
                                <TextField required size='small' style={{ width: 250 }} name='city' value={formInput.city} onChange={handleChange} variant='filled' label='City' /></Col>
                        </Row>
                        <Row gutterWidth={30} style={{ gap: '20px', width: 'max-content' }}>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>Billing Address:</div>
                                <TextField required size='small' style={{ width: 250 }} name='billingAddress' value={formInput.billingAddress} onChange={handleChange} variant='filled' label='Billing' /></Col>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>State/Province:</div>
                                <TextField required size='small' style={{ width: 250 }} name='state' value={formInput.state} onChange={handleChange} variant='filled' label='Place' /></Col>
                        </Row>
                        <Row gutterWidth={30} style={{ gap: '20px', width: 'max-content' }}>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>Country:</div>
                                <TextField required size='small' style={{ width: 250 }} name='country' value={formInput.country} onChange={handleChange} variant='filled' label='Country' /></Col>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>Zip or Postal Code:</div>
                                <TextField required size='small' style={{ width: 250 }} name='zip' value={formInput.zip} onChange={handleChange} variant='filled' label='Post' /></Col>
                        </Row>
                        <Row gutterWidth={30} style={{ gap: '20px', width: 'max-content' }}>
                            <Col className='payment-label flex-col' style={{ gap: '5px' }}>
                                <div>Phone Number:</div>
                                <TextField size='small' style={{ width: 250 }} name='phone' value={formInput.phone} onChange={handleChange} variant='filled' label="Number" /></Col>
                        </Row>
                    </Grid>
                    <FormControlLabel
                        className='flex-centered' control={<Checkbox checked={save}
                            onChange={handleDetails} />} label="Save payment details"
                        slotProps={{
                            typography: {
                                sx: {
                                    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
                                },
                            },
                        }}
                    />
                    <Button style={{ marginTop: '20px' }} variant='contained' type='submit'>Submit</Button>
                </Box>
            </div>
        </div>
    );
}


export default Payment;