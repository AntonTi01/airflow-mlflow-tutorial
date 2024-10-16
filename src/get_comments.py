import json
import logging

import requests
from googleapiclient.discovery import build


# Инициализация клиента YouTube API
def initialize_youtube(YOUTUBE_API_KEY):
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Получение данных о комментариях
def get_data(YOUTUBE_API_KEY, videoId, maxResults, nextPageToken):
    """
    Получение информации со страницы с видео
    """
    YOUTUBE_URI = 'https://www.googleapis.com/youtube/v3/commentThreads?key={KEY}&textFormat=plainText&' + \
        'part=snippet&videoId={videoId}&maxResults={maxResults}&pageToken={nextPageToken}'
    format_youtube_uri = YOUTUBE_URI.format(KEY=YOUTUBE_API_KEY,
                                            videoId=videoId,
                                            maxResults=maxResults,
                                            nextPageToken=nextPageToken)
    content = requests.get(format_youtube_uri).text
    data = json.loads(content)
    return data

# Функция для получения ID видео по ключевым словам
def get_video_ids(youtube, query, count_video=10):
    """
    Поиск видео по ключевым словам
    """
    search_response = youtube.search().list(
        q=query,
        part='id',
        maxResults=count_video,
        type='video'
    ).execute()
    
    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    return video_ids


def get_text_of_comment(data):
    """
    Получение комментариев из полученных данных под одним видео
    """
    comms = set()
    for item in data['items']:
        comm = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comms.add(comm)
    return comms


# Основная функция для получения всех комментариев
def get_all_comments(YOUTUBE_API_KEY, query, count_video=10, limit=30, maxResults=10, nextPageToken=''):
    """
    Выгрузка maxResults комментариев
    """
    youtube = initialize_youtube(YOUTUBE_API_KEY)
    videoIds = get_video_ids(youtube, query, count_video)

    comments_all = []
    for id_video in videoIds:
        try:
            data = get_data(YOUTUBE_API_KEY, id_video, maxResults=maxResults, nextPageToken=nextPageToken)
            comment = list(get_text_of_comment(data))
            comments_all.append(comment)
        except Exception as e:
            logging.error(f"Error fetching comments for video ID {id_video}: {e}")
            continue
    comments = sum(comments_all, [])
    return comments