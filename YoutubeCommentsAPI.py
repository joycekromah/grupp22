import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

MAX_COMMENTS_PER_VIDEO = 10

MAX_VIDEOS = 5

def search_videos(keyword, api_key, max_videos=5):

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "maxResults": max_videos,
        "key": api_key,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        videos = [
            {
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
            }
            for item in data.get("items", [])
        ]
        return videos
    else:
        print(f"Error during video search: {response.status_code} - {response.text}")
        return []

def fetch_video_comments(video_id, api_key, max_comments=50):

    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_comments,
        "key": api_key,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        comments = []
        for item in data.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            comments.append(comment)
        return comments
    else:
        print(f"Error fetching comments for video {video_id}: {response.status_code} - {response.text}")
        return []

def main(searchWord):

    videos = search_videos(searchWord, API_KEY, MAX_VIDEOS)
    if not videos:
        return []

    result = []

    for video in videos:
        video_id = video["videoId"]
        video_title = video["title"]
        comments = fetch_video_comments(video_id, API_KEY, MAX_COMMENTS_PER_VIDEO)
        result.append({
            "title": video_title,
            "videoId": video_id,
            "comments": comments,
        })

    for item in result:
        print(f"Title: {item['title']}, Video ID: {item['videoId']}")

    return result