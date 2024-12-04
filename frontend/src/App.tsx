import './App.css';

import Footer from './Components/Footer';
import { useState } from 'react';
import GuessTable from './Components/GuessTable';

function App() {
	const [guesses, setGuesses] = useState<Guess[]>([
		{
			num: 1,
			guess: 'Danny',
			similarity: 0.5,
			proximity: 'Warm',
		},
		{
			num: 2,
			guess: 'Abhik',
			similarity: 0.8,
			proximity: 'Warm',
		},
		{
			num: 3,
			guess: 'Bob',
			similarity: 0.8,
			proximity: 'Warm',
		},
	]);

	const [guess, setGuess] = useState('');
	const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
		if (e.key === 'Enter') {
			submitGuess(guess);
		}
	};
	const submitGuess = (guess: string) => {
		if (guess == '') return;
		setGuesses([{ num: guesses.length + 1, guess, similarity: 0.5, proximity: 'Warm' }, ...guesses]);
		setGuess('');
	};
	return (
		<>
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
				<button style={styles.outline}>Hint</button>
				<button style={styles.outline}>Give Up</button>
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
};

export default App;
