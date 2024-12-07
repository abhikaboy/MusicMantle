import './App.css';

import Footer from './Components/Footer';
import { useEffect, useState } from 'react';
import GuessTable from './Components/GuessTable';
import Modal from 'react-modal';

type Guess = {
	num: number;
	guess: string;
	similarity: number | string;
	proximity: string;
};

type CheckReponse = {
	name: string;
	score: number;
};

function App() {
	const [guesses, setGuesses] = useState<Guess[]>([]);

	const [secret, setSecret] = useState('');
	const [prompt, setPrompt] = useState('');
	const [guess, setGuess] = useState('');

	const [victory, setVictory] = useState(false);
	const [givenUp, setGivenUp] = useState(false);
	const [showHint, setShowHint] = useState(false);

	const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
		if (e.key === 'Enter') {
			submitGuess(guess);
		}
	};

	const getProximity = (similarity: number) => {
		if (similarity > 0.7) return 'Very Warm';
		if (similarity > 0.42) return 'Warm';
		if (similarity > 0.2) return 'Cool';
		else return 'Very Cold';
	};

	const submitGuess = (guess: string) => {
		if (guess == '') return;

		fetch(`http://127.0.0.1:8000/check?secret=${secret}&term=${guess}`, {
			method: 'GET',
		})
			.then((res) => res.json())
			.then((data) => {
				const [result]: CheckReponse[] = data;
				console.log(result);
				// remap the score from 0.3-0.6 to 0-1

				const similarity = (result.score - 0.3) * 1 * 4;
				setGuesses([
					{
						num: guesses.length + 1,
						guess,
						similarity: similarity.toFixed(4),
						proximity: getProximity(similarity),
					},
					...guesses,
				]);
				if (guess == secret) {
					setVictory(true);
				}
				setGuess('');
			})
			.catch((err) => {
				console.log(err);
			});
	};

	useEffect(() => {
		fetch('http://127.0.0.1:8000/random', {
			method: 'GET',
		})
			.then((res) => res.json())
			.then((data) => {
				console.log(data);
				setSecret(data.name);
				setPrompt(data.prompt);
			});
	}, []);

	return (
		<>
			<Modal
				isOpen={showHint}
				onRequestClose={() => setShowHint(false)}
				style={styles.modal}
				contentLabel='Example Modal'>
				<h2>Hint</h2>
				<p>The artist is from {prompt.split(' from ')[1]}</p>
			</Modal>
			<Modal
				isOpen={givenUp}
				onRequestClose={() => setGivenUp(false)}
				style={styles.modal}
				contentLabel='Example Modal'>
				<h2>{secret}</h2>
				<p>{prompt}</p>
			</Modal>
			<Modal
				isOpen={victory}
				onRequestClose={() => setVictory(false)}
				style={styles.modal}
				contentLabel='Example Modal'>
				<h2>Victory!</h2>
				<p>
					You guessed the artist! which is <b>{secret}</b>
				</p>
				<p>{prompt}</p>
			</Modal>
			<h1>Music Mantle</h1>
			<div className='card' style={{ paddingLeft: '20%', paddingRight: '20%' }}>
				<div>
					<input
						type='text'
						placeholder=''
						id='name'
						value={guess}
						onChange={(e) => setGuess(e.target.value)}
						onKeyDown={handleKeyDown}
						style={styles.inputStyle}
					/>
					<button onClick={() => submitGuess(guess)}>Guess</button>
				</div>
			</div>
			<div style={styles.tableContainer}>
				<GuessTable guesses={guesses} />
			</div>{' '}
			<div style={styles.actionContainer}>
				<button style={styles.outline} onClick={() => setShowHint(true)}>
					Hint
				</button>
				<button style={styles.outline} onClick={() => setGivenUp(true)}>
					Give Up
				</button>
			</div>
			<Footer />
			<div style={{ height: '20vh' }} />
		</>
	);
}

const styles = {
	tableContainer: {
		width: '60%',
		margin: 'auto',
	},
	inputStyle: {
		width: '50%',
		padding: 16,
		backgroundColor: '#F4F4F4',
		border: '0px',
		borderRadius: '8px',
		fontSize: '16px',
	},
	actionContainer: {
		display: 'flex',
		gap: 16,
		width: '100%',
		alignItems: 'center',
		justifyContent: 'center',
		margin: 'auto',
		marginTop: 32,
	},
	outline: {
		border: '2px solid #394262',
		padding: '8px',
		borderRadius: '8px',
		backgroundColor: '#ffffff',
		color: '#394262',
	},
	modal: {
		content: {
			top: '50%',
			left: '50%',
			right: 'auto',
			bottom: 'auto',
			marginRight: '-50%',
			transform: 'translate(-50%, -50%)',
			border: 'none',
			padding: '32px',
			backgroundColor: '#ffffff',
			overflow: 'hidden',
			width: '50%',
		},
		overlay: {
			background: '#000000c0',
		},
	},
};

export default App;
