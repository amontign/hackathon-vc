import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useRouter } from 'next/router';

export default function Home() {
    const [market, setMarket] = useState('');
    const [marketReasearched, setMarketReasearched] = useState(null);
    const [results, setResults] = useState("");
    const [searchMode, setSearchMode] = useState(0);
    const [loadingResults, setLoadingResults] = useState(false);
    const [advancedParametersShow, setAdvancedParametersShow] = useState(false);
    const [advancedParameters, setAdvancedParameters] = useState([]);
    const [progress, setProgress] = useState(0);
    const [showSearchResults, setShowSearchResults] = useState(false);
    const router = useRouter();
    const [advancedParametersSelected, setAdvancedParametersSelected] = useState([]);
    const [loadingMessage, setLoadingMessage] = useState("Loading results...");
    const reasearch_id = Array.isArray(router.query.id) ? router.query.id[0] : router.query.id;

    function checkStatus(interval, uuid) {
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/status?uuid=${uuid}`, {
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
            if (!data.progress) {
                return;
            }
            setProgress(data.progress);
            /*if (data.search_term) {
                setMarketReasearched(data.search_term);
            }*/
            if (data.message) {
                setLoadingMessage(data.message);
            }
            if (data.progress !== 100) {
                return;
            }
            clearInterval(interval);
            if (data.result === undefined) {
                throw new Error('Bad response');
            }
            let results = data.result.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').split('\n');
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
                    if (results[i] === '---') {
                        resultsParsed.push({
                            type: 'dash',
                            value: ''
                        });
                    } else if (results[i].startsWith('# ')) {
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
                    } else if (results[i].startsWith('#### ')) {
                        resultsParsed.push({
                            type: 'title4',
                            value: results[i].replace('#### ', '')
                        });
                    } else {
                        resultsParsed.push({
                            type: 'text',
                            value: results[i]
                        });
                    }
                }
            }
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
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/create?search_type=${searchMode === 1 ? "market" : "company"}&term=${market}&overview_topics=${advancedParametersSelected}`, {
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
            //setMarket('');
            setLoadingResults(true);
            const interval = setInterval(() => {
                checkStatus(interval, data.uuid);
            }, 1000);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

    useEffect(() => {
        if (reasearch_id) {
            setShowSearchResults(true);
            /*if (market) {
                setMarketReasearched(market);
            }*/
            if (!loadingResults) {
                setLoadingResults(true);
                const interval = setInterval(() => {
                    checkStatus(interval, reasearch_id);
                }, 1000);
            }
        }
    }, [reasearch_id]);

    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/overview_topics`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            setAdvancedParameters(data);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }, []);

    return (
        <div className="w-full h-full relative">
            <div className={`w-full transition-all duration-700 ${reasearch_id ? "h-20 gap-0" : "h-screen gap-10"} flex items-center justify-center flex-col`}>
                <h1 className={`text-white text-6xl pointer-events-none duration-500 transition-all ${reasearch_id ? "h-0 opacity-0" : "h-16 opacity-100"}`}>Startup Market Researcher</h1>
                <form className="rounded-lg flex flex-col overflow-hidden" onSubmit={handleReasearch}>
                    <div className={`flex w-full transition-all gap-2 ${showSearchResults ? "h-0 opacity-0" : "h-10 opacity-100"}`}>
                        <div className={`bg-white w-1/2 h-full flex items-center justify-center rounded-t-lg ${searchMode === 0 ? "" : " opacity-50 cursor-pointer shadow-[inset_0px_-2px_10px_#00000080]"}`} onClick={(e) => {
                            e.preventDefault();
                            setSearchMode(0);
                        }}>
                            <p className="text-xl text-black">Startup name</p>
                        </div>
                        <div className={`bg-white w-1/2 h-full flex items-center justify-center rounded-t-lg ${searchMode === 1 ? "" : " opacity-50 cursor-pointer shadow-[inset_0px_-2px_10px_#00000080]"}`} onClick={(e) => {
                            e.preventDefault();
                            setSearchMode(1);
                        }}>
                            <p className="text-xl text-black">Market</p>
                        </div>
                    </div>
                    <div className="bg-white w-[60rem] py-1 pl-4 pr-1 flex gap-2">
                        <input type="text" className="outline-none w-full text-2xl my-1" placeholder={`Search for a ${searchMode === 0 ? "startup" : "market"}`} value={market} onChange={(e) => {setMarket(e.target.value)}} />
                        <button type="submit" className="bg-[#7E99A3] text-black text-2xl rounded px-2 transition-colors hover:bg-black hover:text-[#7E99A3]">Search</button>
                    </div>
                    {/* Advanced parameters */}
                    <div className={`w-[60rem] bg-white px-3 transition-all ${showSearchResults ? "max-h-0 opacity-0 pt-0" : "max-h-screen pt-2 opacity-100"}`}>
                        <div className="h-12 cursor-pointer w-full flex items-center gap-5" onClick={() => {setAdvancedParametersShow(!advancedParametersShow)}}>
                            <div className="w-5 h-full relative flex items-center justify-center translate-x-2.5">
                                <span className={`absolute w-3 h-0.5 lg:w-4 bg-black ${advancedParametersShow ? "-rotate-45" : "rotate-45"} -translate-x-2.5 transition-transform`}></span>
                                <span className={`absolute w-3 h-0.5 lg:w-4 bg-black ${advancedParametersShow ? "rotate-45" : "-rotate-45"} transition-transform`}></span>
                            </div>
                            <p className="text-black text-xl">Advanced parameters</p>
                        </div>
                        <div className={`w-full transition-all grid grid-cols-2 duration-500 delay-0 ${advancedParametersShow ? "max-h-screen pb-2" : "max-h-0 pb-0"}`}>
                        {advancedParameters.map((parameter, index) => {
                            const isSelected = advancedParametersSelected.includes(parameter);
                            const handleClick = () => {
                                if (isSelected) {
                                    setAdvancedParametersSelected(advancedParametersSelected.filter((item) => item !== parameter));
                                } else {
                                    setAdvancedParametersSelected([...advancedParametersSelected, parameter]);
                                }
                            };
                            return (
                                <div key={index} onClick={handleClick} className="flex items-center gap-2 cursor-pointer">
                                    <div className={`h-5 w-5 rounded border border-black flex items-center justify-center ${isSelected && "bg-[#7E99A3]"}`}></div>
                                    <label className="text-black text-lg">{parameter}</label>
                                </div>
                            );
                        })}
                        </div>
                    </div>
                </form>
            </div>
            {showSearchResults && (
                <div className="w-full h-full px-32">
                    {marketReasearched && <p className="text-white text-3xl mb-8">Search results on {marketReasearched} :</p>}
                    {!results ? <div className="w-full h-[calc(100vh-10rem)] flex items-center justify-center">
                        <div className="flex flex-col items-center gap-5">
                            <p className="text-3xl text-white">{loadingMessage}</p>
                            <div className="w-[30rem] bg-[#00000080] h-5 rounded-full overflow-hidden">
                                <div className="bg-[#ffffff] h-full duration-700 transition-all rounded-full" style={{width: `${progress}%`}}></div>
                            </div>
                        </div>
                    </div> : (
                        <div className="flex flex-col gap-2 mb-10">
                            {results.map((result, index) => {
                                if (result.type === 'text') {
                                    return (
                                        <p key={index} className="text-white text-lg" dangerouslySetInnerHTML={{ __html: result.value }}/>
                                    );
                                } else if (result.type === 'title1') {
                                    return (
                                        <p key={index} className="text-white text-5xl mt-10" dangerouslySetInnerHTML={{ __html: result.value }}/>
                                    );
                                } else if (result.type === 'title2') {
                                    return (
                                        <p key={index} className="text-white text-4xl mt-8" dangerouslySetInnerHTML={{ __html: result.value }}/>
                                    );
                                } else if (result.type === 'title3') {
                                    return (
                                        <p key={index} className="text-white text-3xl mt-6" dangerouslySetInnerHTML={{ __html: result.value }}/>
                                    );
                                } else if (result.type === 'title4') {
                                    return (
                                        <p key={index} className="text-white text-2xl mt-4" dangerouslySetInnerHTML={{ __html: result.value }}/>
                                    );
                                } else if (result.type === 'dash') {
                                    return (
                                        <span className="w-full h-px rounded-full my-8 bg-white bloc" />
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
                                                                    <td key={cellIndex} className="border border-white p-2" dangerouslySetInnerHTML={{ __html: cell }}/>
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