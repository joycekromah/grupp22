import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from NewsAPI import main as findNews
from YoutubeCommentsAPI import main as findComments
from main_scrubb import Scrubber
import subprocess
import json
from twisted.internet import reactor



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
            tb_str = traceback.format_exc()
            raise HTTPException(status_code=500, detail={
                "error": str(e),
                "traceback": tb_str,
                "data": data if 'data' in locals() else None,
            })

        return json.loads(sentiment_result)
    except subprocess.CalledProcessError as e:
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
            "data": data if 'data' in locals() else None,
        })
    except json.JSONDecodeError as e:
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
            "data": data if 'data' in locals() else None,
        })
    except Exception as e:
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
            "data": data if 'data' in locals() else None,
        })

@app.get("/fetchData/")
def search_word(search_word: str):
    """
    Endpoint to search for a word, process the data, and return sentiment analysis.
    """
    try:
        data = fetch_searches(search_word)

        sentiment_result = run_sentiment_analysis(data)

        return {
            "search_word": search_word,
            "sentiment_score": sentiment_result.get("averageSentiment"),
        }
    except Exception as e:
        # Capture the full traceback as a string
        tb_str = traceback.format_exc()
        # Raise an HTTPException with the traceback in the detail
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
            "data": data if 'data' in locals() else None,
        })

@app.get("runAnalysis")
def