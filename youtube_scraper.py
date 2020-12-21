
import os
import csv
import re

from googleapiclient.discovery import build


DEVELOPER_KEY = "Your Youtube API Key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MAX_RESULT = 50
KEYWORD = 'Bitcoin'


def main():
    max_pages = 100
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="id,snippet",
        q=KEYWORD,
        maxResults=MAX_RESULT
    )
    response = request.execute()

    total_records = response.get('pageInfo').get('totalResults')
    total_pages = int(total_records / MAX_RESULT)
    next_page_token = response.get('nextPageToken')
    if os.path.isfile('yt_{}.csv'.format(KEYWORD)):
        os.remove('yt_{}.csv'.format(KEYWORD))
    with open('yt_{}.csv'.format(KEYWORD), 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['Channel Id', 'Channel Link', 'Title', 'Description', 'Channel Title',
                         'Subscribers', 'View Count', 'Video Count', 'Email'])
        save_data(youtube, response, writer)

        if not max_pages:
            max_pages = total_pages

        while max_pages != 0:
            print(max_pages)
            max_pages -= 1

            request = youtube.search().list(
                part="id,snippet",
                q="Bitcoin",
                pageToken=next_page_token,
                maxResults=MAX_RESULT
            )
            response = request.execute()
            save_data(youtube, response, writer)
            next_page_token = response.get('nextPageToken')


def save_data(youtube, response, writer):

    for search_result in response.get("items", []):
        channel_id = search_result.get('snippet').get('channelId')
        channel_link = 'https://www.youtube.com/channel/' + str(channel_id)
        title = search_result.get('snippet').get('title')
        description = search_result.get('snippet').get('description')
        channel_title = search_result.get('snippet').get('channelTitle')

        request = youtube.channels().list(
            part="statistics,contentOwnerDetails",
            id=channel_id
        )
        response_channel = request.execute()

        subscribers = response_channel.get('items')[0].get('statistics').get('viewCount')
        view_count = response_channel.get('items')[0].get('statistics').get('subscriberCount')
        video_count = response_channel.get('items')[0].get('statistics').get('videoCount')
        mail_address = re.findall(r'[\w\.-]+@[\w\.-]+', description)
        email = ','.join(mail_address)
        writer.writerow([channel_id, channel_link, title, description, channel_title,
                         subscribers, view_count, video_count, email])


if __name__ == "__main__":
    main()
