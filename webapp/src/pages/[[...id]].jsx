import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useRouter } from 'next/router';

export default function Home() {
    const [market, setMarket] = useState('');
    const [marketReasearched, setMarketReasearched] = useState(null);
    const [results, setResults] = useState("");
    const [showSearchResults, setShowSearchResults] = useState(false);
    const router = useRouter();
    const reasearch_id = Array.isArray(router.query.id) ? router.query.id[0] : router.query.id;

    function getResults(uuid) {
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/result?uuid=${uuid}`, {
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
            if (!data.result) {
                throw new Error('Bad response');
            }
            let results = data.result.split('\n');
            let resultsParsed = [];
            let inTable = false;
            let table = [];
            for (let i = 0; i < results.length; i++) {
                if (results[i][0] === '|' && results[i][results[i].length - 1] === '|') {
                    if (inTable) {
                        const row = results[i].split('|');
                        let isPushable = false;
                        // Detect lines where their cells are not all "-"
                        for (let j = 0; j < row.length; j++) {
                            for (let k = 0; k < row[j].length; k++) {
                                console.log(row[j][k]);
                                if (row[j][k] !== "-") {
                                    isPushable = true;
                                    break;
                                }
                            }
                            if (isPushable) {
                                break;
                            }
                        }
                        if (isPushable) {
                            table.push(row.slice(1, row.length - 1));
                        }
                    } else {
                        table = [];
                        const row = results[i].split('|');
                        table.push(row.slice(1, row.length - 1));
                    }
                    inTable = true;
                } else {
                    if (inTable) {
                        resultsParsed.push({
                            type: 'table',
                            value: table
                        });
                        inTable = false;
                        continue;
                    }
                    if (results[i].startsWith('# ')) {
                        resultsParsed.push({
                            type: 'title1',
                            value: results[i].replace('# ', '')
                        });
                    } else if (results[i].startsWith('## ')) {
                        resultsParsed.push({
                            type: 'title2',
                            value: results[i].replace('## ', '')
                        });
                    } else if (results[i].startsWith('### ')) {
                        resultsParsed.push({
                            type: 'title3',
                            value: results[i].replace('### ', '')
                        });
                    } else {
                        resultsParsed.push({
                            type: 'text',
                            value: results[i]
                        });
                    }
                }
            }
            console.log(resultsParsed);
            setResults(resultsParsed);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

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
            getResults(data.uuid);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

    useEffect(() => {
        if (reasearch_id) {
            setShowSearchResults(true);
            if (market) {
                setMarketReasearched(market);
            }
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
            {showSearchResults && (
                <div className="w-full h-full px-32 mt-20">
                    {marketReasearched && <p className="text-white text-3xl mb-8">Search results on {marketReasearched}</p>}
                    {!results ? <div className="w-full h-[calc(100vh-10rem)] flex items-center justify-center">
                        <div className="loader"></div>
                    </div> : (
                        <div className="flex flex-col gap-2 mb-10">
                            {results.map((result, index) => {
                                if (result.type === 'text') {
                                    return (
                                        <p key={index} className="text-white text-lg">{result.value}</p>
                                    );
                                } else if (result.type === 'title1') {
                                    return (
                                        <p key={index} className="text-white text-5xl mt-6">{result.value}</p>
                                    );
                                } else if (result.type === 'title2') {
                                    return (
                                        <p key={index} className="text-white text-4xl mt-4">{result.value}</p>
                                    );
                                } else if (result.type === 'title3') {
                                    return (
                                        <p key={index} className="text-white text-3xl mt-2">{result.value}</p>
                                    );
                                } else if (result.type === 'table') {
                                    return (
                                        <table key={index} className="w-full text-white border-collapse border border-white my-4">
                                            <tbody>
                                                {result.value.map((row, rowIndex) => {
                                                    return (
                                                        <tr key={rowIndex} className={`border border-white ${rowIndex === 0 && "bg-white text-[#4C585B]"}`}>
                                                            {row.map((cell, cellIndex) => {
                                                                return (
                                                                    <td key={cellIndex} className="border border-white p-2">{cell}</td>
                                                                );
                                                            })}
                                                        </tr>
                                                    );
                                                })}
                                            </tbody>
                                        </table>
                                    );
                                }
                            })}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}