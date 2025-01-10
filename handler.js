/*
This file contains the methods used to communicate with the backend.
 */
export async function fetchSentimentValue (query) {
    await new Promise(resolve => setTimeout(resolve, 3000)); // 5-second delay
    /* Simulate a backend value
    This const has to be replaced with a call to the backend API for a real value.
     */
    const backendValue = Math.floor(Math.random() * 10) - 5; // Random number between -5 and 5
    return backendValue;
}