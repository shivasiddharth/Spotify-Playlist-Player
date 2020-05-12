import urllib.request
import pafy
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import yaml
import random
import os

ROOT_PATH = os.path.realpath(os.path.join(__file__, '..', '..'))

with open('{}/src/config.yaml'.format(ROOT_PATH), 'r') as conf:
    configuration = yaml.load(conf)

# API Key for YouTube
google_cloud_api_key = configuration['Google_cloud_api_key']

# YouTube API Constants
DEVELOPER_KEY = google_cloud_api_key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


# Function to search YouTube and get videoid
def youtube_search(query, maximum=1):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=query,
        part='id,snippet'
    ).execute()
    # print(search_response)
    
    videos = []
    videoids = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))
            videoids.append(search_result['id']['videoId'])

    if len(videoids) != 0:
        if maximum == 1:
            return videoids[0]
        else:
            ids = []
            for id in videoids:
                ids.append(id)
                if len(ids) >= maximum:
                    return ids
            return ids
    elif maximum == 1:
        return []


# Function to get streaming links for YouTube URLs
def youtube_stream_link(video_url):
    video = pafy.new(video_url)
    best_video = video.getbest()
    best_audio = video.getbestaudio()
    audio_streaming_link = best_audio.url
    video_streaming_link = best_video.url
    return audio_streaming_link, video_streaming_link
