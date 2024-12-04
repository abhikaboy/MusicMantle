import React from 'react';

type Props = {
	guesses: Guess[];
};

const column = {
	width: '15%',
};

export default function GuessTable({ guesses }: Props) {
	return (
		<div>
			<div
				style={{
					display: 'flex',
					flexDirection: 'row',
					gap: 80,
					paddingLeft: 16,
					paddingRight: 16,
					borderBottom: '2px solid #394262',
				}}>
				<h3 style={column}>#</h3>
				<h3 style={column}>Guess</h3>
				<h3 style={column}>Similarity</h3>
				<h3 style={column}>Proximity</h3>
			</div>
			{guesses.reverse().map((guess, index) => (
				<div
					key={100 - index}
					style={{
						display: 'flex',
						flexDirection: 'row',
						gap: 80,
						paddingRight: 16,
					}}>
					<p style={column}>{guess.num}</p>
					<p style={column}>{guess.guess}</p>
					<p style={column}>{guess.similarity}</p>
					<p style={column}>{guess.proximity}</p>
				</div>
			))}
		</div>
	);
}
