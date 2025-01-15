import React, { useEffect, useState } from "react";

export default function Home() {
    const [market, setMarket] = useState('');

    function handleReasearch(e) {
        e.preventDefault();
        fetch(`/api/market?text=${market}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

    return (
        <div className="w-full h-full relative">
            <div className="w-full h-screen flex items-center justify-center flex-col gap-10">
                <h1 className="text-white text-6xl">Market researcher</h1>
                <form className="py-2 px-4 bg-white rounded-lg" onSubmit={handleReasearch}>
                    <input type="text" className="outline-none w-96 text-2xl" placeholder="Search for a market" onChange={(e) => {setMarket(e.target.value)}} />
                </form>
            </div>
        </div>
    );
}