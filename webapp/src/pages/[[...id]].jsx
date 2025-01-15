import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useRouter } from 'next/router';

export default function Home() {
    const [market, setMarket] = useState('');
    const [marketReasearched, setMarketReasearched] = useState(null);
    const [searchResults, setSearchResults] = useState(false);
    const router = useRouter();
    const reasearch_id = Array.isArray(router.query.id) ? router.query.id[0] : router.query.id;

    function handleReasearch(e) {
        e.preventDefault();
        if (!market) {
            toast.error('Please enter a market');
            return;
        }
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/create?term=${market}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!data.uuid) {
                throw new Error('Bad response');
            }
            router.replace(`/${data.uuid}`, undefined, { shallow: true });
            e.target.children[0].blur();
            setMarket('');
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

    useEffect(() => {
        if (reasearch_id) {
            setSearchResults(true);
            setMarketReasearched(market);
        }
    }, [reasearch_id]);

    return (
        <div className="w-full h-full relative">
            <div className={`w-full transition-all duration-700 ${reasearch_id ? "h-20 gap-0" : "h-screen gap-10"} flex items-center justify-center flex-col`}>
                <h1 className={`text-white text-6xl pointer-events-none duration-500 transition-all ${reasearch_id ? "h-0 opacity-0" : "h-16 opacity-100"}`}>Startup Market Researcher</h1>
                <form className="py-1 pl-4 pr-1 bg-white rounded-lg flex gap-2" onSubmit={handleReasearch}>
                    <input type="text" className="outline-none w-96 text-2xl my-1" placeholder="Search for a market" value={market} onChange={(e) => {setMarket(e.target.value)}} />
                    <button type="submit" className="bg-[#7E99A3] text-black text-2xl rounded px-2 transition-colors hover:bg-black hover:text-[#7E99A3]">Search</button>
                </form>
            </div>
            {searchResults && (
                <div className="w-full h-full px-10">
                    <p className="text-white text-3xl">Search results on {marketReasearched}</p>
                    <div className="w-full h-[calc(100vh-10rem)] flex items-center justify-center">
                        <div className="loader"></div>
                    </div>
                </div>
            )}
        </div>
    );
}