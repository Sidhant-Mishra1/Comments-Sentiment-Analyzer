import googleapiclient.discovery
import re, requests
from model import *

# Set your API key here
api_key = "AIzaSyCro15HRsmS4dS-IS08AhDw_S6Dd8CVlJ8"

# Create a YouTube resource object
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)


def get_video_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_comments(video_id):
    comments = []
    try:
        request = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText", maxResults=100)
    
    except:
        print("Error")
        
    else:
        while request:
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            
            request = youtube.commentThreads().list_next(request, response)
    
        return comments

def main(url):
    video_id = get_video_id(url)
    
    if not video_id:
        print("Invalid YouTube URL")
        return "Invalid YouTube URL"

    comments = get_comments(video_id)
    prediction_dict = predict_classes(comments)
    print(prediction_dict)
    # for i, comment in enumerate(comments, 1):
    #     print(f"{i}. {comment}")
    return prediction_dict

# main("https://www.youtube.com/watch?v=M-V5MxTtitM")
    