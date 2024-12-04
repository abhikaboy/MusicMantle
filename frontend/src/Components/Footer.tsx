import React from 'react';

export default function Footer() {
	return (
		<div
			style={{
				position: 'fixed',
				bottom: 0,
				left: 0,
				padding: 8,
				backgroundColor: '#394262',
				fontSize: '16px',
				width: '100%',
			}}>
			<p
				className='read-the-docs'
				style={{
					color: 'white',
				}}>
				Danny Vesga, Abhik Ray
			</p>
		</div>
	);
}
