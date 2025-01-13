from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from NewsAPI import main as findNews
from YoutubeCommentsAPI import main as findComments
from main_scrubb import Scrubber
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

def fetch_searches(search_word):
    news_data = findNews(search_word)
    yt_comments_data = findComments(search_word)  # Returns JSON object from YTCommentsAPI
    scrubber = Scrubber()
    twitter_data = scrubber.main(search_word)

    del scrubber
    return {"news": news_data, "youtube_comments": yt_comments_data, "Twitter": twitter_data}
    #return {"news": news_data, "youtube_comments": yt_comments_data}



def run_sentiment_analysis(data):
    try:
        # Pass data to sentiment.js via subprocess
        process = subprocess.Popen(
            ["node", "sentiment.js"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        input_data = json.dumps(data)
        sentiment_result, error = process.communicate(input=input_data)

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error running sentiment.js: {error}")

        return json.loads(sentiment_result)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error running sentiment.js: {e}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON returned by sentiment.js: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@app.get("/search/")
def search_word(search_word: str):
    """
    Endpoint to search for a word, process the data, and return sentiment analysis.
    """
    try:
        data = fetch_searches(search_word)

        sentiment_result = run_sentiment_analysis(data)

        del data

        return {
            "search_word": search_word,
            "sentiment_score": sentiment_result.get("averageSentiment"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))