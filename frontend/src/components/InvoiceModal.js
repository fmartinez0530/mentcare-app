import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import "../pages/styles/Chat.css";
import { useEffect, useRef, useState } from 'react';
import { Button } from '@mui/material';


const style = {
	position: 'absolute',
	top: '50%',
	left: '50%',
	transform: 'translate(-50%, -50%)',
	width: 200,
	height: 140,
	bgcolor: 'rgba(87, 216, 194)',
	border: '2px solid #000',
	boxShadow: 24,
	textAlign: 'center',
	padding: '0',
	p: 4,
};

export default function BasicModalInvoice({ patientId, therapistId }) {
	const [open, setOpen] = React.useState(false);
	const handleOpen = () => {
		setAmount(chargingPrice)
		setOpen(true);
	}
	const handleClose = () => setOpen(false);
	const [amount, setAmount] = React.useState('');
	const [chargingPrice, setChargingPrice] = useState(null);
	const textFieldRef = useRef(null);
	// useEffect(() => {
	// 	if (open) {
	// 		setTimeout(() => {
	// 			if (textFieldRef.current) {
	// 				textFieldRef.current.focus();
	// 			}
	// 		}, 100);
	// 	}
	// }, [open]);

	useEffect(() => {
		const fetchCharging = async () => {
			try {
				const response = await fetch("https://mentcare-backend.onrender.com/getCharging", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						therapistId: therapistId
					}),
				});
				const data = await response.json();
				console.log("Fetched charging:", data);
				setChargingPrice(data[0][0]);
				setAmount(data[0][0]);
			} catch (error) {
				console.error("No charging", error);
			}
		};
		fetchCharging();
	}, [therapistId]);

	const handleInput = async (e) => {
		e.preventDefault();
		console.log(patientId)
		console.log(therapistId)
		console.log(amount)
		await fetch("https://mentcare-backend.onrender.com/sendInvoice", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				patientId: patientId,
				therapistId: therapistId,
				amountDue: amount
			}),
		});
		handleClose();
	};

	const handleRestrict = (e) => {
		const value = e.target.value;
		if (parseFloat(value) > 0) {
			setAmount(value);
		}
	}

	// const handlePress = (e) => {
	// 	if (e.key === '-' || e.key === '+') {
	// 		e.preventDefault();
	// 	}
	// 	else if (e.key === 'Enter') {
	// 		handleInput();
	// 	}
	// }

	return (
		<div>
			<button onClick={handleOpen} className='invoice-button'>Send Invoice</button>
			<Modal
				open={open}
				onClose={handleClose}
				aria-labelledby="invoice-title"
				aria-describedby="invoice-description"
			>
				<Box component="form" onSubmit={handleInput} sx={style}>
					<>
						<Typography id="modal-modal-title" variant="h5" component="h2" style={{ marginBottom: 15 }}>
							Send Invoice
						</Typography>
						<TextField
							required
							inputRef={textFieldRef}
							id="outlined-number"
							label="Amount Due"
							defaultValue={amount}
							type="number"
							onChange={handleRestrict}
							// onKeyDown={handlePress}
							slotProps={{
								input: { inputProps: { min: 0 } },
							}}
						/>
						<Button style={{ marginTop: '10px' }} variant='contained' type='submit'>Submit</Button>
					</>
				</Box>
			</Modal>
		</div>
	);
}