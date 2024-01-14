# cover dates
import googleapiclient.discovery
import os
from dotenv import load_dotenv
import datetime

aug_d = datetime.date(2023, 8, 8)
may_d = datetime.date(2023, 5, 22)


load_dotenv()
#
api_key = os.environ.get("youtubeapi")

youtube = googleapiclient.discovery.build(
    'youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    forUsername="tseries")

response = request.execute()


channel_id = response['items'][0]['id']
playlistid = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def videos():
    playlist = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlistid,
        maxResults=50
    )

    playlist_response = playlist.execute()

    videos_ids = []
    # grab video date
    for i in range(len(playlist_response['items'])):
        video_publish_date = playlist_response['items'][i]['contentDetails']['videoPublishedAt'].split(
            'T')
        c_date = video_publish_date[0].split('-')
        video_current_date = datetime.date(
            int(c_date[0]), int(c_date[1]), int(c_date[2]))

        if may_d < video_current_date < aug_d:
            videos_ids.append(
                playlist_response['items'][i]['contentDetails']['videoId'])

    more_pages = True
    next_page = playlist_response.get('nextPageToken')
    while more_pages:
        if  next_page is None:
            more_pages = False
        else:
            playlist = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlistid,
                maxResults=50,
                pageToken=next_page
            )
            playlist_response = playlist.execute()

            for i in range(len(playlist_response['items'])):
                video_publish_date = playlist_response['items'][i]['contentDetails']['videoPublishedAt'].split(
                    'T')
                c_date = video_publish_date[0].split('-')
                video_current_date = datetime.date(
                    int(c_date[0]), int(c_date[1]), int(c_date[2]))

                if may_d < video_current_date < aug_d:
                    videos_ids.append(
                        playlist_response['items'][i]['contentDetails']['videoId'])
                elif video_current_date < may_d:
                    more_pages=False
            next_page = playlist_response.get('nextPageToken')

    return videos_ids


# call the function
videos_ids = videos()


result = {}
for ids in videos_ids:
    for j in ids:
        if j in result:
            result[j] = result.get(j)+1
        else:
            result[j] = 1
value = list(result.values())

value.sort(reverse=True)
first = value[0]

for k, v in result.items():
    if v == first:
        print(f'key:{k} value:{v}')
