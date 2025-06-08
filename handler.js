/*
This file contains the methods used to communicate with the backend.
 */
export async function fetchNewsData(query) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/NewsData/?search_word=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("data.data i handler", data.data);
        return data.data;
    } catch (error) {
        console.error('Error fetching sentiment value:', error);
        throw error;
    }
}

export async function fetchTwitterData(query) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/TwitterData/?search_word=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("data.data i handler", data.data);
        return data.data;
    } catch (error) {
        console.error('Error fetching sentiment value:', error);
        throw error;
    }
}

export async function fetchYTData(query) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/YoutubeCommentsData/?search_word=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("data.data i handler", data.data);
        return data.data;
    } catch (error) {
        console.error('Error fetching sentiment value:', error);
        throw error;
    }
}

export async function fetchAllData(query) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/AllData/?search_word=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("data.data i handler", data.data);
        return data.data;
    } catch (error) {
        console.error('Error fetching sentiment value:', error);
        throw error;
    }
}

export async function fetchSentimentValue(data) {
    try {
        console.log("data in handler", data);
        const response = await fetch('http://127.0.0.1:8000/Analysis/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                data: data,
            })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const res = await response.json();
        console.log("res in handler", res);
        return res.sentiment_score;
    }  catch (error) {
        console.error('Error fetching sentiment value:', error.message);
        console.error('Stack Trace:', error.stack);
        throw error;
    }
}




