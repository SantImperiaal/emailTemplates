import React, { useState } from 'react';

const LookupForm: React.FC = () => {
    const [A2, setA2] = useState('');
    const [B2, setB2] = useState('');
    const [C2, setC2] = useState('');
    const [D2, setD2] = useState('');
    const [E2, setE2] = useState('');
    const [F2, setF2] = useState('');
    const [result, setResult] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const response = await fetch('/api/lookup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ A2, B2, C2, D2, E2, F2 }),
        });

        const data = await response.json();
        setResult(data.message);
    };

    return (
        <div>
            <h1>Lookup Form</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>A2:</label>
                    <input type="text" value={A2} onChange={(e) => setA2(e.target.value)} required />
                </div>
                <div>
                    <label>B2 (Invoice Due Date):</label>
                    <input type="date" value={B2} onChange={(e) => setB2(e.target.value)} required />
                </div>
                <div>
                    <label>C2 (Application Date):</label>
                    <input type="date" value={C2} onChange={(e) => setC2(e.target.value)} required />
                </div>
                <div>
                    <label>D2:</label>
                    <input type="text" value={D2} onChange={(e) => setD2(e.target.value)} required />
                </div>
                <div>
                    <label>E2 (Study End Date):</label>
                    <input type="date" value={E2} onChange={(e) => setE2(e.target.value)} required />
                </div>
                <div>
                    <label>F2 (Invoice Date):</label>
                    <input type="date" value={F2} onChange={(e) => setF2(e.target.value)} required />
                </div>
                <button type="submit">Submit</button>
            </form>
            {result && <div><h2>Result:</h2><p>{result}</p></div>}
        </div>
    );
};

export default LookupForm;