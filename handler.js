/*
This file contains the methods used to communicate with the backend.
 */
export async function fetchSentimentValue(query) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/search/?fetchData=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.sentiment_score;
    } catch (error) {
        console.error('Error fetching sentiment value:', error);
        throw error;
    }
}




