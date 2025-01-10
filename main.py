from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # Replace "*" with your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_sentiment_analysis():
    """
    Helper function to run sentiment.js and retrieve sentiment value.
    """
    try:
        # Run the sentiment analysis using Node.js
        sentiment_result = subprocess.check_output(["node", "sentiment.js"])
        return json.loads(sentiment_result.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error running sentiment.js: {e}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON returned by sentiment.js.")

@app.get("/search/")
def search_word(search_word: str):
    """
    Endpoint to search for a word, process the data, and return sentiment analysis.
    """
    # Step 1: Fetch news and YouTube data
    """
    Lägg in metoderna för yt, news osv här med searchword som input. 
    """


    # Step 2: Run sentiment analysis

    try:
        # Perform sentiment analysis
        #result = run_sentiment_analysis()
        with open("average_sentiment_result.json", "r") as file:
            sentiment_data = json.load(file)
            sentiment_score = sentiment_data.get("averageSentiment")

        return {
            "search_word": search_word,
            "sentiment_score": sentiment_score,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))