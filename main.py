import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from NewsAPI import main as findNews
from YoutubeCommentsAPI import main as findComments
from main_scrubb import Scrubber
from fastapi import Request
import subprocess
import json
from twisted.internet import reactor



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fetch_searches(search_word):
    news_data = findNews(search_word)
    yt_comments_data = findComments(search_word)
    scrubber = Scrubber()
    twitter_data = scrubber.main(search_word)


    return {"news": news_data, "youtube_comments": yt_comments_data, "Twitter": twitter_data}




def run_sentiment_analysis(data):
    try:
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
            print("Error running sentiment.js:", error)

            tb_str = traceback.format_exc()
            raise HTTPException(status_code=500, detail={
                "error": str(error),
                "traceback": tb_str,
                "data": data if 'data' in locals() else None,
            })
        print("Output from sentiment.js:", sentiment_result)

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

@app.get("/fetchTwitterData/")
def fetch_twitter_data(search_word: str):
    try:
        scrubber = Scrubber()
        twitter_data = scrubber.main(search_word)
        data = {"twitter": twitter_data}

        return {
            "data": data
        }
    except Exception as e:
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
            "data": twitter_data if 'data' in locals() else None,
        })

@app.get("/fetchNewsData/")
def fetch_news_data(search_word: str):
    try:
        news_data = findNews(search_word)
        data = {"news": news_data}
        return {
            "data": data
        }
    except Exception as e:
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
            "data": news_data if 'data' in locals() else None,
        })

@app.get("/fetchYoutubeCommentsData/")
def fetch_youtube_comments_data(search_word: str):
    try:
        yt_data = findComments(search_word)
        data = {"youtube_comments": yt_data}
        return {
            "data": data
        }
    except Exception as e:
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
            "data": yt_data if 'data' in locals() else None,
        })


@app.get("/fetchAllData/")
def fetch_all_data(search_word: str):
    """
    Endpoint to search for a word, process the data, and return sentiment analysis.
    """
    try:
        data = fetch_searches(search_word)
        return {
            "data": data,
        }
    except Exception as e:
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
            "data": data if 'data' in locals() else None,
        })

@app.post("/runAnalysis/")
async def run_analysis(req: Request):
    try:
        req = await req.json()
        data = req.get("data", req)
        sentiment_result = run_sentiment_analysis(data)

        return {
            "sentiment_score": sentiment_result.get("averageSentiment")
        }

    except Exception as e:
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "traceback": tb_str,
        })